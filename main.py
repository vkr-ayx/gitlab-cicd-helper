import sys

from config_reader import create_config_reader, read_job_config
from gitlab_runner import exec_runner


def foo(job_name: str, config_file: str):
    config = read_job_config(create_config_reader(config_file), job_name)
    env = config.  # TODO remove all mandatory params from config -> env vars?
    exec_runner(job_name, executor=config['executor'], shell=config.get('shell'), env_vars=env)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    job_name = sys.argv[1]
    config_file = sys.argv[2]
    foo(job_name, config_file)
