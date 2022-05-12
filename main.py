from gitlab_ci import list_jobs, list_job_names
import sys


def foo():
    return list_job_names('C:\git\project_100\.gitlab-ci.yml')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # job = sys.argv[1]
    print(foo())
