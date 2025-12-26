from src.backend.table import Row, ROW_SIZE

def test_row_serialization():
    print(f"--- Testing Row Serialization (Size: {ROW_SIZE} bytes) ---")

    # 1. Create a User
    original_user = Row(1, "Rahul", "rahul@example.com")
    print(f"[Input] ID: {original_user.id}, User: {original_user.username}")

    # 2. Serialize (Turn to Bytes)
    binary_data = original_user.serialize()
    print(f"[Binary] Hex Representation: {binary_data.hex()[:60]}... (truncated)")

    # 3. Deserialize (Turn back to Object)
    recovered_user = Row.deserialize(binary_data)
    print(f"[Output] ID: {recovered_user.id}, User: {recovered_user.username}")

    # 4. Verify
    assert original_user.id == recovered_user.id
    assert original_user.username == recovered_user.username
    assert original_user.email == recovered_user.email
    
    print("\n--- Test Passed: We can translate Objects to Bytes and back! ---")

if __name__ == "__main__":
    test_row_serialization()