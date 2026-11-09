from engine_base import EngineBase
from expressions_mixin import ExpressionsMixin
from statements_mixin import StatementsMixin
from symbol_table import SymbolTable
from vm_writer import VMWriter

class CompilationEngine(StatementsMixin, ExpressionsMixin, EngineBase):
    """
    Motor de Compilação Jack -> Código VM.
    Gerencia a estrutura global de classes, subrotinas, tabela de símbolos e escrita VM.
    """

    def __init__(self, tokenizer, output_vm_path):
        super().__init__(tokenizer, output_vm_path)
        self.symbol_table = SymbolTable()
        self.vm_writer = VMWriter(output_vm_path)
        self.class_name = ""
        self.label_index = 0  # Gerador de rótulos únicos para if/while

    def get_next_label(self, prefix: str) -> str:
        """Gera rótulos únicos no formato PREFIX_N (ex: IF_TRUE0)."""
        lbl = f"{prefix}{self.label_index}"
        self.label_index += 1
        return lbl

    def compile_class(self):
        """Compila a classe completa registrando símbolos e subrotinas."""
        self._process("class")
        self.class_name = self.tokenizer.current_token
        self._process("identifier")  # className
        self._process("{")

        # Processa declarações de variáveis de classe ('static' | 'field')
        while self.tokenizer.current_token in ('static', 'field'):
            self.compile_class_var_dec()

        # Processa subrotinas ('constructor' | 'function' | 'method')
        while self.tokenizer.current_token in ('constructor', 'function', 'method'):
            self.compile_subroutine()

        self._process("}")
        self.vm_writer.close()

    def compile_class_var_dec(self):
        """Registra variáveis de classe ('static' ou 'field') na SymbolTable."""
        kind = self.tokenizer.current_token  # 'static' ou 'field'
        self._process(kind)

        type_ = self.tokenizer.current_token
        self._process_type()

        name = self.tokenizer.current_token
        self._process("identifier")
        self.symbol_table.define(name, type_, kind)

        while self.tokenizer.current_token == ',':
            self._process(",")
            name = self.tokenizer.current_token
            self._process("identifier")
            self.symbol_table.define(name, type_, kind)

        self._process(";")

    def compile_subroutine(self):
        """Compila subrotina (construtor, função ou método) e emite prólogo VM."""
        self.symbol_table.start_subroutine()

        subroutine_kind = self.tokenizer.current_token  # 'constructor', 'function', 'method'
        self._process(subroutine_kind)

        return_type = self.tokenizer.current_token
        self._process_return_type()

        subroutine_name = self.tokenizer.current_token
        self._process("identifier")

        # Em métodos, argument 0 é a própria instância ('this')
        if subroutine_kind == 'method':
            self.symbol_table.define("this", self.class_name, "ARG")

        self._process("(")
        self.compile_parameter_list()
        self._process(")")

        # Compila o corpo e gera as instruções de inicialização
        self.compile_subroutine_body(subroutine_kind, subroutine_name)

    def compile_parameter_list(self):
        """Registra parâmetros da subrotina na SymbolTable como 'ARG'."""
        if self.tokenizer.current_token != ')':
            type_ = self.tokenizer.current_token
            self._process_type()

            name = self.tokenizer.current_token
            self._process("identifier")
            self.symbol_table.define(name, type_, "ARG")

            while self.tokenizer.current_token == ',':
                self._process(",")
                type_ = self.tokenizer.current_token
                self._process_type()

                name = self.tokenizer.current_token
                self._process("identifier")
                self.symbol_table.define(name, type_, "ARG")

    def compile_subroutine_body(self, subroutine_kind: str, subroutine_name: str):
        """Compila declarações de variáveis locais, emite 'function' e grava o prólogo."""
        self._process("{")

        # Povoa variáveis locais (var) na SymbolTable
        while self.tokenizer.current_token == 'var':
            self.compile_var_dec()

        # Emite instrução 'function ClassName.subroutineName nLocals'
        n_locals = self.symbol_table.var_count("VAR")
        full_name = f"{self.class_name}.{subroutine_name}"
        self.vm_writer.write_function(full_name, n_locals)

        # Prólogos dependentes do tipo de subrotina
        if subroutine_kind == 'constructor':
            n_fields = self.symbol_table.var_count("FIELD")
            self.vm_writer.write_push("constant", n_fields)
            self.vm_writer.write_call("Memory.alloc", 1)
            self.vm_writer.write_pop("pointer", 0)
        elif subroutine_kind == 'method':
            self.vm_writer.write_push("argument", 0)
            self.vm_writer.write_pop("pointer", 0)

        # Compila os comandos (statements) da subrotina
        self.compile_statements()

        self._process("}")

    def compile_var_dec(self):
        """Registra variáveis locais ('var') na SymbolTable como 'VAR'."""
        self._process("var")

        type_ = self.tokenizer.current_token
        self._process_type()

        name = self.tokenizer.current_token
        self._process("identifier")
        self.symbol_table.define(name, type_, "VAR")

        while self.tokenizer.current_token == ',':
            self._process(",")
            name = self.tokenizer.current_token
            self._process("identifier")
            self.symbol_table.define(name, type_, "VAR")

        self._process(";")