import socket
import json
import os
import psutil

def send_command(command):
    HOST = '127.0.0.1'
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(command.encode())
        buf = b''
        while data := s.recv(1024):
            buf += data
    return buf


if __name__ == "__main__":
    while True:
        user_input = input("Введите команду (update для обновления информации, exit для выхода): ")

        if user_input.lower() == 'close':
            response = send_command(user_input.lower())
            print(response.decode())
            break
        else:
            response = send_command(user_input.lower())
            print(response.decode())

