import typing
from .base import (
    Request,
    Response,
    PathInfo,
    OP,
    T,
    Async,
    Sync,
    ProtoSerializer,
    ProtoSchema,
    ProtoPath,
    ProtoHttp,
    ProtoConfig,
    ProtoClient,
    ClientConfig,
    BaseClient,
    HttpMethod
)
from .serializer import (
    Serializer,
    Schema,
    Path
)

__all__ = [
    "Request",
    "Response",
    "PathInfo",
    "OP",
    "T",
    "Async",
    "Sync",
    "ProtoSerializer",
    "ProtoSchema",
    "ProtoPath",
    "ProtoHttp",
    "ProtoConfig",
    "ProtoClient",
    "ClientConfig",
    "BaseClient",
    "Serializer",
    "Schema",
    "Path",
    "HttpMethod",
    "BadRequest",
    "Unauthorized",
    "PaymentRequired",
    "Forbidden",
    "NotFound",
    "MethodNotAllowed",
    "NotAcceptable",
    "ProxyAuthenticationRequired",
    "RequestTimeout",
    "Conflict",
    "Gone",
    "LengthRequired",
    "PreconditionFailed",
    "RequestEntityTooLarge",
    "RequestUriTooLong",
    "UnsupportedMediaType",
    "RequestedRangeNotSatisfiable",
    "ExpectationFailed",
    "MisdirectedRequest",
    "UnprocessableEntity",
    "Locked",
    "FailedDependency",
    "UpgradeRequired",
    "PreconditionRequired",
    "TooManyRequests",
    "RequestHeaderFieldsTooLarge",
    "UnavailableForLegalReasons",
    "InternalServerError",
    "NotImplemented",
    "BadGateway",
    "ServiceUnavailable",
    "GatewayTimeout",
    "HttpVersionNotSupported",
    "VariantAlsoNegotiates",
    "InsufficientStorage",
    "LoopDetected",
    "NotExtended",
    "NetworkAuthenticationRequired",
]


class HTTPException(Exception):
    exceptions: typing.ClassVar[typing.Dict[int, typing.Type["HTTPException"]]] = {}

    def __init_subclass__(cls, status: int) -> None:
        cls.exceptions[status] = cls


class BadRequest(HTTPException, status=400): ...
class Unauthorized(HTTPException, status=401): ...
class PaymentRequired(HTTPException, status=402): ...
class Forbidden(HTTPException, status=403): ...
class NotFound(HTTPException, status=404): ...
class MethodNotAllowed(HTTPException, status=405): ...
class NotAcceptable(HTTPException, status=406): ...
class ProxyAuthenticationRequired(HTTPException, status=407): ...
class RequestTimeout(HTTPException, status=408): ...
class Conflict(HTTPException, status=409): ...
class Gone(HTTPException, status=410): ...
class LengthRequired(HTTPException, status=411): ...
class PreconditionFailed(HTTPException, status=412): ...
class RequestEntityTooLarge(HTTPException, status=413): ...
class RequestUriTooLong(HTTPException, status=414): ...
class UnsupportedMediaType(HTTPException, status=415): ...
class RequestedRangeNotSatisfiable(HTTPException, status=416): ...
class ExpectationFailed(HTTPException, status=417): ...
class MisdirectedRequest(HTTPException, status=421): ...
class UnprocessableEntity(HTTPException, status=422): ...
class Locked(HTTPException, status=423): ...
class FailedDependency(HTTPException, status=424): ...
class UpgradeRequired(HTTPException, status=426): ...
class PreconditionRequired(HTTPException, status=428): ...
class TooManyRequests(HTTPException, status=429): ...
class RequestHeaderFieldsTooLarge(HTTPException, status=431): ...
class UnavailableForLegalReasons(HTTPException, status=451): ...
class InternalServerError(HTTPException, status=500): ...
class NotImplemented(HTTPException, status=501): ...
class BadGateway(HTTPException, status=502): ...
class ServiceUnavailable(HTTPException, status=503): ...
class GatewayTimeout(HTTPException, status=504): ...
class HttpVersionNotSupported(HTTPException, status=505): ...
class VariantAlsoNegotiates(HTTPException, status=506): ...
class InsufficientStorage(HTTPException, status=507): ...
class LoopDetected(HTTPException, status=508): ...
class NotExtended(HTTPException, status=510): ...
class NetworkAuthenticationRequired(HTTPException, status=511): ...
