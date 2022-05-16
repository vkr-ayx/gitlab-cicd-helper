from typing import TypedDict, Optional, Dict


class ExecConfig(TypedDict):
    executor: str
    shell: Optional[str]
    env: Dict[str, str]