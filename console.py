# download from https://www.lfd.uci.edu/~gohlke/pythonlibs/#curses
import curses
from typing import TypedDict, Optional

import console_expectations as exp
from gitlab_ci import CiConfigFile
from model import ExecConfig
from runner_config import is_shell_executor, DEFAULT_CONFIGS
from shells import ALL_SHELLS


class UiState:

    def __init__(self) -> None:
        self.job_name: Optional[str] = None
        self.config: Optional[ExecConfig] = None


def _setup_scr():
    scr = curses.initscr()
    scr.keypad(True)
    return scr


def _teardown(scr):
    scr.keypad(False)
    curses.endwin()


def main():
    yml_path = 'C:\git\project_100\.gitlab-ci.yml'
    ci_file = CiConfigFile(yml_path)
    ui_state = UiState()

    scr = _setup_scr()

    ui_state.job_name = ask_job_name(scr, ci_file)
    scr.clear()
    ui_state.config = ask_config(scr, ci_file, ui_state)
    if is_shell_executor(ui_state.config):
        scr.clear()
        ask_shell(scr, ui_state)
    # TODO

    _teardown(scr)


def ask_job_name(scr, ci_file: CiConfigFile) -> str:
    job_name = None

    def _do_ask():
        scr.addstr('Job to run? ')
        job = scr.getstr().decode()

        if job not in ci_file.list_job_names():
            scr.addstr(f"No such job '{job}'.\n")
            return None
        else:
            return job

    all_jobs = ci_file.list_job_names()

    scr.addstr(f'Jobs found in {ci_file.file_path}:\n\n')
    for job in all_jobs[:-1]:
        scr.addstr(f'{job}, ')
    scr.addstr(f'{all_jobs[-1]}\n\n')

    while job_name is None:
        job_name = _do_ask()

    return job_name


def ask_config(scr, ci_file: CiConfigFile, ui_state: UiState) -> ExecConfig:
    executor = None

    def _do_ask():
        scr.addstr('Executor to run? ')
        exc = scr.getstr().decode()

        if exc not in all_executors:
            scr.addstr(f"No such executor '{exc}'.\n")
            return None
        else:
            return exc

    all_executors = exp.all_executors()
    job_name = ui_state.job_name
    tags = exp.list_job_tags(job_name, ci_file)
    tags_str = ', '.join(tags)
    suggested_configs = exp.suggest_configs(job_name, ci_file)
    suggested_executors = [conf['executor'] for conf in suggested_configs]
    suggested_executors_str = ', '.join(suggested_executors)

    scr.addstr(f"Choose GitLab executor for job {ui_state.job_name}:\n")
    scr.addstr(f"Job tags: {tags_str}\n\n")
    scr.addstr('Possible executors: ')
    for exc in all_executors[:-1]:
        scr.addstr(f'{exc}, ')
    scr.addstr(f'{all_executors[-1]}\n')

    if len(suggested_executors_str) > 0:
        scr.addstr(f'Suggested executor(s) based on job tags [{tags_str}]: {suggested_executors_str}\n\n')
    else:
        scr.addstr('\n')

    while executor is None:
        executor = _do_ask()

    selected_config = [config for config in DEFAULT_CONFIGS.values() if config['executor'] == executor][0]

    return selected_config


def ask_shell(scr, ui_state: UiState):
    shell = None

    def _do_ask():
        scr.addstr('Shell to use? ')
        shell = scr.getstr().decode()

        if shell not in ALL_SHELLS:
            scr.addstr(f"No such shell '{shell}'.\n")
            return None
        else:
            return shell

    scr.addstr('Possible shells: ')
    for sh in ALL_SHELLS[:-1]:
        scr.addstr(f'{sh}, ')
    scr.addstr(f'{ALL_SHELLS[-1]}\n')

    suggested_shell = ui_state.config['shell']
    if suggested_shell is not None:
        scr.addstr(f'Suggested shell: {suggested_shell}\n\n')

    while shell is None:
        shell = _do_ask()


if __name__ == '__main__':
    # job = sys.argv[1]
    main()
