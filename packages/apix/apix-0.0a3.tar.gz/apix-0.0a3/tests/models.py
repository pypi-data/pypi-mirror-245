from apix import Path, Schema, PathInfo


class Data(Schema):
    key: str
    value: str


class GetData(Path[Data]):
    __info__ = PathInfo("GET", "/data", Data)

    key: str


class PostData(Path[bool]):
    __info__ = PathInfo("POST", "/data", bool)

    key: str
    value: str


class GetDataByPath(Path[Data]):
    __info__ = PathInfo("GET", "/data/{key}", Data)

    key: str
