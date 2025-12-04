import socket
import threading
import sys
import time

# Configuration
HOST = '0.0.0.0'
PORT = 9999

# Thread-safe list to store connected client sockets
clients = []
clients_lock = threading.Lock()


def handle_client(client_socket, address):
    """
    Runs in a separate thread for each connected agent.
    Listens for incoming logs or confirmations.
    """
    print(f"[+] New connection from {address}")

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break

            msg = data.decode("utf-8").strip()
            print(f"[{address[0]}] log: {msg}")

        except (ConnectionResetError, ConnectionAbortedError):
            break
        except Exception as e:
            print(f"Error with {address}: {e}")
            break

    # Cleanup on disconnect
    print(f"[-] Connection lost from {address}")
    with clients_lock:
        if client_socket in clients:
            clients.remove(client_socket)

    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"[*] Controller listening on {HOST}:{PORT}")
    except Exception as e:
        print(f"Fatal error binding to port: {e}")
        sys.exit(1)

    while True:
        client, addr = server.accept()
        with clients_lock:
            clients.append(client)

        client_handler = threading.Thread(target=handle_client, args=(client, addr))
        client_handler.daemon = True
        client_handler.start()


def command_interface():
    """Interactive Command Line Interface (CLI)"""
    time.sleep(1)
    print("\n--- Network Controller CLI ---")
    print("Commands: status, push, exit")

    while True:
        try:
            cmd = input("Control> ").strip().lower()

            if cmd == "exit":
                print("Shutting down...")
                sys.exit()

            elif cmd == "status":
                with clients_lock:
                    print(f"Active Agents: {len(clients)}")

            elif cmd == "push":
                with clients_lock:
                    if not clients:
                        print("No agents detected.")
                        continue

                    config_data = input("Enter config command/data: ").strip()
                    print(f"Pushing to {len(clients)} agents...")

                    for c in clients[:]:
                        try:
                            c.send(f"CONFIG:{config_data}".encode("utf-8"))
                        except:
                            print("Failed to send to client. Removing from list.")
                            clients.remove(c)

            else:
                print("Unknown command.")

        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit()


if __name__ == "__main__":
    # Start server thread
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    # Run CLI in main thread
    command_interface()
