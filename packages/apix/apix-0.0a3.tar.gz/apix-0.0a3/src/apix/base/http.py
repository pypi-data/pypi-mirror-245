import typing
import dataclasses
from enum import auto

from strenum import StrEnum


class HttpMethod(StrEnum):
    GET = auto()
    HEAD = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()
    CONNECT = auto()
    OPTIONS = auto()
    TRACE = auto()
    PATCH = auto()


@dataclasses.dataclass
class Request:
    method: str
    url: str
    content: typing.Optional[bytes] = None
    headers: typing.Dict[str, str] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class Response:
    status: int
    content: bytes
    headers: typing.Dict[str, str] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class PathInfo:
    method: str = HttpMethod.GET
    path: str = "/"
    type: typing.Type = bool
    path_params: typing.List[str] = dataclasses.field(default_factory=list)
    query_params: typing.List[str] = dataclasses.field(default_factory=list)
    
    def __post_init__(self):
        self.path_params = [
            param[1:-1]
            for param in self.path.split("/") 
            if param.startswith("{") and param.endswith("}")
        ]
