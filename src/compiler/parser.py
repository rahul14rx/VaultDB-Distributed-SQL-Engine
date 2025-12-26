from src.compiler.lexer import Lexer, TokenType
from src.backend.table import Table, Row

class Parser:
    def __init__(self, table):
        self.table = table
        self.tokens = []
        self.pos = 0

    def parse(self, statement: str) -> str:  # Changed return type to string
        try:
            lexer = Lexer(statement)
            self.tokens = []
            while True:
                token = lexer.get_next_token()
                if token.type == TokenType.EOF:
                    break
                self.tokens.append(token)
            
            self.pos = 0
            if not self.tokens:
                return ""

            command = self.current_token()
            
            # Now we RETURN strings instead of printing
            if command.type == TokenType.INSERT:
                return self.handle_insert()
            elif command.type == TokenType.SELECT:
                return self.handle_select()
            else:
                return f"Error: Unknown command '{command.value}'"
                
        except Exception as e:
            return f"Error: {str(e)}"

    def current_token(self):
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]

    def eat(self, token_type):
        """
        Validates that the current token matches what we expect,
        then advances to the next token.
        """
        token = self.current_token()
        if not token or token.type != token_type:
            expected = token_type
            actual = token.type if token else "None"
            raise Exception(f"Syntax Error: Expected {expected}, found {actual}")
        self.pos += 1
        return token

    def handle_insert(self):
        # ... (Validation code remains the same) ...
        self.eat(TokenType.INSERT)
        self.eat(TokenType.INTO)
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.VALUES)
        self.eat(TokenType.LPAREN)
        id_val = self.eat(TokenType.INTEGER).value
        self.eat(TokenType.COMMA)
        name_val = self.eat(TokenType.STRING).value
        self.eat(TokenType.COMMA)
        email_val = self.eat(TokenType.STRING).value
        self.eat(TokenType.RPAREN)
        
        row = Row(id_val, name_val, email_val)
        self.table.insert(row)
        
        return "SUCCESS: Row inserted."  # CHANGED

    def handle_select(self):
        # ... (Validation code remains the same) ...
        self.eat(TokenType.SELECT)
        self.eat(TokenType.STAR)
        self.eat(TokenType.FROM)
        self.eat(TokenType.IDENTIFIER)
        
        rows = self.table.select()
        
        # Format the output as a clean string
        if not rows:
            return "--- No Rows Found ---"
            
        result = f"--- Found {len(rows)} Rows ---\n"
        for r in rows:
            result += f"ID: {r.id} | Name: {r.username} | Email: {r.email}\n"
            
        return result