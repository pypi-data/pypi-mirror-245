"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import sys

import google.protobuf.descriptor
import google.protobuf.message

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class Metadata(google.protobuf.message.Message):
    """next: 2"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    name: builtins.bytes
    def __init__(
        self,
        *,
        name: builtins.bytes | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["name", b"name"]) -> None: ...

global___Metadata = Metadata
