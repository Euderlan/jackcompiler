# jack_tokenizer.py
import re
import os
import sys

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

def escape_xml(symbol):
    escapes = {
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        '&': '&amp;'
    }
    return escapes.get(symbol, symbol)




class JackTokenizer:
    def __init__(self, input_file):
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Remover comentários
        self.code = self._remove_comments(content)
        # 2. Extrair os tokens do código limpo
        self.tokens = self._tokenize(self.code)
        # 3. Ponteiros de navegação
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

def generate_tokens_xml(jack_file_path, output_xml_path):
    tokenizer = JackTokenizer(jack_file_path)

    with open(output_xml_path, 'w', encoding='utf-8') as out:
        out.write("<tokens>\n")

        while tokenizer.has_more_tokens():
            tokenizer.advance()
            ttype = tokenizer.token_type()

            if ttype == KEYWORD:
                out.write(f"<keyword> {tokenizer.key_word()} </keyword>\n")
            elif ttype == SYMBOL:
                out.write(f"<symbol> {escape_xml(tokenizer.symbol())} </symbol>\n")
            elif ttype == INT_CONST:
                out.write(f"<integerConstant> {tokenizer.int_val()} </integerConstant>\n")
            elif ttype == STRING_CONST:
                out.write(f"<stringConstant> {tokenizer.string_val()} </stringConstant>\n")
            elif ttype == IDENTIFIER:
                out.write(f"<identifier> {tokenizer.identifier()} </identifier>\n")

        out.write("</tokens>\n")
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python jack_tokenizer.py <arquivo.jack ou diretorio>")
        sys.exit(1)

    path = sys.argv[1]
    files_to_process = []

    if os.path.isfile(path) and path.endswith('.jack'):
        files_to_process.append(path)
    elif os.path.isdir(path):
        for f in os.listdir(path):
            if f.endswith('.jack'):
                files_to_process.append(os.path.join(path, f))

    for jack_file in files_to_process:
        xml_output = jack_file.replace('.jack', 'T_my.xml')
        generate_tokens_xml(jack_file, xml_output)
        print(f"Arquivo de tokens gerado: {xml_output}")