from erp.repositorio.relatorio_estoque_repo import RelatorioEstoqueRepository


class RelatorioEstoqueServico:

    @staticmethod
    def estoque_atual():
        return RelatorioEstoqueRepository.estoque_atual()