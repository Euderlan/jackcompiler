class SymbolTable:
    """
    Gerencia a Tabela de Símbolos nos escopos de Classe e Subrotina.
    """
    def __init__(self):
        self.class_table = {}
        self.subroutine_table = {}
        self.counts = {'static': 0, 'field': 0, 'arg': 0, 'var': 0}

    def start_subroutine(self):
        """Reinicia a tabela de símbolos de subrotina."""
        self.subroutine_table.clear()
        self.counts['arg'] = 0
        self.counts['var'] = 0

    def define(self, name: str, type_str: str, kind: str):
        """Define uma nova variável na tabela de símbolos."""
        k = kind.lower()
        if k not in self.counts:
            raise ValueError(f"Kind inválido: {kind}")
        
        index = self.counts[k]
        entry = {'type': type_str, 'kind': k, 'index': index}
        
        if k in ('static', 'field'):
            self.class_table[name] = entry
        else:
            self.subroutine_table[name] = entry
            
        self.counts[k] += 1

    def var_count(self, kind: str) -> int:
        """Retorna o número de variáveis declaradas do tipo (kind) informado."""
        return self.counts.get(kind.lower(), 0)

    def _get(self, name: str):
        if name in self.subroutine_table:
            return self.subroutine_table[name]
        return self.class_table.get(name, None)

    def kind_of(self, name: str):
        """Retorna o segmento/kind da variável ('static', 'field', 'arg', 'var') ou None."""
        res = self._get(name)
        return res['kind'] if res else None

    def type_of(self, name: str):
        """Retorna o tipo da variável ou None."""
        res = self._get(name)
        return res['type'] if res else None

    def index_of(self, name: str):
        """Retorna o índice da variável ou None."""
        res = self._get(name)
        return res['index'] if res is not None else None