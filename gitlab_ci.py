from typing import List
from os.path import exists
import yaml

GLOBAL_KEYWORDS = [
    'default',
    'include',
    'stages',
    'variables',
    'workflow',
]


class CiConfigFile:

    def __init__(self, ci_file_path: str):
        self.file_path = ci_file_path
        if not exists(ci_file_path):
            raise ValueError(f"Cannot open file {ci_file_path}.")
        self.yml = self._load_ci_file(ci_file_path)

    @staticmethod
    def _load_ci_file(ci_file_path: str) -> dict:
        with open(ci_file_path, 'r') as ci:
            try:
                return yaml.safe_load(ci)
            except yaml.YAMLError as e:
                print(e)
                raise e

    def get_job(self, job_name: str) -> dict:
        job = self.yml[job_name]
        if type(job) is not dict:
            raise ValueError(f"{job_name} is not a job! ({type(job)})")
        return job

    def list_jobs(self) -> List[dict]:
        job_names = self.list_job_names()
        jobs = [self.yml[job_name] for job_name in job_names]
        return jobs

    def list_job_names(self) -> List[str]:
        job_names = [j for j in self.yml.keys() if j not in GLOBAL_KEYWORDS]
        return job_names
