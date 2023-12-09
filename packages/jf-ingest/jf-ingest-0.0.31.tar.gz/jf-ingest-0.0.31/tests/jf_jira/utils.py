import json
import os

import requests_mock

from jf_ingest.jf_jira.auth import JiraAuthConfig, get_jira_connection
from jf_ingest.jf_jira.downloaders import IssueMetadata

_MOCK_REST_BASE_URL = "https://test-co.atlassian.net/rest/api/2"
_MOCK_AGILE_BASE_URL = "https://test-co.atlassian.net/rest/agile/1.0"


def get_jira_mock_connection():

    _MOCK_SERVER_INFO_RESP = (
        '{"baseUrl":"https://test-co.atlassian.net","version":"1001.0.0-SNAPSHOT",'
        '"versionNumbers":[1001,0,0],"deploymentType":"Cloud","buildNumber":100218,'
        '"buildDate":"2023-03-16T08:21:48.000-0400","serverTime":"2023-03-17T16:32:45.255-0400",'
        '"scmInfo":"9999999999999999999999999999999999999999","serverTitle":"JIRA",'
        '"defaultLocale":{"locale":"en_US"}} '
    )

    auth_config = JiraAuthConfig(
        url="https://test-co.atlassian.net/",
        personal_access_token="asdf",
        company_slug="test_co",
    )

    with requests_mock.Mocker() as m:
        _register_jira_uri(m, "serverInfo", f"{_MOCK_SERVER_INFO_RESP}")
        _register_jira_uri_with_file(m, "field", "api_responses/fields.json")
        jira_conn = get_jira_connection(config=auth_config, max_retries=1)

    return jira_conn


def get_fixture_file_data(fixture_path: str):
    with open(f"{os.path.dirname(__file__)}/fixtures/{fixture_path}", "r") as f:
        return f.read()


def get_jellyfish_issue_metadata() -> dict[str, IssueMetadata]:
    with open(
        f"{os.path.dirname(__file__)}/fixtures/jellyfish_issue_metadata.json", "r"
    ) as f:
        return [
            IssueMetadata(**metadata_dict) for metadata_dict in json.loads(f.read())
        ]


def _register_jira_uri_with_file(
    mock: requests_mock.Mocker, endpoint: str, fixture_path: str
):
    _register_jira_uri(mock, endpoint, get_fixture_file_data(fixture_path=fixture_path))


def _register_jira_uri(
    mock: requests_mock.Mocker,
    endpoint: str,
    return_value: str,
    HTTP_ACTION: str = "GET",
    use_agile_endpoint: bool = False,
    status_code: int = 200,
):
    """Helper function used to registering mock results for testing against our mock JIRA API. Works by providing
    a request_mock.Mocker instance, what endpoint you want to spoof, and the string that you want that spoofed endpoint
    to return

    Args:
        mock (requests_mock.Mocker): Mocker object
        endpoint (str): Endpoint to append to the end of the base URL ("https://test-co.atlassian.net/rest/api/2", unless use_agile_endpoint is True)
        return_value (str): The raw str to return from the API endpoint
        use_agile_endpoint (bool, optional): IF TRUE, switch the default base URL from the /rest/api/2 endpoint to the agile endpoint. MUST BE TRUE FOR SPRINT AND BOARD API ENDPOINTS. Defaults to False.
    """

    mock_base_url = (
        _MOCK_REST_BASE_URL if not use_agile_endpoint else _MOCK_AGILE_BASE_URL
    )
    mock.register_uri(
        HTTP_ACTION,
        f"{mock_base_url}/{endpoint}",
        text=return_value,
        status_code=status_code,
    )
