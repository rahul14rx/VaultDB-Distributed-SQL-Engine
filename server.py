import socket
import threading  # <--- NEW: The library for concurrency
from src.backend.table import Table
from src.compiler.parser import Parser

HOST = '127.0.0.1'
PORT = 5432

# Global Lock: Prevents two threads from writing to the file simultaneously
db_lock = threading.Lock()

def handle_client(conn, addr, table):
    """
    This function runs inside its OWN Thread.
    It handles one specific user until they disconnect.
    """
    print(f"[NEW CONNECTION] {addr} connected.")
    
    # Each client gets their own Parser instance
    parser = Parser(table)
    
    try:
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                
                query = data.decode('utf-8')
                print(f"[{addr}] Query: {query}")
                
                # CRITICAL SECTION
                # We lock the DB so this thread has exclusive access to the file
                with db_lock:
                    response = parser.parse(query)
                
                conn.sendall(response.encode('utf-8'))
                
    except ConnectionResetError:
        pass
    finally:
        print(f"[DISCONNECTED] {addr} disconnected.")

def start_server():
    print(f"--- ProjectVault Server Running on {HOST}:{PORT} (Multithreaded) ---")
    
    # Initialize Database ONCE
    table = Table("server_data.db")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        
        print("Waiting for connections...")
        
        while True:
            # 1. Accept the connection
            conn, addr = s.accept()
            
            # 2. Spin up a NEW Thread just for this user
            # We pass the 'handle_client' function to the thread
            thread = threading.Thread(target=handle_client, args=(conn, addr, table))
            thread.start()
            
            # 3. Print how many people are online
            # (active_count includes the main thread, so we subtract 1)
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()