class ExpressionsMixin:
    """
    Mixin responsável por compilar expressões, termos, chamadas e operadores para VM.
    """

    OPERATORS = {
        '+': 'add',
        '-': 'sub',
        '=': 'eq',
        '>': 'gt',
        '<': 'lt',
        '&': 'and',
        '|': 'or'
    }

    def compile_expression(self):
        """Compila uma expressão (term (op term)*)."""
        self.compile_term()

        while self.tokenizer.current_token in ('+', '-', '*', '/', '=', '>', '<', '&', '|'):
            op = self.tokenizer.current_token
            self._process(op)
            self.compile_term()

            if op == '*':
                self.vm_writer.write_call("Math.multiply", 2)
            elif op == '/':
                self.vm_writer.write_call("Math.divide", 2)
            else:
                self.vm_writer.write_arithmetic(self.OPERATORS[op])

    def compile_term(self):
        """Compila um termo (constantes, variáveis, chamadas, arrays, operadores unários)."""
        token_type = self.tokenizer.token_type()
        token = self.tokenizer.current_token

        # 1. Constante Inteira
        if token_type == 'integerConstant':
            self.vm_writer.write_push("constant", int(token))
            self._process(token)

        # 2. Constante de String
        elif token_type == 'stringConstant':
            string_val = token[1:-1] if token.startswith('"') and token.endswith('"') else token
            self._process(token)
            self.vm_writer.write_push("constant", len(string_val))
            self.vm_writer.write_call("String.new", 1)
            for char in string_val:
                self.vm_writer.write_push("constant", ord(char))
                self.vm_writer.write_call("String.appendChar", 2)

        # 3. Palavras-chave constantes (true, false, null, this)
        elif token in ('true', 'false', 'null', 'this'):
            self._process(token)
            if token == 'true':
                self.vm_writer.write_push("constant", 1)
                self.vm_writer.write_arithmetic("neg")
            elif token in ('false', 'null'):
                self.vm_writer.write_push("constant", 0)
            elif token == 'this':
                self.vm_writer.write_push("pointer", 0)

        # 4. Operadores Unários (- / ~)
        elif token in ('-', '~'):
            self._process(token)
            self.compile_term()
            if token == '-':
                self.vm_writer.write_arithmetic("neg")
            else:
                self.vm_writer.write_arithmetic("not")

        # 5. Expressões entre Parênteses (expr)
        elif token == '(':
            self._process("(")
            self.compile_expression()
            self._process(")")

        # 6. Identificadores (Variáveis, Arrays, Chamadas de Método/Função)
        elif token_type == 'identifier':
            name = self.tokenizer.current_token
            self._process("identifier")

            # Acesso a Array: varName[expr]
            if self.tokenizer.current_token == '[':
                self._process("[")
                kind = self.symbol_table.kind_of(name)
                idx = self.symbol_table.index_of(name)
                self.vm_writer.write_push(kind, idx)

                self.compile_expression()
                self._process("]")

                self.vm_writer.write_arithmetic("add")
                self.vm_writer.write_pop("pointer", 1)
                self.vm_writer.write_push("that", 0)

            # Chamada de Método/Função: varName.subroutine() ou varName()
            elif self.tokenizer.current_token in ('(', '.'):
                self._compile_subroutine_call(name)

            # Variável Simples
            else:
                kind = self.symbol_table.kind_of(name)
                idx = self.symbol_table.index_of(name)
                self.vm_writer.write_push(kind, idx)

    def _compile_subroutine_call(self, first_name: str):
        """Auxiliar para compilar chamadas de subrotinas."""
        n_args = 0
        call_name = ""

        if self.tokenizer.current_token == '.':
            self._process(".")
            sub_name = self.tokenizer.current_token
            self._process("identifier")

            type_ = self.symbol_table.type_of(first_name)
            if type_ is not None:
                kind = self.symbol_table.kind_of(first_name)
                idx = self.symbol_table.index_of(first_name)
                self.vm_writer.write_push(kind, idx)
                call_name = f"{type_}.{sub_name}"
                n_args = 1
            else:
                call_name = f"{first_name}.{sub_name}"
                n_args = 0

        elif self.tokenizer.current_token == '(':
            self.vm_writer.write_push("pointer", 0)
            call_name = f"{self.class_name}.{first_name}"
            n_args = 1

        self._process("(")
        n_args += self.compile_expression_list()
        self._process(")")

        self.vm_writer.write_call(call_name, n_args)

    def compile_expression_list(self) -> int:
        """Compila a lista de expressões separadas por vírgula e retorna a contagem de argumentos."""
        n_args = 0
        if self.tokenizer.current_token != ')':
            self.compile_expression()
            n_args += 1
            while self.tokenizer.current_token == ',':
                self._process(",")
                self.compile_expression()
                n_args += 1
        return n_args