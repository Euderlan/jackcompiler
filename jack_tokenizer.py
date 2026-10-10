# jack_tokenizer.py
import re

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
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        self.code = self._remove_comments(content)
        self.tokens = []
        self.current_index = -1
        self.current_token = None

    def _remove_comments(self, text):
        # Remove comentários em bloco /* ... */ e /** ... */
        text = re.sub(r'/\*[\s\S]*?\*/', '', text)
        # Remove comentários de linha //
        text = re.sub(r'//.*', '', text)
        return text

    def _tokenize(self, text):
        # Expressão regular para capturar strings, símbolos, números e identificadores/keywords
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