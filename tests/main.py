from src.backend.table import Table
from src.compiler.parser import Parser
import sys

def main():
    # Point this variable to the file you created in 'test_database.py'
    db_file = "users.db"  
    
    # Use the variable here!
    table = Table(db_file) 
    parser = Parser(table)

    print(f"Welcome to ProjectVault DB (v1.0)")
    print(f"Connected to: {db_file}")
    print("Type 'exit' to quit.")
    print("-" * 30)

    while True:
        try:
            query = input("db > ").strip()
            
            if query == "exit":
                break
            if not query:
                continue

            parser.parse(query)

        except Exception as e:
            print(f"Error: {e}")

    table.close()
    print("Database connection closed.")