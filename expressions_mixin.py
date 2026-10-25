class ExpressionsMixin:
    """
    Mixin responsável pelo parsing de expressões, termos e listas de expressões na linguagem Jack.
    """

    def compile_expression(self):
        """Compila uma expressão: term (op term)*"""
        self._open_tag("expression")

        self.compile_term()

        # Processa operadores binários (+, -, *, /, etc.)
        while self.tokenizer.current_token in self.OP_SYMBOLS:
            self._process(self.tokenizer.current_token)
            self.compile_term()

        self._close_tag("expression")

    def compile_term(self):
        """
        Compila um termo (constantes, variáveis, chamadas de subrotina, 
        expressões entre parênteses ou operadores unários).
        """
        self._open_tag("term")

        ttype = self.tokenizer.token_type()
        curr = self.tokenizer.current_token

        if ttype == "integerConstant":
            self._process("integerConstant")
        elif ttype == "stringConstant":
            self._process("stringConstant")
        elif curr in self.KEYWORD_CONSTANTS:
            self._process(curr)
        elif curr in self.UNARY_OP_SYMBOLS:
            self._process(curr)
            self.compile_term()
        elif curr == '(':
            self._process("(")
            self.compile_expression()
            self._process(")")
        elif ttype == "identifier":
            self._process("identifier")
            
            # Lookahead para resolver ambiguidades: varName[expr], subroutineCall() ou varName.subroutineCall()
            if self.tokenizer.current_token == '[':
                self._process("[")
                self.compile_expression()
                self._process("]")
            elif self.tokenizer.current_token == '(':
                self._process("(")
                self.compile_expression_list()
                self._process(")")
            elif self.tokenizer.current_token == '.':
                self._process(".")
                self._process("identifier")
                self._process("(")
                self.compile_expression_list()
                self._process(")")

        self._close_tag("term")

    def compile_expression_list(self):
        """Compila uma lista de expressões separadas por vírgula: (expression (',' expression)*)?"""
        self._open_tag("expressionList")

        if self.tokenizer.current_token != ')':
            self.compile_expression()

            while self.tokenizer.current_token == ',':
                self._process(",")
                self.compile_expression()

        self._close_tag("expressionList")