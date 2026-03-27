from erp.repositorio.fluxo_caixa_repo import FluxoCaixaRepository


class FluxoCaixaServico:
    """
    Serviço de leitura de fluxo de caixa
    """

    @staticmethod
    def resumo_por_periodo(data_inicio: str, data_fim: str) -> dict:
        entradas = FluxoCaixaRepository.entradas_por_periodo(data_inicio, data_fim)
        saidas = FluxoCaixaRepository.saidas_por_periodo(data_inicio, data_fim)

        return {
            "periodo": f"{data_inicio} a {data_fim}",
            "entradas": entradas,
            "saidas": saidas,
            "saldo": entradas - saidas
        }