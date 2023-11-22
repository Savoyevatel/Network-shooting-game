import socket
import threading

HOST = '192.168.178.129'
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Server initialized on {HOST}:{PORT}")

def handle_client(conn, addr, clients):
    print(f"connection from {addr}")

    for client in clients:
        client.send(f"Player {addr} joined the game".encode())

    clients.append(conn)

    try:
        while True:
            data = conn.recv(1024).decode()
            print(data)
            if not data:
                break

            # Broadcast the received data to all clients
            for client in clients:
                if client != conn:
                    client.send(data.encode())


    except Exception as e:
        print(f"Error: {e}")
    finally:
        clients.remove(conn)
        conn.close()
        print(f"Connection from {addr} closed")


clients = []
while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr, clients))
    thread.start()
