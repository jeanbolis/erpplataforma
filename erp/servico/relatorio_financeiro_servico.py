from erp.repositorio.relatorio_financeiro_repo import RelatorioFinanceiroRepository


class RelatorioFinanceiroServico:

    @staticmethod
    def resumo():
        return RelatorioFinanceiroRepository.resumo_financeiro()