class StatementsMixin:
    """
    Mixin responsável por compilar comandos (statements) da linguagem Jack para VM.
    """

    def compile_statements(self):
        """Compila uma sequência de comandos."""
        while self.tokenizer.current_token in ('let', 'if', 'while', 'do', 'return'):
            if self.tokenizer.current_token == 'let':
                self.compile_let()
            elif self.tokenizer.current_token == 'if':
                self.compile_if()
            elif self.tokenizer.current_token == 'while':
                self.compile_while()
            elif self.tokenizer.current_token == 'do':
                self.compile_do()
            elif self.tokenizer.current_token == 'return':
                self.compile_return()

    def compile_let(self):
        """
        Compila o comando let:
        let varName ([ expr ])? = expr ;
        """
        self._process("let")
        var_name = self.tokenizer.current_token
        self._process("identifier")

        is_array = False
        if self.tokenizer.current_token == '[':
            is_array = True
            self._process("[")
            kind = self.symbol_table.kind_of(var_name)
            idx = self.symbol_table.index_of(var_name)
            self.vm_writer.write_push(kind, idx)

            self.compile_expression()
            self._process("]")
            self.vm_writer.write_arithmetic("add")

        self._process("=")
        self.compile_expression()
        self._process(";")

        if is_array:
            self.vm_writer.write_pop("temp", 0)       # Salva resultado de expr em temp 0
            self.vm_writer.write_pop("pointer", 1)    # Ajusta THAT para o endereço (a + i)
            self.vm_writer.write_push("temp", 0)      # Recupera o valor
            self.vm_writer.write_pop("that", 0)       # Grava em THAT 0
        else:
            kind = self.symbol_table.kind_of(var_name)
            idx = self.symbol_table.index_of(var_name)
            self.vm_writer.write_pop(kind, idx)

    def compile_if(self):
        """
        Compila o comando if/else:
        if ( expr ) { statements } (else { statements })?
        """
        label_true = self.get_next_label("IF_TRUE")
        label_false = self.get_next_label("IF_FALSE")
        label_end = self.get_next_label("IF_END")

        self._process("if")
        self._process("(")
        self.compile_expression()
        self._process(")")

        self.vm_writer.write_if(label_true)
        self.vm_writer.write_goto(label_false)
        self.vm_writer.write_label(label_true)

        self._process("{")
        self.compile_statements()
        self._process("}")

        if self.tokenizer.current_token == 'else':
            self._process("else")
            self.vm_writer.write_goto(label_end)
            self.vm_writer.write_label(label_false)
            self._process("{")
            self.compile_statements()
            self._process("}")
            self.vm_writer.write_label(label_end)
        else:
            self.vm_writer.write_label(label_false)

    def compile_while(self):
        """
        Compila o comando while:
        while ( expr ) { statements }
        """
        label_exp = self.get_next_label("WHILE_EXP")
        label_end = self.get_next_label("WHILE_END")

        self.vm_writer.write_label(label_exp)

        self._process("while")
        self._process("(")
        self.compile_expression()
        self._process(")")

        self.vm_writer.write_arithmetic("not")
        self.vm_writer.write_if(label_end)

        self._process("{")
        self.compile_statements()
        self._process("}")

        self.vm_writer.write_goto(label_exp)
        self.vm_writer.write_label(label_end)

    def compile_do(self):
        """
        Compila o comando do descartando o valor de retorno em temp 0:
        do subroutineCall ;
        """
        self._process("do")
        self.compile_expression()
        self._process(";")
        self.vm_writer.write_pop("temp", 0)

    def compile_return(self):
        """
        Compila o comando return:
        return ( expr )? ;
        """
        self._process("return")
        if self.tokenizer.current_token != ';':
            self.compile_expression()
        else:
            self.vm_writer.write_push("constant", 0)

        self._process(";")
        self.vm_writer.write_return()