import subprocess
from typing import Optional


def exec_runner(job_name: str, executor: str, shell: Optional[str] = None, env_entries: dict = None):
    if env_entries is None:
        env_entries = {}

    print('environment: ', env_entries.items())

    path_to_runner = 'C:\gitlab-runner\gitlab-runner.exe'
    executor = executor
    args = [path_to_runner, 'exec', executor]
    if shell:
        args += ['--shell', shell]
    for env_var, val in env_entries.items():
        args += ['--env', f'{env_var}={val}']
    args += [job_name]
    print(subprocess.list2cmdline(args))
    subprocess.run(args)
