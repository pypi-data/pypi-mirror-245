from apix import Response

from .models import Data, GetData, PostData, GetDataByPath

def test_data(client):
    assert client.serializer.to_json(Data("foo", "fooson")) == b'{"key":"foo","value":"fooson"}'

def test_get_data(client):
    assert client.serializer.to_json(GetData("foo")) == b'{"key":"foo"}'

def test_post_data(client):
    assert client.serializer.to_json(PostData("foo", "bar")) == b'{"key":"foo","value":"bar"}'

def test_decode_data(client):
    assert client.serializer.from_json(b'{"key":"foo","value":"fooson"}', Data) == Data("foo", "fooson")
 
def test_build_request(client):
    request = GetData("foo").build_request(client)
    assert request.method == "GET"
    assert request.url == "https://api.example.com/data?key=foo"

def test_build_result(client):
    response = Response(200, b'{"key":"foo","value":"fooson"}')
    assert GetData("foo").build_result(response, client) == Data("foo", "fooson")

def test_get_data_by_path(client):
    request = GetDataByPath("foo").build_request(client)
    assert request.url == "https://api.example.com/data/foo"
