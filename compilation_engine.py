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
