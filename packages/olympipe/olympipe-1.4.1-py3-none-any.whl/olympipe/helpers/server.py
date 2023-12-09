import json
import socket
from typing import Any, Dict, Generator, List, Tuple, Union

import dpkt  # type: ignore
import urllib.parse
from olympipe.types import OutPacket, RouteHandler


def server_generator(
    route_handlers: List[RouteHandler[OutPacket]],
    host: str = "localhost",
    port: int = 8000,
) -> Generator[Union[Exception, Tuple[socket.socket, OutPacket]], Any, None]:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.settimeout(0.2)
    server_socket.bind((host, port))
    server_socket.listen(5)

    while True:
        try:
            connection, _ = server_socket.accept()
            data = b""
            while True:
                chunk = connection.recv(1024)
                data += chunk
                try:
                    req = dpkt.http.Request(data)
                    break
                except Exception:
                    pass
            for method, path, func in route_handlers:
                if method == req.method and path == urllib.parse.urlparse(req.uri).path:
                    yield connection, func(json.loads(req.body))
                    break
        except Exception:
            yield Exception()


def send_json_response(connection: socket.socket, response: Dict[str, Any]) -> None:
    response_json = json.dumps(response)
    str_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: application/json\r\n"
        f"Content-Length: {len(response_json)}\r\n\r\n"
        f"{response_json}"
    )
    connection.sendall(str_response.encode("utf-8"))
    connection.close()
