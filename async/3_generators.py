def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5001))
    server_socket.listen()

    print('Сервер запущен.')

    while True:
        yield ('read', server_socket)
        client_socket, client_addr = server_socket.accept()

        print('Соединение установлено по адресу', client_addr)

        tasks.append(client(client_socket))


def client(client_socket):
    while True:
        yield ('read', client_socket)
        request = client_socket.recv(4096)

        if not request:
            break

        response = '<h1>Hello, world!</h1>'.encode()

        yield ('write', client_socket)
        client_socket.send(response)

    client_socket.close()


def event_loop():
    while any([tasks, to_read, to_write]):
        try:
            while not tasks:
                ready_to_read, ready_to_write, _ = select(
                    to_read, to_write, [])

                for sock in ready_to_read:
                    tasks.append(to_read.pop(sock))

                for sock in ready_to_write:
                    tasks.append(to_write.pop(sock))

            try:
                task = tasks.pop(0)
                io_determ, sock = next(task)

                if io_determ == 'read':
                    to_read[sock] = task
                elif io_determ == 'write':
                    to_write[sock] = task

            except StopIteration:
                print('Обмен данными с клиентом прекращён.')

        except KeyboardInterrupt:
            print('Сервер завершил работу.')
            break


if __name__ == "__main__":
    import socket
    from select import select

    tasks = []
    to_read, to_write = {}, {}

    tasks.append(server())
    event_loop()
