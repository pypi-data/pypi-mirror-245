from _typeshed import Incomplete
from abc import ABC, abstractmethod

from .syntax import PDFObject

class Action(ABC):
    next: PDFObject | str | None
    def __init__(self, next_action: PDFObject | str | None = None) -> None: ...
    @abstractmethod
    def serialize(self) -> str: ...

class URIAction(Action):
    uri: str
    def __init__(self, uri: str, next_action: PDFObject | str | None = None) -> None: ...
    def serialize(self) -> str: ...

class NamedAction(Action):
    action_name: str
    def __init__(self, action_name: str, next_action: PDFObject | str | None = None) -> None: ...
    def serialize(self) -> str: ...

class GoToAction(Action):
    dest: Incomplete
    def __init__(self, dest, next_action: PDFObject | str | None = None) -> None: ...
    def serialize(self) -> str: ...

class GoToRemoteAction(Action):
    file: str
    dest: Incomplete
    def __init__(self, file: str, dest, next_action: PDFObject | str | None = None) -> None: ...
    def serialize(self) -> str: ...

class LaunchAction(Action):
    file: str
    def __init__(self, file: str, next_action: PDFObject | str | None = None) -> None: ...
    def serialize(self) -> str: ...
