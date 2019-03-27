import socket


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5001))
server_socket.listen()

print('Сервер запущен.')


while True:
    try:
        client_socket, client_addr = server_socket.accept()
        print('Соединение установлено по адресу', client_addr)

        while True:
            request = client_socket.recv(4096)

            if not request:
                break

            response = '<h1>Hello, world!</h1>'.encode()
            client_socket.send(response)

        client_socket.close()

    except KeyboardInterrupt:
        print('Сервер завершил работу.')
        break
