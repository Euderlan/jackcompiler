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
        """Compila a estrutura completa de uma classe: 'class' className '{' classVarDec* subroutineDec* '}'"""
        self._open_tag("class")
        
        self._process("class")
        self._process("identifier")  # className
        self._process("{")

        # Processa declarações de variáveis de classe ('static' | 'field')
        while self.tokenizer.current_token in ('static', 'field'):
            self.compile_class_var_dec()

        # Processa declarações de subrotinas ('constructor' | 'function' | 'method')
        while self.tokenizer.current_token in ('constructor', 'function', 'method'):
            self.compile_subroutine()

        self._process("}")
        self._close_tag("class")

    def compile_class_var_dec(self):
        """Compila declarações de variáveis de classe: ('static' | 'field') type varName (',' varName)* ';'"""
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
        """Compila declarações de subrotinas (funções/métodos/construtores)."""
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
        """Compila a lista de parâmetros de uma subrotina: ((type varName) (',' type varName)*)?"""
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
        """Compila o corpo de uma subrotina: '{' varDec* statements '}'"""
        self._open_tag("subroutineBody")
        
        self._process("{")

        while self.tokenizer.current_token == 'var':
            self.compile_var_dec()

        self.compile_statements()

        self._process("}")
        self._close_tag("subroutineBody")

    def compile_var_dec(self):
        """Compila declarações de variáveis locais: 'var' type varName (',' varName)* ';'"""
        self._open_tag("varDec")

        self._process("var")
        self._process(self.tokenizer.current_token)  # type
        self._process("identifier")                 # varName

        while self.tokenizer.current_token == ',':
            self._process(",")
            self._process("identifier")

        self._process(";")
        self._close_tag("varDec")