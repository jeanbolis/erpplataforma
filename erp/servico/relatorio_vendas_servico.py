from erp.repositorio.relatorio_vendas_repo import RelatorioVendasRepository


class RelatorioVendasServico:

    @staticmethod
    def vendas_por_periodo(data_inicio: str, data_fim: str):
        return RelatorioVendasRepository.vendas_por_periodo(data_inicio, data_fim)