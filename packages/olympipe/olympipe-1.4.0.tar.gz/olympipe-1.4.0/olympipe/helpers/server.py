import json
import socket
from typing import Any, Dict, List

import dpkt  # type: ignore
import urllib.parse
from olympipe.types import OutPacket, RouteHandler


def server_generator(
    route_handlers: List[RouteHandler[OutPacket]],
    host: str = "localhost",
    port: int = 8000,
):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    while True:
        connection, address = server_socket.accept()

        try:
            data = b""  # Initialisez data avec une chaîne vide
            while (
                b"\r\n\r\n" not in data
            ):  # Continuez à lire jusqu'à la fin de l'en-tête
                chunk = connection.recv(1024)
                if not chunk:
                    break
                data += chunk

            req = dpkt.http.Request(data)
            for method, path, func in route_handlers:
                if method == req.method and path == urllib.parse.urlparse(req.uri).path:
                    yield connection, func(json.loads(req.body))
                    break
        except Exception as e:
            print(e, address)


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
