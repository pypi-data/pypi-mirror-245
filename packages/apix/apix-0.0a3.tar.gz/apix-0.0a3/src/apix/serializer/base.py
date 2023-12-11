from ..base import ProtoClient, T, ProtoPath, Response, Request
from urllib.parse import urlencode
from ..base.http import HttpMethod


def build_request(path: ProtoPath[T], client: ProtoClient) -> Request:
    """
    Build from Path Request object
    """
    info = path.__info__
    content = None
    headers = {}
    params = {}

    url = client.build_url(path)

    if HttpMethod.GET == info.method or info.path_params:
        params = client.config.serializer.to_builtins(path)

    if info.path_params:
        url = url.format(**{k: v for k, v in params.items() if k in info.path_params})
        params = {k: v for k, v in params.items() if k not in info.path_params}

    if HttpMethod.GET == info.method and params:
        url = f"{url}?{urlencode(params)}"
    else:
        content = client.config.serializer.to_json(params if info.path_params else path)
        headers = {"Content-Type": "application/json"}

    return Request(
        method=info.method,
        url=url,
        headers=headers,
        content=content,
    )


def build_result(path: ProtoPath[T], response: Response, client: ProtoClient) -> T:
    return client.config.serializer.from_json(response.content, path.__info__.type)
