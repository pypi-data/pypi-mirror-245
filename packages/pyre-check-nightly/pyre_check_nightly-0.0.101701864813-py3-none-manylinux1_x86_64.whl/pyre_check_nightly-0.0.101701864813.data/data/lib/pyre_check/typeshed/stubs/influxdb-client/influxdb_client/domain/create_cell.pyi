from _typeshed import Incomplete

class CreateCell:
    openapi_types: Incomplete
    attribute_map: Incomplete
    discriminator: Incomplete
    def __init__(
        self,
        name: Incomplete | None = None,
        x: Incomplete | None = None,
        y: Incomplete | None = None,
        w: Incomplete | None = None,
        h: Incomplete | None = None,
        using_view: Incomplete | None = None,
    ) -> None: ...
    @property
    def name(self): ...
    @name.setter
    def name(self, name) -> None: ...
    @property
    def x(self): ...
    @x.setter
    def x(self, x) -> None: ...
    @property
    def y(self): ...
    @y.setter
    def y(self, y) -> None: ...
    @property
    def w(self): ...
    @w.setter
    def w(self, w) -> None: ...
    @property
    def h(self): ...
    @h.setter
    def h(self, h) -> None: ...
    @property
    def using_view(self): ...
    @using_view.setter
    def using_view(self, using_view) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
