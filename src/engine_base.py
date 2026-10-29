class EngineBase:
    """
    Infraestrutura base do CompilationEngine.
    Gerencia a escrita no arquivo XML, controle de indentação e consumo de tokens.
    """

    OP_SYMBOLS = {'+', '-', '*', '/', '&', '|', '<', '>', '='}
    UNARY_OP_SYMBOLS = {'-', '~'}
    KEYWORD_CONSTANTS = {'true', 'false', 'null', 'this'}

    def __init__(self, tokenizer, output_file_path):
        self.tokenizer = tokenizer
        self.out = open(output_file_path, 'w', encoding='utf-8')
        self.indent_level = 0
        
        # Posiciona o tokenizer no primeiro token válido do arquivo
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()

    def close(self):
        """Fecha o arquivo de saída XML."""
        self.out.close()

    # --- Métodos de Formatação e Escrita ---

    def _write(self, line):
        """Escreve uma linha no arquivo mantendo a indentação atual."""
        indent = "  " * self.indent_level
        self.out.write(f"{indent}{line}\n")

    def _open_tag(self, tag_name):
        """Abre uma tag não-terminal e incrementa o nível de indentação."""
        self._write(f"<{tag_name}>")
        self.indent_level += 1

    def _close_tag(self, tag_name):
        """Decrementa a indentação e fecha uma tag não-terminal."""
        self.indent_level -= 1
        self._write(f"</{tag_name}>")

    def _escape_xml(self, symbol):
        """Converte caracteres especiais para entidades XML válidas."""
        escapes = {'<': '&lt;', '>': '&gt;', '"': '&quot;', '&': '&amp;'}
        return escapes.get(symbol, symbol)

    def _eat_current_token(self):
        """Escreve o token atual em sua tag correspondente e avança para o próximo."""
        ttype = self.tokenizer.token_type()
        val = self.tokenizer.current_token

        if ttype == "keyword":
            self._write(f"<keyword> {val} </keyword>")
        elif ttype == "symbol":
            self._write(f"<symbol> {self._escape_xml(val)} </symbol>")
        elif ttype == "integerConstant":
            self._write(f"<integerConstant> {val} </integerConstant>")
        elif ttype == "stringConstant":
            # Remove as aspas delimitadoras do texto ao salvar no XML
            self._write(f"<stringConstant> {val[1:-1]} </stringConstant>")
        elif ttype == "identifier":
            self._write(f"<identifier> {val} </identifier>")

        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()

    def _process(self, expected_token_or_type):
        """Valida se o token atual corresponde ao esperado e o consome."""
        curr = self.tokenizer.current_token
        ttype = self.tokenizer.token_type()

        if curr == expected_token_or_type or ttype == expected_token_or_type:
            self._eat_current_token()
        else:
            raise SyntaxError(
                f"Erro Sintático: Esperado '{expected_token_or_type}', mas encontrado '{curr}' (Tipo: {ttype})"
            )

    def _process_type(self):
        """Valida se o token atual é um tipo válido Jack ('int', 'char', 'boolean' ou nome de classe/identifier)."""
        curr = self.tokenizer.current_token
        ttype = self.tokenizer.token_type()

        if curr in ('int', 'char', 'boolean') or ttype == 'identifier':
            self._eat_current_token()
        else:
            raise SyntaxError(
                f"Erro Sintático: Esperado um tipo ('int', 'char', 'boolean' ou identificador), "
                f"mas encontrado '{curr}' (Tipo: {ttype})"
            )

    def _process_return_type(self):
        """Valida se o token atual é um tipo de retorno válido ('void' ou tipo)."""
        if self.tokenizer.current_token == 'void':
            self._eat_current_token()
        else:
            self._process_type()