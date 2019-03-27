def make_connection(server_socket):
    client_socket, client_addr = server_socket.accept()
    print('Соединение установлено по адресу', client_addr)

    to_monitor.append(client_socket)


def send_response(client_socket):
    request = client_socket.recv(4096)

    if not request:
        client_socket.close()
        to_monitor.remove(client_socket)
    else:
        response = '<h1>Hello, world!</h1>'.encode()
        client_socket.send(response)


def event_loop():
    while True:
        try:
            ready_to_read, _, _ = select(to_monitor, [], [])

            for sock in ready_to_read:
                if sock is server_socket:
                    make_connection(sock)
                else:
                    send_response(sock)

        except KeyboardInterrupt:
            print('Сервер завершил работу.')
            break


if __name__ == "__main__":
    import socket
    from select import select

    to_monitor = []

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5001))
    server_socket.listen()

    print('Сервер запущен.')

    to_monitor.append(server_socket)
    event_loop()
