import socket
from jinja2 import Template


class Request:
    def __init__(self, request_text: str):
        try:
            self.interpret_request(request_text)

        except:
            raise MalformedRequest("Received malformed request")

    def interpret_request(self, request_text: str):
        self.raw = request_text

        request_split = request_text.split("\r\n")
        request_line = request_split[0]
        request_line_split = request_line.split(" ")
        
        self.method = request_line_split[0]
        self.uri = request_line_split[1]
        self.version = request_line_split[2]

        self.headers = {}
        for line in request_split:
            if ": " in line:
                line_split = line.split(": ", 1)
                self.headers[line_split[0]] = line_split[1]

        if self.method == "GET":
            self.body = None
        
        elif self.method == "POST":
            request_bigsplit = request_text.split("\r\n\r\n")
            if len(request_bigsplit) > 1:
                self.body = request_bigsplit[1].split("\r\n")[0]
            else:
                self.body = None

        elif self.method in ["HEAD", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]:
            raise RequestMethodNotSupported(f"The {self.method} method is not yet supported by this parser")
        
        else:
            raise UnknownRequestMethod(f"Unknown method {self.method}")


class RequestMethodNotSupported(Exception):
    """The method is not yet supported by this parser."""

class UnknownRequestMethod(Exception):
    """Unknown request method."""

class MalformedRequest(Exception):
    """The request was malformed."""


class Server:
    def __init__(self, *, host: str = "", port: int = 80):
        self.host = host
        self.port = port
        self.routes = {}

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            sock.bind((self.host, self.port))
            sock.listen(1000)
            print(f"Listening on port {self.port}")

            while True:
                conn, addr = sock.accept()

                with conn:
                    request_text = conn.recv(1024).decode()
                    print(f"\nNew request from {addr[0]}!")

                    request = Request(request_text)
                    response = self.respond(request)

                    conn.sendall(response.encode())

    def route(self, path):
        """Registers a route"""
        def register(func):
            self.routes[path] = func
            # return func # idk if i need this
        return register

    def respond(self, request: Request) -> str:
        if request.uri in self.routes:
            return self.routes[request.uri]()

        uri_split = request.uri.split("/")
        for route in self.routes:
            route_split = route.split("/")
            if len(route_split) != len(uri_split):
                continue
            for part_index in range(len(route_split)):
                if route_split[part_index] != uri_split[part_index]:
                    continue
                # idk if i will continue this project