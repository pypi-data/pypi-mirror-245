import os
import logging
import urllib3
import sys
import yaml
from datetime import datetime

from jf_ingest.jf_jira.auth import JiraAuthConfig
from jf_ingest.jf_jira import JiraIngestionConfig, load_and_push_jira_to_s3


def setup_harness_logging(logging_level: int):
    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s %(threadName)s %(levelname)s %(name)s %(message)s"
        if logging_level == logging.DEBUG
        else "%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger(urllib3.__name__).setLevel(logging.WARNING)


# NOTE: This is a work in progress developer debugging tool.
# it is currently run by using the following command:
#   pdm run ingest_harness
# and it requires you to have a creds.env and a config.yml file at
# the root of this project
if __name__ == "__main__":
    debug_mode = "--debug" in sys.argv

    # Get credentials for Auth Config
    auth_config = JiraAuthConfig(
        company_slug=os.getenv("COMPANY_SLUG"),
        url=os.getenv("JIRA_URL"),
        user=os.getenv("JIRA_USERNAME"),
        password=os.getenv("JIRA_PASSWORD"),
    )
    # Get Config data for Ingestion Config
    with open("./config.yml") as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)
        jira_config_data = yaml_data["jira"]
        jira_config_data["earliest_issue_dt"] = (
            datetime.strptime(jira_config_data["earliest_issue_dt"], "%Y-%m-%d")
            if jira_config_data["earliest_issue_dt"]
            else None
        )
        jira_config_data["work_logs_pull_from"] = (
            datetime.strptime(jira_config_data["work_logs_pull_from"], "%Y-%m-%d")
            if jira_config_data["work_logs_pull_from"]
            else datetime.min
        )
        ingest_config = JiraIngestionConfig(**jira_config_data)
        # Inject auth data into config
        ingest_config.auth_config = auth_config
        if ingest_config.earliest_issue_dt == None:
            print(
                "earliest_issue_dt option in config.yml detected as being null, setting to datetime.min!"
            )
            ingest_config.earliest_issue_dt = datetime.min

    setup_harness_logging(logging_level=logging.DEBUG if debug_mode else logging.INFO)

    load_and_push_jira_to_s3(ingest_config)
