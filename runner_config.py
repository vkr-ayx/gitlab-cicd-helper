from typing import List

from model import ExecConfig

DEFAULT_CONFIGS = {
    'windows-docker': ExecConfig(executor='docker-windows', shell=None),
    'windows-shell': ExecConfig(executor='shell', shell='pwsh'),
    'linux-docker': ExecConfig(executor='docker', shell=None),
    'bash': ExecConfig(executor='shell')
}


def is_shell_executor(config: ExecConfig) -> bool:
    return True #config['executor'] == 'shell'


def _find_matching_tags(job: dict) -> List[str]:
    tags: List[str] = job['tags']
    matching_tags = [t for t in tags if t in DEFAULT_CONFIGS.keys()]
    return matching_tags


def suggest_configs(job: dict) -> List[ExecConfig]:
    tags = _find_matching_tags(job)
    matching_configs = [DEFAULT_CONFIGS[tag] for tag in tags]
    return matching_configs
