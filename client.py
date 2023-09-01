import socket
import threading

# Создаем сокет клиента
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Указываем адрес и порт сервера для подключения
server_address = ('localhost', 55555)

# Подключаемся к серверу
client_socket.connect(server_address)
print("Подключено к серверу. Можете начать общение.")

# Функция для отправки сообщений серверу
def send_message():
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))

# Функция для приема сообщений от сервера
def receive_message():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except Exception as e:
            print(f"Ошибка: {e}")
            client_socket.close()
            break

# Создаем и запускаем отдельные потоки для отправки и приема сообщений
send_thread = threading.Thread(target=send_message)
receive_thread = threading.Thread(target=receive_message)

send_thread.start()
receive_thread.start()
