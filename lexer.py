import re

# Token types
TOKEN_TYPES = [
    'NUMBER', 'IDENTIFIER', 'PLUS', 'MINUS', 'MULT', 'DIV', 'EQUAL',
    'LPAREN', 'RPAREN', 'PRINT', 'SEMICOLON', 'COMMA', 'COMMENT', 'STRING'
]

# Patterns for multi-character tokens (order matters!)
TOKEN_REGEX = [
    # Comments
    (r'~~(.*?)~~', 'COMMENT'),            # multi-line comment using ~~
    (r'#.*', 'COMMENT'),                  # single-line comment

    # Conditionals
    (r'if\b', 'IF'),
    (r'elif\b', 'ELSEIF'),
    (r'else\b', 'ELSE'),

    # Functions
    (r'fun\b', 'FUN'),


    # Variables and Variable related 
    (r'(["\'])(.*?)\1', 'STRING'),  
    (r'[a-zA-Z_][a-zA-Z0-9_]*', 'IDENTIFIER'),
    (r'out\b', 'PRINT'),           
    
    # Mathematical Operation
    (r'\d+', 'NUMBER'),
    (r'\+', 'PLUS'),
    (r'-', 'MINUS'),
    (r'\*', 'MULT'),
    (r'/', 'DIV'),
    (r'==', 'EQ'),
    (r'!=', 'NEQ'),
    (r'>=', 'GTE'),
    (r'<=', 'LTE'),
    (r'>', 'GT'),
    (r'<', 'LT'),
    (r'=', 'EQUAL'),

]

# Single-character tokens
SINGLE_CHAR_TOKENS = {
    ';': 'SEMICOLON',
    '(': 'LPAREN',
    ')': 'RPAREN',
    ',': 'COMMA',
    '{': 'LBRACKET',
    '}': 'RBRACKET'
}

def tokenize(code):
    tokens = []
    
    while code:
        code = code.lstrip()
        if not code:
            break

        matched = False

        # 1. Try regex patterns
        for pattern, type_ in TOKEN_REGEX:
            flags = re.DOTALL if type_ == 'COMMENT' and '~~' in pattern else 0
            match = re.match(pattern, code, flags)
            if match:
                if type_ == "STRING":
                    value = match.group(2)  # get inner content without quotes
                    tokens.append((type_, value))
                elif type_ == "COMMENT":
                    # skip comment entirely
                    code = code[match.end():]
                    matched = True
                    break
                else:
                    value = match.group(0)
                    tokens.append((type_, value))
                
                code = code[match.end():]
                matched = True
                break

        # 2. Single-character tokens
        if not matched and code[0] in SINGLE_CHAR_TOKENS:
            tokens.append((SINGLE_CHAR_TOKENS[code[0]], code[0]))
            code = code[1:]
            matched = True

        # 3. If nothing matched, raise error
        if not matched:
            raise Exception(f"Unexpected character: {code[0]!r}")

    return tokens

