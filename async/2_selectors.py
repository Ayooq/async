def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5001))
    server_socket.listen()

    print('Сервер запущен.')

    selector.register(server_socket, selectors.EVENT_READ, make_connection)


def make_connection(server_socket):
    client_socket, client_addr = server_socket.accept()
    print('Соединение установлено по адресу', client_addr)

    selector.register(client_socket, selectors.EVENT_READ, send_response)


def send_response(client_socket):
    request = client_socket.recv(4096)

    if not request:
        selector.unregister(client_socket)
        client_socket.close()
    else:
        response = '<h1>Hello, world!</h1>'.encode()
        client_socket.send(response)


def event_loop():
    while True:
        try:
            ready_to_read = selector.select()

            for key, _ in ready_to_read:
                callback = key.data
                callback(key.fileobj)

        except KeyboardInterrupt:
            print('Сервер завершил работу.')
            break


if __name__ == "__main__":
    import socket
    import selectors

    selector = selectors.DefaultSelector()

    server()
    event_loop()
