import abc
import collections
import sys
import typing
from _collections_abc import dict_items, dict_keys, dict_values
from _typeshed import IdentityFunction, Incomplete
from typing import (  # noqa: Y022,Y037,Y038,Y039
    IO as IO,
    TYPE_CHECKING as TYPE_CHECKING,
    AbstractSet as AbstractSet,
    Any as Any,
    AnyStr as AnyStr,
    AsyncContextManager as AsyncContextManager,
    AsyncGenerator as AsyncGenerator,
    AsyncIterable as AsyncIterable,
    AsyncIterator as AsyncIterator,
    Awaitable as Awaitable,
    BinaryIO as BinaryIO,
    Callable as Callable,
    ChainMap as ChainMap,
    ClassVar as ClassVar,
    Collection as Collection,
    Container as Container,
    ContextManager as ContextManager,
    Coroutine as Coroutine,
    Counter as Counter,
    DefaultDict as DefaultDict,
    Deque as Deque,
    Dict as Dict,
    ForwardRef as ForwardRef,
    FrozenSet as FrozenSet,
    Generator as Generator,
    Generic as Generic,
    Hashable as Hashable,
    ItemsView as ItemsView,
    Iterable as Iterable,
    Iterator as Iterator,
    KeysView as KeysView,
    List as List,
    Mapping as Mapping,
    MappingView as MappingView,
    Match as Match,
    MutableMapping as MutableMapping,
    MutableSequence as MutableSequence,
    MutableSet as MutableSet,
    NoReturn as NoReturn,
    Optional as Optional,
    Pattern as Pattern,
    Reversible as Reversible,
    Sequence as Sequence,
    Set as Set,
    Sized as Sized,
    SupportsAbs as SupportsAbs,
    SupportsBytes as SupportsBytes,
    SupportsComplex as SupportsComplex,
    SupportsFloat as SupportsFloat,
    SupportsInt as SupportsInt,
    SupportsRound as SupportsRound,
    Text as Text,
    TextIO as TextIO,
    Tuple as Tuple,
    Type as Type,
    Union as Union,
    ValuesView as ValuesView,
    _Alias,
    cast as cast,
    no_type_check as no_type_check,
    no_type_check_decorator as no_type_check_decorator,
    overload as overload,
    type_check_only,
)

if sys.version_info >= (3, 10):
    from types import UnionType
if sys.version_info >= (3, 9):
    from types import GenericAlias

__all__ = [
    "Any",
    "Buffer",
    "ClassVar",
    "Concatenate",
    "Final",
    "LiteralString",
    "ParamSpec",
    "ParamSpecArgs",
    "ParamSpecKwargs",
    "Self",
    "Type",
    "TypeVar",
    "TypeVarTuple",
    "Unpack",
    "Awaitable",
    "AsyncIterator",
    "AsyncIterable",
    "Coroutine",
    "AsyncGenerator",
    "AsyncContextManager",
    "ChainMap",
    "ContextManager",
    "Counter",
    "Deque",
    "DefaultDict",
    "NamedTuple",
    "OrderedDict",
    "TypedDict",
    "SupportsIndex",
    "SupportsAbs",
    "SupportsRound",
    "SupportsBytes",
    "SupportsComplex",
    "SupportsFloat",
    "SupportsInt",
    "Annotated",
    "assert_never",
    "assert_type",
    "dataclass_transform",
    "deprecated",
    "final",
    "IntVar",
    "is_typeddict",
    "Literal",
    "NewType",
    "overload",
    "override",
    "Protocol",
    "reveal_type",
    "runtime",
    "runtime_checkable",
    "Text",
    "TypeAlias",
    "TypeAliasType",
    "TypeGuard",
    "TYPE_CHECKING",
    "Never",
    "NoReturn",
    "Required",
    "NotRequired",
    "clear_overloads",
    "get_args",
    "get_origin",
    "get_original_bases",
    "get_overloads",
    "get_type_hints",
    "AbstractSet",
    "AnyStr",
    "BinaryIO",
    "Callable",
    "Collection",
    "Container",
    "Dict",
    "Doc",
    "ForwardRef",
    "FrozenSet",
    "Generator",
    "Generic",
    "Hashable",
    "IO",
    "ItemsView",
    "Iterable",
    "Iterator",
    "KeysView",
    "List",
    "Mapping",
    "MappingView",
    "Match",
    "MutableMapping",
    "MutableSequence",
    "MutableSet",
    "Optional",
    "Pattern",
    "Reversible",
    "Sequence",
    "Set",
    "Sized",
    "TextIO",
    "Tuple",
    "Union",
    "ValuesView",
    "cast",
    "get_protocol_members",
    "is_protocol",
    "no_type_check",
    "no_type_check_decorator",
]

_T = typing.TypeVar("_T")
_F = typing.TypeVar("_F", bound=Callable[..., Any])
_TC = typing.TypeVar("_TC", bound=type[object])

# unfortunately we have to duplicate this class definition from typing.pyi or we break pytype
class _SpecialForm:
    def __getitem__(self, parameters: Any) -> object: ...
    if sys.version_info >= (3, 10):
        def __or__(self, other: Any) -> _SpecialForm: ...
        def __ror__(self, other: Any) -> _SpecialForm: ...

# Do not import (and re-export) Protocol or runtime_checkable from
# typing module because type checkers need to be able to distinguish
# typing.Protocol and typing_extensions.Protocol so they can properly
# warn users about potential runtime exceptions when using typing.Protocol
# on older versions of Python.
Protocol: _SpecialForm

def runtime_checkable(cls: _TC) -> _TC: ...

# This alias for above is kept here for backwards compatibility.
runtime = runtime_checkable
Final: _SpecialForm

def final(f: _F) -> _F: ...

Literal: _SpecialForm

def IntVar(name: str) -> Any: ...  # returns a new TypeVar

# Internal mypy fallback type for all typed dicts (does not exist at runtime)
# N.B. Keep this mostly in sync with typing._TypedDict/mypy_extensions._TypedDict
@type_check_only
class _TypedDict(Mapping[str, object], metaclass=abc.ABCMeta):
    __required_keys__: ClassVar[frozenset[str]]
    __optional_keys__: ClassVar[frozenset[str]]
    __total__: ClassVar[bool]
    __orig_bases__: ClassVar[tuple[Any, ...]]
    def copy(self) -> Self: ...
    # Using Never so that only calls using mypy plugin hook that specialize the signature
    # can go through.
    def setdefault(self, k: Never, default: object) -> object: ...
    # Mypy plugin hook for 'pop' expects that 'default' has a type variable type.
    def pop(self, k: Never, default: _T = ...) -> object: ...  # pyright: ignore[reportInvalidTypeVarUse]
    def update(self: _T, __m: _T) -> None: ...
    def items(self) -> dict_items[str, object]: ...
    def keys(self) -> dict_keys[str, object]: ...
    def values(self) -> dict_values[str, object]: ...
    def __delitem__(self, k: Never) -> None: ...
    if sys.version_info >= (3, 9):
        @overload
        def __or__(self, __value: Self) -> Self: ...
        @overload
        def __or__(self, __value: dict[str, Any]) -> dict[str, object]: ...
        @overload
        def __ror__(self, __value: Self) -> Self: ...
        @overload
        def __ror__(self, __value: dict[str, Any]) -> dict[str, object]: ...
        # supposedly incompatible definitions of `__ior__` and `__or__`:
        def __ior__(self, __value: Self) -> Self: ...  # type: ignore[misc]

# TypedDict is a (non-subscriptable) special form.
TypedDict: object

OrderedDict = _Alias()

def get_type_hints(
    obj: Callable[..., Any],
    globalns: dict[str, Any] | None = None,
    localns: dict[str, Any] | None = None,
    include_extras: bool = False,
) -> dict[str, Any]: ...
def get_args(tp: Any) -> tuple[Any, ...]: ...

if sys.version_info >= (3, 10):
    @overload
    def get_origin(tp: UnionType) -> type[UnionType]: ...

if sys.version_info >= (3, 9):
    @overload
    def get_origin(tp: GenericAlias) -> type: ...

@overload
def get_origin(tp: ParamSpecArgs | ParamSpecKwargs) -> ParamSpec: ...
@overload
def get_origin(tp: Any) -> Any | None: ...

Annotated: _SpecialForm
_AnnotatedAlias: Any  # undocumented

@runtime_checkable
class SupportsIndex(Protocol, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __index__(self) -> int: ...

# New and changed things in 3.10
if sys.version_info >= (3, 10):
    from typing import (
        Concatenate as Concatenate,
        NewType as NewType,
        ParamSpecArgs as ParamSpecArgs,
        ParamSpecKwargs as ParamSpecKwargs,
        TypeAlias as TypeAlias,
        TypeGuard as TypeGuard,
        is_typeddict as is_typeddict,
    )
else:
    @final
    class ParamSpecArgs:
        @property
        def __origin__(self) -> ParamSpec: ...
        def __init__(self, origin: ParamSpec) -> None: ...

    @final
    class ParamSpecKwargs:
        @property
        def __origin__(self) -> ParamSpec: ...
        def __init__(self, origin: ParamSpec) -> None: ...

    Concatenate: _SpecialForm
    TypeAlias: _SpecialForm
    TypeGuard: _SpecialForm
    def is_typeddict(tp: object) -> bool: ...

    class NewType:
        def __init__(self, name: str, tp: Any) -> None: ...
        def __call__(self, __x: _T) -> _T: ...
        __supertype__: type

# New things in 3.11
# NamedTuples are not new, but the ability to create generic NamedTuples is new in 3.11
if sys.version_info >= (3, 11):
    from typing import (
        LiteralString as LiteralString,
        NamedTuple as NamedTuple,
        Never as Never,
        NotRequired as NotRequired,
        Required as Required,
        Self as Self,
        Unpack as Unpack,
        assert_never as assert_never,
        assert_type as assert_type,
        clear_overloads as clear_overloads,
        dataclass_transform as dataclass_transform,
        get_overloads as get_overloads,
        reveal_type as reveal_type,
    )
else:
    Self: _SpecialForm
    Never: _SpecialForm
    def reveal_type(__obj: _T) -> _T: ...
    def assert_never(__arg: Never) -> Never: ...
    def assert_type(__val: _T, __typ: Any) -> _T: ...
    def clear_overloads() -> None: ...
    def get_overloads(func: Callable[..., object]) -> Sequence[Callable[..., object]]: ...

    Required: _SpecialForm
    NotRequired: _SpecialForm
    LiteralString: _SpecialForm
    Unpack: _SpecialForm

    def dataclass_transform(
        *,
        eq_default: bool = True,
        order_default: bool = False,
        kw_only_default: bool = False,
        frozen_default: bool = False,
        field_specifiers: tuple[type[Any] | Callable[..., Any], ...] = (),
        **kwargs: object,
    ) -> IdentityFunction: ...

    class NamedTuple(tuple[Any, ...]):
        if sys.version_info < (3, 8):
            _field_types: ClassVar[collections.OrderedDict[str, type]]
        elif sys.version_info < (3, 9):
            _field_types: ClassVar[dict[str, type]]
        _field_defaults: ClassVar[dict[str, Any]]
        _fields: ClassVar[tuple[str, ...]]
        __orig_bases__: ClassVar[tuple[Any, ...]]
        @overload
        def __init__(self, typename: str, fields: Iterable[tuple[str, Any]] = ...) -> None: ...
        @overload
        def __init__(self, typename: str, fields: None = None, **kwargs: Any) -> None: ...
        @classmethod
        def _make(cls, iterable: Iterable[Any]) -> Self: ...
        if sys.version_info >= (3, 8):
            def _asdict(self) -> dict[str, Any]: ...
        else:
            def _asdict(self) -> collections.OrderedDict[str, Any]: ...

        def _replace(self, **kwargs: Any) -> Self: ...

# New things in 3.xx
# The `default` parameter was added to TypeVar, ParamSpec, and TypeVarTuple (PEP 696)
# The `infer_variance` parameter was added to TypeVar in 3.12 (PEP 695)
# typing_extensions.override (PEP 698)
@final
class TypeVar:
    @property
    def __name__(self) -> str: ...
    @property
    def __bound__(self) -> Any | None: ...
    @property
    def __constraints__(self) -> tuple[Any, ...]: ...
    @property
    def __covariant__(self) -> bool: ...
    @property
    def __contravariant__(self) -> bool: ...
    @property
    def __infer_variance__(self) -> bool: ...
    @property
    def __default__(self) -> Any | None: ...
    def __init__(
        self,
        name: str,
        *constraints: Any,
        bound: Any | None = None,
        covariant: bool = False,
        contravariant: bool = False,
        default: Any | None = None,
        infer_variance: bool = False,
    ) -> None: ...
    if sys.version_info >= (3, 10):
        def __or__(self, right: Any) -> _SpecialForm: ...
        def __ror__(self, left: Any) -> _SpecialForm: ...
    if sys.version_info >= (3, 11):
        def __typing_subst__(self, arg: Incomplete) -> Incomplete: ...

@final
class ParamSpec:
    @property
    def __name__(self) -> str: ...
    @property
    def __bound__(self) -> Any | None: ...
    @property
    def __covariant__(self) -> bool: ...
    @property
    def __contravariant__(self) -> bool: ...
    @property
    def __infer_variance__(self) -> bool: ...
    @property
    def __default__(self) -> Any | None: ...
    def __init__(
        self,
        name: str,
        *,
        bound: None | type[Any] | str = None,
        contravariant: bool = False,
        covariant: bool = False,
        default: type[Any] | str | None = None,
    ) -> None: ...
    @property
    def args(self) -> ParamSpecArgs: ...
    @property
    def kwargs(self) -> ParamSpecKwargs: ...

@final
class TypeVarTuple:
    @property
    def __name__(self) -> str: ...
    @property
    def __default__(self) -> Any | None: ...
    def __init__(self, name: str, *, default: Any | None = None) -> None: ...
    def __iter__(self) -> Any: ...  # Unpack[Self]

def deprecated(__msg: str, *, category: type[Warning] | None = ..., stacklevel: int = 1) -> Callable[[_T], _T]: ...

if sys.version_info >= (3, 12):
    from collections.abc import Buffer as Buffer
    from types import get_original_bases as get_original_bases
    from typing import TypeAliasType as TypeAliasType, override as override
else:
    def override(__arg: _F) -> _F: ...
    def get_original_bases(__cls: type) -> tuple[Any, ...]: ...
    @final
    class TypeAliasType:
        def __init__(
            self, name: str, value: Any, *, type_params: tuple[TypeVar | ParamSpec | TypeVarTuple, ...] = ()
        ) -> None: ...
        @property
        def __value__(self) -> Any: ...
        @property
        def __type_params__(self) -> tuple[TypeVar | ParamSpec | TypeVarTuple, ...]: ...
        @property
        def __parameters__(self) -> tuple[Any, ...]: ...
        @property
        def __name__(self) -> str: ...
        # It's writable on types, but not on instances of TypeAliasType.
        @property
        def __module__(self) -> str | None: ...  # type: ignore[override]
        def __getitem__(self, parameters: Any) -> Any: ...
        if sys.version_info >= (3, 10):
            def __or__(self, right: Any) -> _SpecialForm: ...
            def __ror__(self, left: Any) -> _SpecialForm: ...

    @runtime_checkable
    class Buffer(Protocol):
        # Not actually a Protocol at runtime; see
        # https://github.com/python/typeshed/issues/10224 for why we're defining it this way
        def __buffer__(self, __flags: int) -> memoryview: ...

if sys.version_info >= (3, 13):
    from typing import get_protocol_members as get_protocol_members, is_protocol as is_protocol
else:
    def is_protocol(__tp: type) -> bool: ...
    def get_protocol_members(__tp: type) -> frozenset[str]: ...

class Doc:
    documentation: str
    def __init__(self, __documentation: str) -> None: ...
    def __hash__(self) -> int: ...
    def __eq__(self, other: object) -> bool: ...
