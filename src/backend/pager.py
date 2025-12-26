import os

# The standard size for a database page (4KB)
PAGE_SIZE = 4096

class Pager:
    def __init__(self, filename):
        self.filename = filename
        
        # Check if file exists, if not create it
        if not os.path.exists(filename):
            with open(filename, 'wb') as f:
                pass  # Create empty file
        
        # Open in 'r+b' mode: Read + Write + Binary
        # This allows us to manipulate raw bytes
        self.file = open(filename, 'r+b')

    def write_page(self, page_num: int, data: bytes):
        if len(data) > PAGE_SIZE:
            raise ValueError(f"Data too large! Max {PAGE_SIZE} bytes.")

        # Calculate the exact byte offset in the file
        offset = page_num * PAGE_SIZE
        
        # Jump to that location
        self.file.seek(offset)
        
        # Write the data
        self.file.write(data)
        
        # Force the OS to save to disk immediately (Critical for DBs)
        self.file.flush() 

    def read_page(self, page_num: int) -> bytes:
        """
        Reads a specific page from the file.
        """
        offset = page_num * PAGE_SIZE
        self.file.seek(offset)
        
        # Read exactly 4096 bytes
        data = self.file.read(PAGE_SIZE)
        return data

    def close(self):
        self.file.close()