import socket

HOST = '127.0.0.1'
PORT = 5432

def print_table(response):
    """
    Manually renders a beautiful table without external libraries.
    """
    rows = []
    # 1. Parse the raw text response into a list of dictionaries
    lines = response.split('\n')
    for line in lines:
        if "|" in line and "ID:" in line:
            # format: "ID: 1 | Name: Rahul | Email: ..."
            parts = line.split('|')
            row = {
                "id": parts[0].split(':')[1].strip(),
                "name": parts[1].split(':')[1].strip(),
                "email": parts[2].split(':')[1].strip()
            }
            rows.append(row)

    if not rows:
        return

    # 2. Calculate column widths dynamically
    # Start with minimum widths based on headers
    w_id, w_name, w_email = 4, 10, 20
    
    for row in rows:
        w_id = max(w_id, len(row['id']))
        w_name = max(w_name, len(row['name']))
        w_email = max(w_email, len(row['email']))

    # Add a little padding
    w_id += 2
    w_name += 2
    w_email += 2

    # 3. Print the Table using Box Drawing Characters
    # Header
    print("┌" + "─" * w_id + "┬" + "─" * w_name + "┬" + "─" * w_email + "┐")
    header = f"│{'ID'.center(w_id)}│{'USERNAME'.center(w_name)}│{'EMAIL'.center(w_email)}│"
    print(header)
    print("├" + "─" * w_id + "┼" + "─" * w_name + "┼" + "─" * w_email + "┤")

    # Rows
    for row in rows:
        line = f"│{row['id'].center(w_id)}│{row['name'].ljust(w_name)}│{row['email'].ljust(w_email)}│"
        print(line)

    # Footer
    print("└" + "─" * w_id + "┴" + "─" * w_name + "┴" + "─" * w_email + "┘")

def start_client():
    print("\n--- ProjectVault Client (Zero Dependency Edition) ---")
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print(f"Connected to {HOST}:{PORT}!")
            print("Type 'exit' to quit.\n")
            
            while True:
                query = input("db-client > ")
                
                if query.lower() == 'exit':
                    break
                
                if not query.strip():
                    continue
                    
                s.sendall(query.encode('utf-8'))
                
                data = s.recv(4096)
                response = data.decode('utf-8')
                
                # Intelligent Display Logic
                if "ID:" in response and "|" in response:
                    print_table(response)
                elif "SUCCESS" in response:
                    print(f"✅  {response}")
                elif "Error" in response:
                    print(f"❌  {response}")
                else:
                    print(response)

    except ConnectionRefusedError:
        print("❌ Error: Could not connect to server. Is it running?")
    except KeyboardInterrupt:
        print("\nClient closing...")

if __name__ == "__main__":
    start_client()