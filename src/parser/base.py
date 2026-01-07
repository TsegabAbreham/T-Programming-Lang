# parser/base.py
from error import unexpected_token

class ParserBase:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def peek(self, n=1):
        if self.pos + n < len(self.tokens):
            return self.tokens[self.pos + n][0]
        return None

    def eat(self, token_type):
        type_, value = self.current()
        if type_ == token_type:
            self.pos += 1
            return value
        raise unexpected_token(self, expected=token_type)
