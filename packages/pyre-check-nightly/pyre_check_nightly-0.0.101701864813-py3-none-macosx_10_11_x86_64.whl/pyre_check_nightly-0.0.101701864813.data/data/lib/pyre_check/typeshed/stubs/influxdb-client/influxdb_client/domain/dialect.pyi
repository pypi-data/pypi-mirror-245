from _typeshed import Incomplete

class Dialect:
    openapi_types: Incomplete
    attribute_map: Incomplete
    discriminator: Incomplete
    def __init__(
        self,
        header: bool = True,
        delimiter: str = ",",
        annotations: Incomplete | None = None,
        comment_prefix: str = "#",
        date_time_format: str = "RFC3339",
    ) -> None: ...
    @property
    def header(self): ...
    @header.setter
    def header(self, header) -> None: ...
    @property
    def delimiter(self): ...
    @delimiter.setter
    def delimiter(self, delimiter) -> None: ...
    @property
    def annotations(self): ...
    @annotations.setter
    def annotations(self, annotations) -> None: ...
    @property
    def comment_prefix(self): ...
    @comment_prefix.setter
    def comment_prefix(self, comment_prefix) -> None: ...
    @property
    def date_time_format(self): ...
    @date_time_format.setter
    def date_time_format(self, date_time_format) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
