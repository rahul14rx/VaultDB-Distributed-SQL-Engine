import struct
import os
from .pager import Pager, PAGE_SIZE

# Format:
# I = Unsigned Int (4 bytes)
# 32s = String of 32 chars (Username)
# 255s = String of 255 chars (Email)
COLUMN_FORMAT = 'I32s255s'
ROW_SIZE = struct.calcsize(COLUMN_FORMAT)

ROWS_PER_PAGE = PAGE_SIZE // ROW_SIZE
TABLE_MAX_PAGES = 100
TABLE_MAX_ROWS = ROWS_PER_PAGE * TABLE_MAX_PAGES

class Row:
    def __init__(self, id: int, username: str, email: str):
        self.id = id
        self.username = username
        self.email = email

    def serialize(self) -> bytes:
        """
        Converts the Row object into bytes.
        """
        username_bytes = self.username.encode('utf-8')
        email_bytes = self.email.encode('utf-8')
        
        # Pack string, ensuring we handle the padding correctly for struct
        return struct.pack(COLUMN_FORMAT, self.id, username_bytes, email_bytes)

    @staticmethod
    def deserialize(data: bytes):
        """
        Converts bytes back into a Row object.
        """
        try:
            id, username_bytes, email_bytes = struct.unpack(COLUMN_FORMAT, data)
            
            # Decode bytes back to string and strip null characters
            username = username_bytes.decode('utf-8').rstrip('\x00')
            email = email_bytes.decode('utf-8').rstrip('\x00')
            
            return Row(id, username, email)
        except Exception:
            return None

class Table:
    def __init__(self, filename):
        self.pager = Pager(filename)
        
        # Calculate num_rows based on actual file size
        file_size = os.path.getsize(filename)
        self.num_rows = file_size // ROW_SIZE

    def insert(self, row: Row):
        if self.num_rows >= TABLE_MAX_ROWS:
            raise Exception("Error: Table full.")

        row_num = self.num_rows
        page_num = row_num // ROWS_PER_PAGE
        row_offset = row_num % ROWS_PER_PAGE
        byte_offset = row_offset * ROW_SIZE

        original_page = self.pager.read_page(page_num)
        
        if len(original_page) < PAGE_SIZE:
             original_page = original_page.ljust(PAGE_SIZE, b'\x00')

        row_bytes = row.serialize()

        new_page_data = (
            original_page[:byte_offset] + 
            row_bytes + 
            original_page[byte_offset + ROW_SIZE:]
        )

        self.pager.write_page(page_num, new_page_data)
        self.num_rows += 1

    def select(self):
        rows = []
        for i in range(self.num_rows):
        
            page_num = i // ROWS_PER_PAGE
            row_offset = i % ROWS_PER_PAGE
            byte_offset = row_offset * ROW_SIZE
            
            page_data = self.pager.read_page(page_num)
            row_bytes = page_data[byte_offset : byte_offset + ROW_SIZE]
            
            row = Row.deserialize(row_bytes)
            if row:
                rows.append(row)
        return rows
        
    def close(self):
        self.pager.close()