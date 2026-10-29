from engine_base import EngineBase
from expressions_mixin import ExpressionsMixin
from statements_mixin import StatementsMixin

class CompilationEngine(StatementsMixin, ExpressionsMixin, EngineBase):
    """
    Motor de Análise Sintática Principal.
    Herda as capacidades de controle base, comandos e expressões, 
    gerenciando a estrutura global de classes e subrotinas.
    """

    def compile_class(self):
        self._open_tag("class")
        self._process("class")
        self._process("identifier")  # className
        self._process("{")

        while self.tokenizer.current_token in ('static', 'field'):
            self.compile_class_var_dec()

        while self.tokenizer.current_token in ('constructor', 'function', 'method'):
            self.compile_subroutine()

        self._process("}")
        self._close_tag("class")

    def compile_class_var_dec(self):
        self._open_tag("classVarDec")

        self._process(self.tokenizer.current_token)  # 'static' ou 'field'
        self._process_type()                          # Validação estrita do tipo
        self._process("identifier")                 # varName

        while self.tokenizer.current_token == ',':
            self._process(",")
            self._process("identifier")

        self._process(";")
        self._close_tag("classVarDec")

    def compile_subroutine(self):
        self._open_tag("subroutineDec")

        self._process(self.tokenizer.current_token)  # constructor/function/method
        self._process_return_type()                 # Validação estrita de void | type
        self._process("identifier")                 # subroutineName
        
        self._process("(")
        self.compile_parameter_list()
        self._process(")")

        self.compile_subroutine_body()

        self._close_tag("subroutineDec")

    def compile_parameter_list(self):
        self._open_tag("parameterList")

        if self.tokenizer.current_token != ')':
            self._process_type()                     # Validação estrita do tipo
            self._process("identifier")             # varName

            while self.tokenizer.current_token == ',':
                self._process(",")
                self._process_type()                 # Validação estrita do tipo
                self._process("identifier")

        self._close_tag("parameterList")

    def compile_subroutine_body(self):
        self._open_tag("subroutineBody")
        self._process("{")

        while self.tokenizer.current_token == 'var':
            self.compile_var_dec()

        self.compile_statements()

        self._process("}")
        self._close_tag("subroutineBody")

    def compile_var_dec(self):
        self._open_tag("varDec")

        self._process("var")
        self._process_type()                         # Validação estrita do tipo
        self._process("identifier")                 # varName

        while self.tokenizer.current_token == ',':
            self._process(",")
            self._process("identifier")

        self._process(";")
        self._close_tag("varDec")