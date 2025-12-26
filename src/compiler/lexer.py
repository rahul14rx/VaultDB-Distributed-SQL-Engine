from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):
    # Keywords
    INSERT = auto()
    INTO = auto()
    VALUES = auto()
    SELECT = auto()
    FROM = auto()
    
    # Symbols
    LPAREN = auto()  # (
    RPAREN = auto()  # )
    COMMA = auto()   # ,
    STAR = auto()    # *
    
    # Data
    INTEGER = auto()
    STRING = auto()
    IDENTIFIER = auto() # Table names, column names
    
    EOF = auto() # End of File

@dataclass
class Token:
    type: TokenType
    value: str = None

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.current_char = self.source[0] if self.source else None

    def advance(self):
        """Move one character forward"""
        self.pos += 1
        if self.pos >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def parse_identifier(self):
        """Handle keywords (INSERT) and identifiers (users)"""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        # Check if it's a reserved keyword
        keyword_map = {
            'insert': TokenType.INSERT,
            'into': TokenType.INTO,
            'values': TokenType.VALUES,
            'select': TokenType.SELECT,
            'from': TokenType.FROM,
        }
        
        # SQL is case-insensitive (INSERT == insert), so we lower() it
        token_type = keyword_map.get(result.lower(), TokenType.IDENTIFIER)
        return Token(token_type, result)

    def parse_string(self):
        """Handle "text inside quotes" """
        result = ''
        self.advance() # Skip opening quote
        
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
            
        self.advance() # Skip closing quote
        return Token(TokenType.STRING, result)

    def parse_number(self):
        """Handle 12345"""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(TokenType.INTEGER, int(result))

    def get_next_token(self):
        while self.current_char is not None:
            
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
                
            if self.current_char.isalpha():
                return self.parse_identifier()
                
            if self.current_char.isdigit():
                return self.parse_number()
                
            if self.current_char == '"':
                return self.parse_string()
                
            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(')
                
            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')
                
            if self.current_char == ',':
                self.advance()
                return Token(TokenType.COMMA, ',')

            if self.current_char == '*':
                self.advance()
                return Token(TokenType.STAR, '*')

            raise Exception(f"Unknown character: {self.current_char}")

        return Token(TokenType.EOF)