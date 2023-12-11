from typing import Optional, ClassVar

from .proto import ProtoClient, OP, ProtoConfig, ProtoHttp, ProtoPath, T, ProtoSerializer
from .http import Response, Request
from .config import ClientConfig


class BaseClient(ProtoClient[OP]):
    BASE_URL: ClassVar[str] = "https://api.example.com"

    def __init__(
            self, 
            config: Optional[ProtoConfig] = None
    ) -> None:
        self._http: Optional[ProtoHttp[OP]]
        self._config = config or ClientConfig()
        if self._config.http is None:
            self._http = self.default_http()
        else:
            self._http = None
        if self._config.base_url is None:
            self._base_url = self.BASE_URL
        else:
            self._base_url = self.config.base_url

    @property
    def config(self) -> ProtoConfig:
        return self._config

    @property
    def http(self) -> ProtoHttp[OP]:
        if _http := self._http or self.config.http:
            return _http
        raise RuntimeError("Client is not initialized http")
    
    @property
    def serializer(self) -> ProtoSerializer:
        return self.config.serializer

    def build_url(self, path: ProtoPath[T]) -> str:
        return self._base_url + path.__info__.path
    
    def _build_request(self, path: ProtoPath[T], **kwargs) -> Request:
        return path.build_request(self)

    def _build_result(self, response: Response, path: ProtoPath[T]) -> T:
        return path.build_result(response, self)
