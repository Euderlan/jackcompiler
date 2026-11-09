# src/symbol_table.py

class SymbolTable:
    """
    Gerencia a tabela de símbolos para compilação Jack em dois escopos:
    - Escopo de Classe (STATIC, FIELD/THIS)
    - Escopo de Subrotina (ARG/ARGUMENT, VAR/LOCAL)
    """

    STATIC = "STATIC"
    FIELD = "FIELD"
    ARG = "ARG"
    VAR = "VAR"

    def __init__(self):
        self.class_scope = {}
        self.subroutine_scope = {}
        self.counts = {
            self.STATIC: 0,
            self.FIELD: 0,
            self.ARG: 0,
            self.VAR: 0
        }

    def start_subroutine(self):
        """Reinicia a tabela de símbolos no escopo de subrotina ao entrar em uma nova função/método."""
        self.subroutine_scope.clear()
        self.counts[self.ARG] = 0
        self.counts[self.VAR] = 0

    def define(self, name: str, type_: str, kind: str):
        """Define um novo símbolo e atribui o próximo índice sequencial disponível."""
        kind_upper = kind.upper()
        if kind_upper == "STATIC":
            k = self.STATIC
        elif kind_upper in ("FIELD", "THIS"):
            k = self.FIELD
        elif kind_upper in ("ARG", "ARGUMENT"):
            k = self.ARG
        elif kind_upper in ("VAR", "LOCAL"):
            k = self.VAR
        else:
            raise ValueError(f"Tipo de variável desconhecido: {kind}")

        index = self.counts[k]
        symbol_info = {"type": type_, "kind": k, "index": index}

        if k in (self.STATIC, self.FIELD):
            self.class_scope[name] = symbol_info
        else:
            self.subroutine_scope[name] = symbol_info

        self.counts[k] += 1

    def var_count(self, kind: str) -> int:
        """Retorna o número de variáveis declaradas do tipo especificado."""
        kind_upper = kind.upper()
        mapping = {"STATIC": self.STATIC, "FIELD": self.FIELD, "THIS": self.FIELD,
                   "ARG": self.ARG, "ARGUMENT": self.ARG, "VAR": self.VAR, "LOCAL": self.VAR}
        k = mapping.get(kind_upper, kind_upper)
        return self.counts.get(k, 0)

    def _lookup(self, name: str):
        """Busca o símbolo prioritariamente no escopo de subrotina, e depois no de classe."""
        if name in self.subroutine_scope:
            return self.subroutine_scope[name]
        return self.class_scope.get(name, None)

    def kind_of(self, name: str):
        """Retorna o tipo de segmento da variável ('STATIC', 'FIELD', 'ARG', 'VAR') ou None."""
        info = self._lookup(name)
        return info["kind"] if info else None

    def type_of(self, name: str):
        """Retorna o tipo de dado da variável ou None."""
        info = self._lookup(name)
        return info["type"] if info else None

    def index_of(self, name: str):
        """Retorna o índice da variável no segmento ou None."""
        info = self._lookup(name)
        return info["index"] if info else None