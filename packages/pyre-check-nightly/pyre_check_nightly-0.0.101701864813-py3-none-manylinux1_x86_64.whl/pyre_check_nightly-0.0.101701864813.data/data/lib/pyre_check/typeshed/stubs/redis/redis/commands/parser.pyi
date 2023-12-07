from redis.client import AbstractRedis
from redis.typing import EncodableT

class CommandsParser:
    commands: dict[str, str]
    def __init__(self, redis_connection: AbstractRedis) -> None: ...
    def initialize(self, r: AbstractRedis) -> None: ...
    def get_keys(self, redis_conn: AbstractRedis, *args: EncodableT) -> list[EncodableT] | None: ...
