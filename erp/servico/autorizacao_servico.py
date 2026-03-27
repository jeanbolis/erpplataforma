class AutorizacaoServico:

    PERMISSOES = {
        "ADMIN": {"*"},
        "FINANCEIRO": {"financeiro", "relatorios"},
        "ESTOQUE": {"estoque", "compras"},
        "VENDAS": {"vendas"}
    }

    @staticmethod
    def pode_acessar(papeis: list, recurso: str) -> bool:
        for papel in papeis:
            regras = AutorizacaoServico.PERMISSOES.get(papel, set())
            if "*" in regras or recurso in regras:
                return True
        return False