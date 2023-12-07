from _typeshed import Incomplete
from typing import Any

from google.cloud.ndb import _options

class PropertyOrder:
    name: Any
    reverse: Any
    def __init__(self, name, reverse: bool = ...) -> None: ...
    def __neg__(self): ...

class RepeatedStructuredPropertyPredicate:
    name: Any
    match_keys: Any
    match_values: Any
    def __init__(self, name, match_keys, entity_pb) -> None: ...
    def __call__(self, entity_pb): ...

class ParameterizedThing:
    def __eq__(self, other): ...
    def __ne__(self, other): ...

class Parameter(ParameterizedThing):
    def __init__(self, key) -> None: ...
    def __eq__(self, other): ...
    @property
    def key(self): ...
    def resolve(self, bindings, used): ...

class ParameterizedFunction(ParameterizedThing):
    func: Any
    values: Any
    def __init__(self, func, values) -> None: ...
    def __eq__(self, other): ...
    def is_parameterized(self): ...
    def resolve(self, bindings, used): ...

class Node:
    def __new__(cls): ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __le__(self, unused_other): ...
    def __lt__(self, unused_other): ...
    def __ge__(self, unused_other): ...
    def __gt__(self, unused_other): ...
    def resolve(self, bindings, used): ...

class FalseNode(Node):
    def __eq__(self, other): ...

class ParameterNode(Node):
    def __new__(cls, prop, op, param): ...
    def __getnewargs__(self): ...
    def __eq__(self, other): ...
    def resolve(self, bindings, used): ...

class FilterNode(Node):
    def __new__(cls, name, opsymbol, value): ...
    def __getnewargs__(self): ...
    def __eq__(self, other): ...

class PostFilterNode(Node):
    def __new__(cls, predicate): ...
    def __getnewargs__(self): ...
    def __eq__(self, other): ...

class _BooleanClauses:
    name: Any
    combine_or: Any
    or_parts: Any
    def __init__(self, name, combine_or) -> None: ...
    def add_node(self, node) -> None: ...

class ConjunctionNode(Node):
    def __new__(cls, *nodes): ...
    def __getnewargs__(self): ...
    def __iter__(self): ...
    def __eq__(self, other): ...
    def resolve(self, bindings, used): ...

class DisjunctionNode(Node):
    def __new__(cls, *nodes): ...
    def __getnewargs__(self): ...
    def __iter__(self): ...
    def __eq__(self, other): ...
    def resolve(self, bindings, used): ...

AND = ConjunctionNode
OR = DisjunctionNode

class QueryOptions(_options.ReadOptions):
    project: Any
    namespace: Any
    database: str | None
    def __init__(self, config: Incomplete | None = ..., context: Incomplete | None = ..., **kwargs) -> None: ...

class Query:
    default_options: Any
    kind: Any
    ancestor: Any
    filters: Any
    order_by: Any
    project: Any
    namespace: Any
    limit: Any
    offset: Any
    keys_only: Any
    projection: Any
    distinct_on: Any
    database: str | None
    def __init__(
        self,
        kind: Incomplete | None = ...,
        filters: Incomplete | None = ...,
        ancestor: Incomplete | None = ...,
        order_by: Incomplete | None = ...,
        orders: Incomplete | None = ...,
        project: Incomplete | None = ...,
        app: Incomplete | None = ...,
        namespace: Incomplete | None = ...,
        projection: Incomplete | None = ...,
        distinct_on: Incomplete | None = ...,
        group_by: Incomplete | None = ...,
        limit: Incomplete | None = ...,
        offset: Incomplete | None = ...,
        keys_only: Incomplete | None = ...,
        default_options: Incomplete | None = ...,
    ) -> None: ...
    @property
    def is_distinct(self): ...
    def filter(self, *filters): ...
    def order(self, *props): ...
    def analyze(self): ...
    def bind(self, *positional, **keyword): ...
    def fetch(self, limit: Incomplete | None = ..., **kwargs): ...
    def fetch_async(self, limit: Incomplete | None = ..., **kwargs): ...
    def run_to_queue(self, queue, conn, options: Incomplete | None = ..., dsquery: Incomplete | None = ...) -> None: ...
    def iter(self, **kwargs): ...
    __iter__: Any
    def map(self, callback, **kwargs): ...
    def map_async(self, callback, **kwargs) -> None: ...
    def get(self, **kwargs): ...
    def get_async(self, **kwargs) -> None: ...
    def count(self, limit: Incomplete | None = ..., **kwargs): ...
    def count_async(self, limit: Incomplete | None = ..., **kwargs): ...
    def fetch_page(self, page_size, **kwargs): ...
    def fetch_page_async(self, page_size, **kwargs) -> None: ...

def gql(query_string: str, *args: Any, **kwds: Any) -> Query: ...
