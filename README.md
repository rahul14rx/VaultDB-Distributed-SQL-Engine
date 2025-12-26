# VaultDB: Distributed SQL Engine

![Language](https://img.shields.io/badge/language-Python_3.10+-blue.svg)
![Type](https://img.shields.io/badge/type-Database_Engine-green.svg)
![Architecture](https://img.shields.io/badge/architecture-Client_Server-orange.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

**VaultDB** is a multithreaded, ACID-compliant SQL database engine engineered from scratch in Python. It implements a custom binary storage format, a hand-written recursive descent parser for SQL, and a concurrent TCP server architecture without relying on any external database libraries.

---

## 🏗 System Architecture

![VaultDB Architecture](https://raw.githubusercontent.com/rahul14rx/VaultDB-Distributed-SQL-Engine/main/architecture_diagram.png)

The system is composed of three decoupled layers:
1.  **Transport Layer**: A multithreaded TCP server handling concurrent client connections.
2.  **Compiler Layer**: A custom Lexer and Parser that tokenizes raw SQL and builds an execution plan.
3.  **Storage Layer**: A paged binary file engine (`.db`) that manages persistence using 4KB pages and C-style struct serialization.

---

## 🔧 Core Engineering Features

### 1. Custom Binary Storage Engine
Unlike simple text-based stores, VaultDB implements low-level data persistence:
* **Paged Memory**: Data is stored in fixed-size **4KB pages**, mimicking standard OS paging.
* **Struct Packing**: Rows are serialized into binary formats using Python's `struct` module for C-compatible memory layout.
* **Data Persistence**: State is maintained across server restarts by reading file offsets and page headers.

### 2. SQL Compiler (Lexer & Parser)
VaultDB does not use regex for parsing. It features a full **Recursive Descent Parser**:
* **Lexical Analysis**: Converts raw string input into a stream of tokens (`INSERT`, `IDENTIFIER`, `LPAREN`, etc.).
* **Syntax Analysis**: Validates the grammar of the token stream and executes the corresponding backend method.

### 3. Distributed Multithreading
* **Concurrency**: Uses `threading` and `socket` to spawn a dedicated worker thread for every new client connection.
* **Thread Safety**: Implements `threading.Lock()` to ensure mutual exclusion during file write operations, preventing race conditions.

---

## 🚀 Usage

### Prerequisites
* Python 3.10+
* No external `pip` dependencies required for the core engine.

### Start the Server
The server binds to `localhost:5432` and listens for incoming TCP connections.

```bash
python server.py
