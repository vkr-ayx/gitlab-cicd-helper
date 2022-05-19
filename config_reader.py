import configparser
import os

DEFAULT_SECTION = 'DEFAULT'
CONFIG_FILE = 'config.ini'
MANDATORY_PARAMS = ['executor', 'GIT_BRANCH', 'CI_JOB_TOKEN']


def read_job_config(config, job_name: str):
    if job_name not in config:
        raise ValueError(f"Configuration file '{CONFIG_FILE}' is missing the '{job_name}' section.")

    default = config[DEFAULT_SECTION]
    job = config[job_name]
    merged = dict()
    merged.update(default)
    merged.update(job)
    missing_keys = [mandatory for mandatory in MANDATORY_PARAMS if mandatory not in merged.keys()]
    if len(missing_keys) > 0:
        raise ValueError(f"Configuration for job '{job_name}' is missing mandatory keys {missing_keys}")

    return merged


def _check_file_exists(config_file_path: str):
    if not os.path.exists(config_file_path):
        raise ValueError(f"Config file '{config_file_path}' does not exist.")


def create_config_reader(config_file_path: str):
    _check_file_exists(config_file_path)
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(config_file_path)
    if DEFAULT_SECTION not in config:
        raise ValueError(f"Configuration file {CONFIG_FILE} is missing the mandatory '{DEFAULT_SECTION}' section.")
    return config
