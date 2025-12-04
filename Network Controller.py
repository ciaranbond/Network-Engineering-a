import socket
import threading
import sys
import time

HOST = '0.0.0.0'
PORT = 9999

clients = []
clients_lock = threading.Lock()

def handle_client(client_socket, address):
    print(f"[+] New connection from {address}")
    
    # Makefile to handle TCP stream buffering automatically and read line by line
    try:
        stream = client_socket.makefile('r', encoding='utf-8')
        
        for line in stream:
            msg = line.strip()
            # To fix UI glitch: typically write to log file, but for now:
            sys.stdout.write(f"\r[{address[0]}] {msg}\nControl> ") 
            
    except Exception as e:
        # Expected error on disconnect usually
        pass
    finally:
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
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

    while True:
        client, addr = server.accept()
        with clients_lock:
            clients.append(client)
        
        t = threading.Thread(target=handle_client, args=(client, addr), daemon=True)
        t.start()

def command_interface():
    print("\n--- Network Controller CLI ---")
    
    while True:
        try:
            # Using simple input
            cmd_raw = input("Control> ").strip().split(" ", 1)
            cmd = cmd_raw[0].lower()
            
            if cmd == "exit":
                sys.exit()
            
            elif cmd == "status":
                with clients_lock:
                    print(f"Active Agents: {len(clients)}")
            
            elif cmd == "push":
                if len(cmd_raw) < 2:
                    print("Usage: push <data>")
                    continue
                    
                payload = cmd_raw[1] + "\n" # Add newline delimiter for the client
                
                with clients_lock:
                    active_list = clients[:] 
                
                print(f"Pushing to {len(active_list)} agents...")
                
                for c in active_list:
                    try:
                        c.sendall(payload.encode('utf-8'))
                    except:
                        # handle_client thread handles cleanup to avoid race conditions
                        pass 

        except KeyboardInterrupt:
            sys.exit()

if __name__ == "__main__":
    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    time.sleep(0.5)
    command_interface()
