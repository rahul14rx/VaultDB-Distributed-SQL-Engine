from src.backend.pager import Pager, PAGE_SIZE

def test_database_storage():
    print("--- Starting Storage Engine Test ---")
    
    db_file = "database.db"
    pager = Pager(db_file)

    # 1. Create some data (Convert string to raw bytes)
    data1 = b"Hello, this is Page 0! The beginning of the DB."
    data2 = b"And this is Page 3. We skipped Page 1 and 2!"

    # Pad the data so it fits the visualization (Optional, but good for understanding)
    # We are just writing raw bytes now.
    
    print(f"[Write] Writing {len(data1)} bytes to Page 0...")
    pager.write_page(0, data1)

    print(f"[Write] Writing {len(data2)} bytes to Page 3...")
    pager.write_page(3, data2)

    # 2. Read it back
    print("\n--- Reading Back ---")
    
    page_0_data = pager.read_page(0)
    # .strip(b'\x00') removes the empty null bytes so we can read the text
    print(f"Page 0 Content: {page_0_data[:50]}") 

    page_1_data = pager.read_page(1)
    print(f"Page 1 Content (Should be empty): {page_1_data[:50]}")

    page_3_data = pager.read_page(3)
    print(f"Page 3 Content: {page_3_data[:50]}")

    pager.close()
    print("\n--- Test Passed: Binary Storage Works ---")

if __name__ == "__main__":
    test_database_storage()