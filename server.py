import socket
import threading

# Создаем сокет сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Указываем адрес и порт сервера
server_address = ('localhost', 55555)

# Привязываем сервер к указанному адресу и порту
server_socket.bind(server_address)

# Слушаем подключения (максимальное количество клиентов - 5)
server_socket.listen(5)
print("Сервер запущен. Ожидание подключений...")

# Список подключенных клиентов
clients = []

# Функция для обработки сообщений от клиентов
def handle_client(client_socket):
    while True:
        try:
            # Получаем сообщение от клиента
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                # Если сообщение пустое, клиент отключился
                print(f"Клиент {client_socket.getpeername()} отключился.")
                clients.remove(client_socket)
                client_socket.close()
                break
            else:
                # Отправляем сообщение всем подключенным клиентам
                for client in clients:
                    if client != client_socket:
                        client.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Ошибка: {e}")
            clients.remove(client_socket)
            client_socket.close()
            break

while True:
    # Принимаем подключение клиента
    client_socket, client_address = server_socket.accept()
    print(f"Подключен клиент {client_address}")
    
    # Добавляем клиента в список
    clients.append(client_socket)
    
    # Создаем и запускаем отдельный поток для обработки клиента
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
