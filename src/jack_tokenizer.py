import re

KEYWORD = "keyword"
SYMBOL = "symbol"
IDENTIFIER = "identifier"
INT_CONST = "integerConstant"
STRING_CONST = "stringConstant"

KEYWORDS = {
    "class", "constructor", "function", "method", "field", "static", "var",
    "int", "char", "boolean", "void", "true", "false", "null", "this",
    "let", "do", "if", "else", "while", "return"
}

SYMBOLS = {
    '{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/',
    '&', '|', '<', '>', '=', '~'
}

class JackTokenizer:
    def __init__(self, input_file):
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.code = self._remove_comments(content)
        self.tokens = self._tokenize(self.code)
        self.current_index = -1
        self.current_token = None

    def _remove_comments(self, text):
        text = re.sub(r'/\*[\s\S]*?\*/', '', text)
        text = re.sub(r'//.*', '', text)
        return text

    def _tokenize(self, text):
        pattern = r'("[^"\n]*")|([{}()\[\].,;+\-*/&|<>=~])|(\d+)|([a-zA-Z_][a-zA-Z0-9_]*)'
        tokens = []
        for match in re.finditer(pattern, text):
            tokens.append(match.group(0))
        return tokens

    def has_more_tokens(self):
        return (self.current_index + 1) < len(self.tokens)

    def advance(self):
        if self.has_more_tokens():
            self.current_index += 1
            self.current_token = self.tokens[self.current_index]

    def token_type(self):
        token = self.current_token
        if token in KEYWORDS:
            return KEYWORD
        elif token in SYMBOLS:
            return SYMBOL
        elif token.startswith('"') and token.endswith('"'):
            return STRING_CONST
        elif token.isdigit():
            return INT_CONST
        else:
            return IDENTIFIER

    def key_word(self):
        return self.current_token

    def symbol(self):
        return self.current_token

    def int_val(self):
        return int(self.current_token)

    def string_val(self):
        return self.current_token[1:-1]

    def identifier(self):
        return self.current_token