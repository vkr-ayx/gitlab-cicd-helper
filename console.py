# download from https://www.lfd.uci.edu/~gohlke/pythonlibs/#curses
import curses
from typing import TypedDict

import console_expectations as exp
from gitlab_ci import CiConfigFile


class UiState(TypedDict):
    job_name: str


def main():
    yml_path = 'C:\git\project_100\.gitlab-ci.yml'
    ci_file = CiConfigFile(yml_path)
    ui_state = UiState()

    scr = curses.initscr()
    scr.keypad(True)

    ui_state['job_name'] = ask_job_name(scr, ci_file)
    scr.clear()
    ask_executor(scr, ci_file, ui_state)
    scr.clear()
    #TODO

    scr.keypad(False)
    curses.endwin()


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


def ask_executor(scr, ci_file: CiConfigFile, ui_state: UiState) -> str:
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
    job_name = ui_state['job_name']
    tags = exp.list_job_tags(job_name, ci_file)
    tags_str = ', '.join(tags)
    tag_str = ', '.join(tags)
    suggested_executors = exp.suggest_executors(job_name, ci_file)
    suggested_executors_str = ', '.join(suggested_executors)

    scr.addstr(f"Choose GitLab executor for job {ui_state['job_name']}:\n")
    scr.addstr(f"Job tags: {tag_str}\n\n")
    scr.addstr('Possible executors: ')
    for exc in all_executors[:-1]:
        scr.addstr(f'{exc}, ')
    scr.addstr(f'{all_executors[-1]}\n')

    if len(suggested_executors_str) > 0:
        scr.addstr(f'Suggested executor(s) based on job tags {tags_str}: {suggested_executors_str}\n\n')
    else:
        scr.addstr('\n')

    while executor is None:
        executor = _do_ask()

    return executor


def printing(w):
    """
    A few simple demonstrations of printing.
    """

    w.addstr("This was printed using addstr\n\n")
    w.refresh()

    w.addstr("The following letter was printed using addch:- ")
    w.addch('a')
    w.refresh()

    w.addstr("\n\nThese numbers were printed using addstr:-\n{}\n{:.6f}\n".format(123, 456.789))
    w.refresh()


def moving_and_sleeping(w):
    """
    Demonstrates moving the cursor to a specified position before printing,
    and sleeping for a specified period of time.
    These are useful for very basic animations.
    """

    row = 5
    col = 0

    curses.curs_set(False)

    for c in range(65, 91):
        w.addstr(row, col, chr(c))
        w.refresh()
        row += 1
        col += 1
        curses.napms(100)

    curses.curs_set(True)

    w.addch('\n')


def colouring(w):
    """
    Demonstration of setting background and foreground colours.
    """

    if curses.has_colors():

        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_RED)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_CYAN)

        w.addstr("Yellow on red\n\n", curses.color_pair(1))
        w.refresh()

        w.addstr("Green on green + bold\n\n", curses.color_pair(2) | curses.A_BOLD)
        w.refresh()

        w.addstr("Magenta on cyan\n", curses.color_pair(3))
        w.refresh()

    else:

        w.addstr("has_colors() = False\n")
        w.refresh()


if __name__ == '__main__':
    # job = sys.argv[1]
    main()
