import json
import socket
import urllib.parse
from typing import Any, Dict, Generator, List, Tuple, Union, cast

import dpkt  # type: ignore

from olympipe.types import OutPacket, RouteHandler


def server_generator(
    route_handlers: List[RouteHandler[OutPacket]],
    host: str = "localhost",
    port: int = 8000,
    debug: bool = False,
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
            request_path: str = ""
            body = {}
            while True:
                chunk = connection.recv(1024)
                data += chunk
                try:
                    req: Any = dpkt.http.Request(data)
                    request_path = cast(str, urllib.parse.urlparse(req.uri).path)
                    body = json.loads(req.body)
                    break
                except dpkt.NeedData:
                    pass

            found = False
            for method, path, func in route_handlers:
                if method == req.method and path == request_path:
                    if debug:
                        print(f"Handling {req.method} {request_path} with {func}")
                    yield connection, func(body)
                    found = True
                    break
            if debug and not found:
                print(f"No route handler for {req.method} {request_path}")
        except StopIteration:
            send_json_response(connection, {"status": "killed"})  # type: ignore
            connection.close()  # type: ignore
            return
        except socket.timeout:
            yield Exception()
        except Exception as e:
            print(e)
            send_json_response(connection, {"error": f"{e}"}, status=500, reason="Internal Server Error")  # type: ignore
            connection.close()  # type: ignore
            return


def send_json_response(
    connection: socket.socket,
    response: Dict[str, Any],
    status: int = 200,
    reason: str = "OK",
) -> None:
    response_json = json.dumps(response)
    str_response = (
        f"HTTP/1.1 {status} {reason}\r\n"
        "Content-Type: application/json\r\n"
        f"Content-Length: {len(response_json)}\r\n\r\n"
        f"{response_json}"
    )
    connection.sendall(str_response.encode("utf-8"))
    connection.close()
