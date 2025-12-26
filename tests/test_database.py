from src.backend.table import Table, Row
import os

DB_FILE = "users.db"

def test_database_insert():
    # Clean up old test file
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    print("--- Starting Database Stress Test ---")
    table = Table(DB_FILE)

    # 1. Insert 100 Users
    print("[Insert] Inserting 100 rows...")
    for i in range(100):
        username = f"User_{i}"
        email = f"user{i}@test.com"
        row = Row(i, username, email)
        table.insert(row)
    
    print(f"[Check] Table now has {table.num_rows} rows stored.")

    # 2. Select All to verify data integrity
    print("[Select] Reading back data...")
    all_rows = table.select()
    
    # Verify the last guy
    last_row = all_rows[-1]
    print(f"[Verify] Last Row ID: {last_row.id} | Name: {last_row.username}")
    
    assert last_row.id == 99
    assert last_row.username == "User_99"

    table.close()
    print("--- Test Passed: 100 Rows Inserted & Verified ---")

if __name__ == "__main__":
    test_database_insert()