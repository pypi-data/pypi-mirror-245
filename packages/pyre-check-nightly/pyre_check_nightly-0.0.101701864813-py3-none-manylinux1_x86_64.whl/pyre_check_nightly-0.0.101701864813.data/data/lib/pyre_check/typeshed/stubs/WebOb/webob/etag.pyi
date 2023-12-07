from collections.abc import Collection
from datetime import datetime
from typing import Any, overload
from typing_extensions import TypeAlias

from webob.response import Response

_ETag: TypeAlias = _AnyETag | _NoETag | ETagMatcher

class _ETagProperty:
    @overload
    def __get__(self, __obj: None, __type: type | None = ...) -> property: ...
    @overload
    def __get__(self, __obj: Any, __type: type | None = ...) -> _ETag: ...
    @overload
    def __set__(self, __obj: Any, __value: str | None) -> None: ...
    @overload
    def __set__(self, __obj: Any, __value: _ETag) -> None: ...
    def __delete__(self, __obj: Any) -> None: ...

def etag_property(key: str, default: _ETag, rfc_section: str, strong: bool = True) -> _ETagProperty: ...

class _AnyETag:
    def __bool__(self) -> bool: ...
    def __contains__(self, other: str) -> bool: ...

AnyETag: _AnyETag

class _NoETag:
    def __bool__(self) -> bool: ...
    def __contains__(self, other: str) -> bool: ...

NoETag: _NoETag

class ETagMatcher:
    etags: Collection[str]
    def __init__(self, etags: Collection[str]) -> None: ...
    def __contains__(self, other: str) -> bool: ...
    @classmethod
    def parse(cls, value: str, strong: bool = True) -> ETagMatcher | _AnyETag: ...

class IfRange:
    etag: _ETag
    def __init__(self, etag: _ETag) -> None: ...
    @classmethod
    def parse(cls, value: str) -> IfRange | IfRangeDate: ...
    def __contains__(self, resp: Response) -> bool: ...
    def __bool__(self) -> bool: ...

class IfRangeDate:
    date: datetime
    def __init__(self, date: datetime) -> None: ...
    def __contains__(self, resp: Response) -> bool: ...
