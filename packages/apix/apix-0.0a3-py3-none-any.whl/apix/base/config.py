from typing import Optional
import dataclasses

from .proto import OP, ProtoHttp, ProtoSerializer, ProtoConfig


def default_serializer() -> ProtoSerializer:
    from ..serializer.default import Serializer

    return Serializer()


@dataclasses.dataclass
class ClientConfig(ProtoConfig[OP]):
    base_url: Optional[str] = None
    serializer: ProtoSerializer = dataclasses.field(
        default_factory=default_serializer)
    http: Optional[ProtoHttp[OP]] = None
