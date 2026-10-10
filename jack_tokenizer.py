# jack_tokenizer.py

# Tipos de Tokens
KEYWORD = "keyword"
SYMBOL = "symbol"
IDENTIFIER = "identifier"
INT_CONST = "integerConstant"
STRING_CONST = "stringConstant"

# Palavras reservadas e símbolos da linguagem Jack
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
        self.raw_code = ""
        self.tokens = []
        self.current_index = -1
        self.current_token = None