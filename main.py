import os
import json
import datetime
import socket
import psutil

class ProcessInfoCollector:
    def get_processes_info(self):
        processes = []
        if os.name == "nt":
            for proc in psutil.process_iter(['name']):
                processes.append({'name': proc.info['name']})
        elif os.name == "posix":
            for proc in os.popen('ps -A -o pid,ppid,comm'):
                if 'PID' not in proc:
                    parts = proc.split()
                    processes.append({'name': parts[2]})
        print(processes)
        return processes

    def save_to_file(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=1)

def handle_connection(conn, addr, collector):
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            command = data.decode()
            if command == 'update':
                processes_info = collector.get_processes_info()
                filename = f"./{datetime.datetime.now().strftime('%d-%m-%Y_%H_%M_%S')}.json"
                collector.save_to_file(processes_info, filename)

                with open(filename, 'r') as f:
                    data = f.read().encode()
                    conn.sendall(data)
                    #conn.close()
                #conn.sendall(b'Information updated successfully. File saved as ' + filename.encode())
            elif command == 'close':
                conn.sendall(b'Connection closed.')
                conn.close()
                break
            else:
                conn.sendall(b'Invalid command.')

if __name__ == "__main__":
    collector = ProcessInfoCollector()

    HOST = '127.0.0.1'
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Сервер запущен на {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            handle_connection(conn, addr, collector)
