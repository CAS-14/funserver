import socket

# https://www.codementor.io/@joaojonesventura/building-a-basic-http-server-from-scratch-in-python-1cedkg0842

SERVER_HOST = ""
SERVER_PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.bind((SERVER_HOST, SERVER_PORT))
    sock.listen(1000)
    print(f"Listening on port {SERVER_PORT}")

    while True:
        conn, addr = sock.accept()

        with conn:
            request_text = conn.recv(1024).decode()
            print(f"\nNew request from {addr[0]}!")
            
            request = request_text.split("\n\r")
            for i in range(len(request)):
                if i == 0:
                    continue

                request[i] = request[i].split(": ")

            print(request)

            response = "HTTP/1.0 200 OK\n\nHello World"
            conn.sendall(response.encode())
            conn.close()