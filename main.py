import sys

from config_reader import create_config_reader, read_job_config
from gitlab_runner import exec_runner


def foo(job_name: str, config_file: str):
    config = read_job_config(create_config_reader(config_file), job_name)
    environment_entries = list_uppercase_entries(config)
    exec_runner(job_name, executor=config['executor'], shell=config.get('shell'), env_entries=environment_entries)


def list_uppercase_entries(dictionary: dict) -> dict:
    return {key: dictionary[key] for key in dictionary.keys() if key.isupper()}


if __name__ == '__main__':
    job_name = sys.argv[1]
    config_file = sys.argv[2]
    foo(job_name, config_file)
