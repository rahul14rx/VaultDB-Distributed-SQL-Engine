from src.compiler.lexer import Lexer, TokenType

def test_sql_understanding():
    print("--- Testing SQL Lexer ---")
    
    # A standard SQL query
    sql = 'INSERT INTO users VALUES (1, "Rahul")'
    print(f"Parsing: {sql}")
    
    lexer = Lexer(sql)
    
    expected_tokens = [
        TokenType.INSERT,
        TokenType.INTO,
        TokenType.IDENTIFIER, # users
        TokenType.VALUES,
        TokenType.LPAREN,
        TokenType.INTEGER,    # 1
        TokenType.COMMA,
        TokenType.STRING,
        TokenType.RPAREN,
        TokenType.EOF
    ]
    
    count = 0
    while True:
        token = lexer.get_next_token()
        print(f"Token: {token.type} | Value: {token.value}")
        
        if token.type == TokenType.EOF:
            break
            
        # Verify order (Simple check)
        assert token.type == expected_tokens[count]
        count += 1
        
    print("\n--- Test Passed: Your engine understands SQL syntax! ---")

if __name__ == "__main__":
    test_sql_understanding()