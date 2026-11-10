class EngineBase:
    """
    Infraestrutura base do CompilationEngine para geração de código VM (Projeto 11).
    Apenas valida e avança os tokens sem gravar XML.
    """
    OP_SYMBOLS = {'+', '-', '*', '/', '&', '|', '<', '>', '='}
    UNARY_OP_SYMBOLS = {'-', '~'}
    KEYWORD_CONSTANTS = {'true', 'false', 'null', 'this'}

    def __init__(self, tokenizer, output_vm_path):
        self.tokenizer = tokenizer
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()

    def _process(self, expected):
        """Valida se o token atual corresponde ao esperado e avança."""
        curr = self.tokenizer.current_token
        ttype = self.tokenizer.token_type()

        if curr == expected or ttype == expected:
            if self.tokenizer.has_more_tokens():
                self.tokenizer.advance()
        else:
            raise SyntaxError(
                f"Erro Sintático: Esperado '{expected}', mas encontrado '{curr}' (Tipo: {ttype})"
            )

    def _process_type(self):
        """Valida se o token atual é um tipo válido Jack ('int', 'char', 'boolean' ou identifier)."""
        curr = self.tokenizer.current_token
        ttype = self.tokenizer.token_type()

        if curr in ('int', 'char', 'boolean') or ttype == 'identifier':
            if self.tokenizer.has_more_tokens():
                self.tokenizer.advance()
        else:
            raise SyntaxError(
                f"Erro Sintático: Esperado um tipo, mas encontrado '{curr}' (Tipo: {ttype})"
            )

    def _process_return_type(self):
        """Valida se o token atual é um tipo de retorno válido ('void' ou tipo)."""
        if self.tokenizer.current_token == 'void':
            if self.tokenizer.has_more_tokens():
                self.tokenizer.advance()
        else:
            self._process_type()