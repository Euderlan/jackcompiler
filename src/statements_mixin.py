class StatementsMixin:
    """
    Mixin responsável pelo parsing dos comandos (statements) da linguagem Jack.
    """

    def compile_statements(self):
        """Compila uma sequência de comandos."""
        self._open_tag("statements")

        statement_keywords = ('let', 'if', 'while', 'do', 'return')
        while self.tokenizer.current_token in statement_keywords:
            kw = self.tokenizer.current_token
            if kw == 'let':
                self.compile_let()
            elif kw == 'if':
                self.compile_if()
            elif kw == 'while':
                self.compile_while()
            elif kw == 'do':
                self.compile_do()
            elif kw == 'return':
                self.compile_return()

        self._close_tag("statements")

    def compile_let(self):
        """Compila o comando 'let': 'let' varName ('[' expression ']')? '=' expression ';'"""
        self._open_tag("letStatement")

        self._process("let")
        self._process("identifier")

        if self.tokenizer.current_token == '[':
            self._process("[")
            self.compile_expression()
            self._process("]")

        self._process("=")
        self.compile_expression()
        self._process(";")

        self._close_tag("letStatement")

    def compile_if(self):
        """Compila o comando 'if': 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?"""
        self._open_tag("ifStatement")

        self._process("if")
        self._process("(")
        self.compile_expression()
        self._process(")")

        self._process("{")
        self.compile_statements()
        self._process("}")

        if self.tokenizer.current_token == 'else':
            self._process("else")
            self._process("{")
            self.compile_statements()
            self._process("}")

        self._close_tag("ifStatement")

    def compile_while(self):
        """Compila o comando 'while': 'while' '(' expression ')' '{' statements '}'"""
        self._open_tag("whileStatement")

        self._process("while")
        self._process("(")
        self.compile_expression()
        self._process(")")

        self._process("{")
        self.compile_statements()
        self._process("}")

        self._close_tag("whileStatement")

    def compile_do(self):
        """Compila o comando 'do': 'do' subroutineCall ';'"""
        self._open_tag("doStatement")

        self._process("do")
        self._process("identifier")

        if self.tokenizer.current_token == '.':
            self._process(".")
            self._process("identifier")

        self._process("(")
        self.compile_expression_list()
        self._process(")")

        self._process(";")
        self._close_tag("doStatement")

    def compile_return(self):
        """Compila o comando 'return': 'return' expression? ';'"""
        self._open_tag("returnStatement")

        self._process("return")

        if self.tokenizer.current_token != ';':
            self.compile_expression()

        self._process(";")
        self._close_tag("returnStatement")