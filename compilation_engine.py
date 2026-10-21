import sys

class CompilationEngine:
    """
    Motor de Análise Sintática para a linguagem Jack.
    Gera a árvore sintática no formato XML exigido pelo Nand2Tetris.
    """

    OP_SYMBOLS = {'+', '-', '*', '/', '&', '|', '<', '>', '='}
    UNARY_OP_SYMBOLS = {'-', '~'}
    KEYWORD_CONSTANTS = {'true', 'false', 'null', 'this'}

    def __init__(self, tokenizer, output_file_path):
        self.tokenizer = tokenizer
        self.out = open(output_file_path, 'w', encoding='utf-8')
        self.indent_level = 0
        
        # Posiciona no primeiro token
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()

    def close(self):
        self.out.close()

    # --- Métodos Auxiliares de Saída e Navegação ---

    def _write(self, line):
        indent = "  " * self.indent_level
        self.out.write(f"{indent}{line}\n")

    def _open_tag(self, tag_name):
        self._write(f"<{tag_name}>")
        self.indent_level += 1

    def _close_tag(self, tag_name):
        self.indent_level -= 1
        self._write(f"</{tag_name}>")

    def _escape_xml(self, symbol):
        escapes = {'<': '&lt;', '>': '&gt;', '"': '&quot;', '&': '&amp;'}
        return escapes.get(symbol, symbol)

    def _eat_current_token(self):
        """Escreve o token atual e avança para o próximo."""
        ttype = self.tokenizer.token_type()
        val = self.tokenizer.current_token

        if ttype == "keyword":
            self._write(f"<keyword> {val} </keyword>")
        elif ttype == "symbol":
            self._write(f"<symbol> {self._escape_xml(val)} </symbol>")
        elif ttype == "integerConstant":
            self._write(f"<integerConstant> {val} </integerConstant>")
        elif ttype == "stringConstant":
            # Remove as aspas delimitadoras no XML
            self._write(f"<stringConstant> {val[1:-1]} </stringConstant>")
        elif ttype == "identifier":
            self._write(f"<identifier> {val} </identifier>")

        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()

    def _process(self, expected_token_or_type):
        """Verifica e consome um token esperado."""
        curr = self.tokenizer.current_token
        ttype = self.tokenizer.token_type()

        if curr == expected_token_or_type or ttype == expected_token_or_type:
            self._eat_current_token()
        else:
            raise SyntaxError(
                f"Erro Sintático: Esperado '{expected_token_or_type}', mas encontrado '{curr}' (Tipo: {ttype})"
            )

    # --- Regras Sintáticas da Gramática Jack ---

    def compile_class(self):
        """'class' className '{' classVarDec* subroutineDec* '}'"""
        self._open_tag("class")
        
        self._process("class")
        self._process("identifier")  # className
        self._process("{")

        # classVarDec* ('static' | 'field')
        while self.tokenizer.current_token in ('static', 'field'):
            self.compile_class_var_dec()

        # subroutineDec* ('constructor' | 'function' | 'method')
        while self.tokenizer.current_token in ('constructor', 'function', 'method'):
            self.compile_subroutine()

        self._process("}")
        self._close_tag("class")

    def compile_class_var_dec(self):
        """('static' | 'field') type varName (',' varName)* ';'"""
        self._open_tag("classVarDec")

        self._process(self.tokenizer.current_token)  # 'static' ou 'field'
        self._process(self.tokenizer.current_token)  # type
        self._process("identifier")                 # varName

        while self.tokenizer.current_token == ',':
            self._process(",")
            self._process("identifier")

        self._process(";")
        self._close_tag("classVarDec")

    def compile_subroutine(self):
        """('constructor'|'function'|'method') ('void'|type) subroutineName '(' parameterList ')' subroutineBody"""
        self._open_tag("subroutineDec")

        self._process(self.tokenizer.current_token)  # constructor/function/method
        self._process(self.tokenizer.current_token)  # void/type
        self._process("identifier")                 # subroutineName
        
        self._process("(")
        self.compile_parameter_list()
        self._process(")")

        self.compile_subroutine_body()

        self._close_tag("subroutineDec")

    def compile_parameter_list(self):
        """((type varName) (',' type varName)*)?"""
        self._open_tag("parameterList")

        if self.tokenizer.current_token != ')':
            self._process(self.tokenizer.current_token)  # type
            self._process("identifier")                 # varName

            while self.tokenizer.current_token == ',':
                self._process(",")
                self._process(self.tokenizer.current_token)  # type
                self._process("identifier")                 # varName

        self._close_tag("parameterList")

    def compile_subroutine_body(self):
        """'{' varDec* statements '}'"""
        self._open_tag("subroutineBody")
        
        self._process("{")

        while self.tokenizer.current_token == 'var':
            self.compile_var_dec()

        self.compile_statements()

        self._process("}")
        self._close_tag("subroutineBody")

    def compile_var_dec(self):
        """'var' type varName (',' varName)* ';'"""
        self._open_tag("varDec")

        self._process("var")
        self._process(self.tokenizer.current_token)  # type
        self._process("identifier")                 # varName

        while self.tokenizer.current_token == ',':
            self._process(",")
            self._process("identifier")

        self._process(";")
        self._close_tag("varDec")
