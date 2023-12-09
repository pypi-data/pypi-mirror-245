import dataclasses
import json
import logging
import os
import time
from collections.abc import Callable
from concurrent.futures import Future, ThreadPoolExecutor
from datetime import datetime
from types import TracebackType
from typing import Any, Callable, Generator, Iterable, Optional
from tqdm import tqdm


from jf_ingest import logging_helper

logger = logging.getLogger(__name__)

RETRY_EXPONENT_BASE = 5


class RetryLimitExceeded(Exception):
    pass


class StrDefaultEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return str(o)


class IngestIOHelper:
    def __init__(self, s3_bucket: str, s3_path: str, local_file_path: str):
        self.s3_bucket = s3_bucket
        self.s3_path = (s3_path,)
        # EVERYTHING in this file path will (potentially) be uploaded to S3!
        # DO NOT put any creds file in this path!!!!
        self.local_file_path = local_file_path

        if not os.path.exists(self.local_file_path):
            os.makedirs(self.local_file_path)

    def _get_file_name(self, object_name: str, batch_number: Optional[int] = 0):
        return f'{object_name}{batch_number if batch_number else ""}.json'

    def write_json_data_to_local(
        self,
        object_name: str,
        json_data: dict | list[dict],
        batch_number: Optional[int] = 0,
    ):
        try:
            file_name = self._get_file_name(
                object_name=object_name, batch_number=batch_number
            )
            full_file_path = f"{self.local_file_path}/{file_name}"
            logger.debug(f"Attempting to save {object_name} data to {full_file_path}")
            with open(full_file_path, "w") as f:
                f.write(json.dumps(json_data, indent=2, cls=StrDefaultEncoder))
                logger.debug(
                    f"File: {full_file_path}, Size: {round(f.tell() / 1000000, 1)}MB"
                )
        except Exception as e:
            logger.error(
                f"Exception encountered when attempting to write data to local file! Error: {e}"
            )

    def upload_files_to_s3(self):
        # TODO: Write multi threaded uploader to upload this local_file_path
        raise NotImplementedError("Function not implemented!")


def get_wait_time(e: Optional[Exception], retries: int) -> int:
    """
    This function attempts to standardize determination of a wait time on a retryable failure.
    If the exception's response included a Retry-After header, respect it.
    If it does not, we do an exponential backoff - 5s, 25s, 125s.

    A possible future addition would be to add a jitter factor.
    This is a fairly standard practice but not clearly required for our situation.
    """
    # getattr with a default works on _any_ object, even None.
    # We expect that almost always e will be a JIRAError or a RequestException, so we will have a
    # response and it will have headers.
    # So I'm choosing to use the getattr call to handle the valid but infrequent possibility
    # that it may not (None or another Exception type that doesn't have a response), rather tha
    # preemptively checking.
    response = getattr(e, "response", None)
    headers = getattr(response, "headers", {})
    retry_after = headers.get("Retry-After")

    # Normalize retry after if it is a string
    if isinstance(retry_after, str) and retry_after.isnumeric():
        retry_after = int(retry_after)
    # Don't do anything if we have a valid int for retry after
    elif isinstance(retry_after, int):
        pass
    else:
        # Null out any invalid retry after values
        retry_after = None

    if retry_after:
        return retry_after
    else:
        return RETRY_EXPONENT_BASE ** retries


def retry_for_429s(f: Callable[..., Any], *args, max_retries: int = 5, **kwargs) -> Any:
    """
    This function allows for us to retry 429s from Jira. There are much more elegant ways of accomplishing
    this, but this is a quick and reasonable approach to doing so.

    Note:
        - max_retries=5 will give us a maximum wait time of 10m25s.
    """
    for retry in range(max_retries + 1):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            if hasattr(e, "status_code") and e.status_code == 429:
                if retry < max_retries:
                    wait_time = get_wait_time(e, retries=retry)
                    logging_helper.log_standard_error(
                        logging.WARNING,
                        # NOTE: Getting the function name here isn't always useful,
                        # because sometimes we circumvent the JIRA standard library
                        # and use functions like "get" and "_get_json", but it's still
                        # better than nothing
                        msg_args=[f.__name__, retry, max_retries, wait_time],
                        error_code=3071,
                    )
                    time.sleep(wait_time)
                    continue
                else:
                    raise RetryLimitExceeded(e)

            # Raise any non-429 related errors
            raise


def batch_iterable(
    iterable: Iterable, batch_size: int
) -> Generator[list[Any], None, None]:
    """Helper function used for batching a given iterable into equally sized batches

    Args:
        iterable (Iterable): An iterable you want to split into batches
        batch_size (int): The size of the batches you want

    Yields:
        Generator[list[Any], None, None]: This generator yields a list of equal size batches, plus a potential final batch that is less than the batch_size arg
    """
    chunk = []
    i = 0
    for item in iterable:
        chunk.append(item)
        i += 1
        if i == batch_size:
            yield chunk
            chunk = []
            i = 0

    if chunk:
        yield chunk


def format_date_to_jql(datetime: datetime):
    return datetime.strftime("%Y-%m-%d")


class ThreadPoolWithTqdm(ThreadPoolExecutor):
    """THIS CLASS MUST BE USED AS A CONTEXT MANAGER ONLY!!!!
    
    This is a custom class that extends the ThreadPoolExecutor class,
    and combines it with some TQDM (progress bar) functionality. This
    should help reduce the number of repeated code around jf_ingest
    
    Yes, I know there is a concurrency extension for TQDM (tqdm.contrib.concurrent)
    BUT this library only has .map style functions, and it does NOT have a submit style
    function. There are instances where using submit is preferred, and often it lends itself
    to simpler code. That is what this library is for

    Args:
        ThreadPoolExecutor (ThreadPoolExecutor): The parent class that this extends

    Returns:
        ThreadPoolWithTqdm: ThreadPoolWithTqdm
    """

    desc: str
    total: int
    exceptions_encountered: list[Exception]
    prog_bar: tqdm

    def __init__(
        self,
        desc: str = None,
        total: int = 0,
        max_workers: int | None = None,
        thread_name_prefix: str = "",
        initializer: Callable[..., object] | None = None,
        initargs: tuple[Any, ...] = ...,
    ) -> None:
        """Custom Constructor, to allow us to set the progress bar values

        Args:
            desc (str, optional): The description field on the TQDM progress bar. Defaults to None.
            total (int, optional): The total value to set on the TQDM progress bar. Defaults to 0.
            max_workers: The maximum number of threads that can be used to execute the given calls.
            thread_name_prefix: An optional name prefix to give our threads.
            initializer: A callable used to initialize worker threads.
            initargs: A tuple of arguments to pass to the initializer.
        """
        self.desc = desc
        self.total = total
        self.exceptions_encountered = []
        super().__init__(max_workers, thread_name_prefix, initializer, initargs)

    def __enter__(self):
        """Override the __enter__ function to instantiate a progress bar (TQDM)
        when using this as a context manager.
        """
        self.prog_bar = tqdm(desc=self.desc, total=self.total)
        return super().__enter__()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        """Override the __exit__ function to tear down a progress bar (TQDM)
        when using this as a context manager.
        Progress bar .close() call MUST BE AFTER THE THREADPOOLEXECUTOR TEARDOWN.
        
        Also raises any exceptions we encountered
        """
        retval = super().__exit__(exc_type, exc_val, exc_tb)

        # Progress bar must be close AFTER the parent __exit__ call,
        # because the parent __exit__ call is blocking
        self.prog_bar.close()

        if self.exceptions_encountered:
            raise self.exceptions_encountered[0]
        return retval

    def submit(self, __fn, *args, **kwargs) -> Future:
        """Submit function override, which allows us to set some custom
        callback functions that handle exceptions and progress bar logic

        Args:
            __fn (_type_): A function to submit to the pool

        Returns:
            Future: A future object returned by super class
        """
        # Get the base class generated future
        future = super().submit(__fn, *args, **kwargs)

        # Add custom callbacks
        future.add_done_callback(self.check_for_exception_callback)
        future.add_done_callback(self.update_progress_bar)
        return future

    def submit_with_custom_callbacks(
        self, __fn, custom_call_backs: list[Callable], *args, **kwargs
    ) -> Future:
        """A custom submit function that allows us to set additional callbacks

        Args:
            __fn (_type_): A function to submit to the pool
            custom_call_backs (list[Callable]): A list of custom callbacks,
            for further customization on this class

        Returns:
            Future: A future object returned by super class
        """
        future = self.submit(__fn, *args, **kwargs)

        for callback in custom_call_backs:
            future.add_done_callback(callback)

        return future

    def check_for_exception_callback(self, future: Future):
        """Helper function for dealing with exceptions. Stores them in a class
        field and raises them on exit
        
        Args:
            future (Future): A ThreadPoolExecutor Future object
        """
        exception = future.exception()
        if exception:
            self.exceptions_encountered.append(exception)

    def update_progress_bar(self, future: Future):
        """A custom callback function that iterates on the progress bar by
        default. Does some guessing to see how much we should updated the 
        progress bar by

        Args:
            future (Future): A ThreadPoolExecutor Future object
        """
        if future.exception():
            return

        result = future.result()

        with tqdm.get_lock():
            if isinstance(result, Iterable):
                self.prog_bar.update(len(result))
            else:
                self.prog_bar.update(1)
