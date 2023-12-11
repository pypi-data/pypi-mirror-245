from __future__ import annotations

from typing import overload, TypeVar, Type, Any, Protocol, ClassVar, Optional

from .http import PathInfo, Request, Response


class Operation: ...
class Sync(Operation): ...
class Async(Operation): ...

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
OP = TypeVar("OP")
OP_co = TypeVar("OP_co", covariant=True)


class ProtoSerializer(Protocol):
    def to_json(self, obj: Any) -> bytes: ...
    def from_json(self, data: bytes, type: Type[T]) -> T: ...
    def to_builtins(self, obj: Any) -> Any: ...
    def to_type(self, obj: Any, type: Type[T]) -> T: ...


class ProtoSchema(Protocol): ...


class ProtoPath(Protocol[T_co]):
    __info__: ClassVar[PathInfo]
    
    def build_request(self, client: ProtoClient) -> Request: ...
    def build_result(self, response: Response, client: ProtoClient) -> T_co: ...


class ProtoHttp(Protocol[OP_co]):
    @overload
    def fetch(self: ProtoHttp[Sync], request: Request) -> Response: ...

    @overload
    async def fetch(self: ProtoHttp[Async], request: Request) -> Response: ...

    @overload
    def close(self: ProtoHttp[Sync]) -> None: ...

    @overload
    async def close(self: ProtoHttp[Async]) -> None: ...


class ProtoConfig(Protocol[OP]):
    serializer: ProtoSerializer
    base_url: Optional[str]
    http: Optional[ProtoHttp[OP]]


class ProtoClient(Protocol[OP]):
    @overload
    def __call__(self: ProtoClient[Sync], path: ProtoPath[T], **kwargs) -> T: ...

    @overload
    async def __call__(self: ProtoClient[Async], path: ProtoPath[T], **kwargs) -> T: ...

    @property
    def config(self) -> ProtoConfig[OP]: ...

    @property
    def http(self) -> ProtoHttp: ...

    @staticmethod
    def default_http() -> ProtoHttp[OP]: ...

    def build_url(self, path: ProtoPath[T]) -> str: ...
