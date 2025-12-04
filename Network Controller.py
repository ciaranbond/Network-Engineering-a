import socket
import threading
import sys
import time

# Configuration
Host = '0.0.0.0'
Port = 9999

# Thread safe list to store connected client sockets
clients = []

def handle_client(client_socket, address)
  """
  Runs in separate thread for each connected agent. Listens for incoming logs or confirmations.
  """
print(f"[+] new connection from {address}")
while True:
  try:
      #size 1024 buffer control standard
      data = client_socket.recv(1024)
      if not data:
        break
      .strip()
      print(f"\n[{address[0]}] log: {data.decode('utf-8').strip()}")
  except ConnectionResetError:
      break
  except Exception as e:
      print(f"Error with {address}: {e}")
      break

# Client disconnect cleanup
print(f"[-] connection lost from {address}")
if client_socket in clients:
  clients.remove(client_socket)
client.socket.close()

# Main socket listener with script restart option errorless
def start_server():
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

  try:
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] controller listening om {HOST}:{PORT}")
  except Exception as e:
    print(f"fatal error binding to port: {e}")
    sys.exit(1)

  while True:
    client, addr = server.accept()
    clients.append(client)
    # Threading so client doesn't disconnect
    client.handler = threading.Thread(target=handle_client, args=(client,addr))
    client_handler.daemon = True """Kills thread if main program exits"""
    client_handler.start()

def command_interface():
  """Interactive Command Line Interface (CLI)"""
  time.sleep(1) """delay for server to initialise"""
  print("\n--- Network Controller CLI ---")
  print("Commands: status, push, exit")

  while True:
    try:
      cmd = input("Control> ").strip().lower()

      if cmd == 'exit':
        print("shutting down...")
        sys.exit()

      elif cmd == 'status':
        print(f"Active Agents: {len(clients)}")
      elif cmd == 'push':
        if not clients:
          print ("No agent detected")
          continue

        config_data = input("enter config command/data: ")
        print(f"pushing to {len(clients)} agents...")

# Iterate list copy to avoid errors
      for c in clients[:]:
        try:
# data translation protocol
          c.send(f"CONFIG:{config.data}".encode('utf-8'))
        except:
          print("Failed to send to client. Removing from list.")
          if c in clients:
            clients.remove(c)
    else:
      print("unknown command")
  except KeyboardInterrupt:
    print("\nExiting...")
    sys.exit()

if __name__ == __main_":
  # starts background server logic
  t = threading.Thread(target=start_server)
  t.daemon = True """ensures thread terminates when main CLI terminates"""
  t.start()

# Retains main CLI thread
  command_interface()
