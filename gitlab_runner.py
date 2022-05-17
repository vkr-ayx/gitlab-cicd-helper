import subprocess
from typing import Optional


def exec_runner(job_name: str, executor: str, shell: Optional[str] = None, env_vars: dict = None):
    path_to_runner = 'C:\gitlab-runner\gitlab-runner.exe'
    executor = executor
    args = [path_to_runner, 'exec', executor]
    if shell:
        args += ['--shell', shell]
    for var in env_vars:
        args += ['--env', var]
    args += [job_name]
    print(args)
    subprocess.run(args)
