from typing_extensions import Final

def lxml_available() -> bool: ...
def lxml_env_set() -> bool: ...

LXML: Final[bool]

def defusedxml_available() -> bool: ...
def defusedxml_env_set() -> bool: ...

DEFUSEDXML: Final[bool]
