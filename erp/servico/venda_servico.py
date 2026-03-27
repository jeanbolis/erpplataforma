from erp.repositorio.venda_repo import VendaRepository
from erp.servico.estoque_servico import EstoqueServico


class VendaServico:
    """
    Serviço de negócio para Vendas
    """

    @staticmethod
    def registrar_venda(
        cliente: str,
        data_venda: str,
        itens: list,
        observacao: str = None
    ) -> int:
        """
        itens = [
            {"produto_id": int, "quantidade": float}
        ]
        """

        # 1. Criar venda
        venda_id = VendaRepository.criar_venda(
            cliente=cliente,
            data_venda=data_venda,
            observacao=observacao
        )

        # 2. Registrar itens e saída de estoque
        for item in itens:
            produto_id = item["produto_id"]
            quantidade = item["quantidade"]

            # Pode lançar EstoqueInsuficienteError
            EstoqueServico.registrar_saida(
                produto_id=produto_id,
                quantidade=quantidade,
                origem="Venda",
                observacao=f"Venda #{venda_id}"
            )

            VendaRepository.adicionar_item(
                venda_id=venda_id,
                produto_id=produto_id,
                quantidade=quantidade
            )

        return venda_id