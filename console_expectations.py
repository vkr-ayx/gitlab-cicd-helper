from typing import List

import runner_config
from gitlab_ci import CiConfigFile


def all_executors() -> List[str]:
    configs = runner_config.DEFAULT_CONFIGS.values()
    return [config['executor'] for config in configs]


def suggest_executors(job_name: str, ci_file: CiConfigFile) -> List[str]:
    job = ci_file.get_job(job_name)
    configs = runner_config.suggest_configs(job)
    executors = [conf['executor'] for conf in configs]
    return executors


def list_job_tags(job_name: str, ci_file: CiConfigFile) -> List[str]:
    job = ci_file.get_job(job_name)
    return job['tags']
