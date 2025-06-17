import socket
import threading

HOST = "127.0.0.1"
PORT = 12345
clients = []

def broadcast(msg, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(msg)
            except:
                clients.remove(client)

def handle_client(client_socket, addr):
    print(f"[+] {addr} connected.")
    clients.append(client_socket)
    while True:
        try:
            msg = client_socket.recv(1024)
            if not msg:
                break
            broadcast(msg, client_socket)
        except:
            break
    clients.remove(client_socket)
    client_socket.close()
    print(f"[-] {addr} disconnected.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("[*] Server is running...")
    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    start_server()