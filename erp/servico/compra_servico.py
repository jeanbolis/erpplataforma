from erp.repositorio.compra_repo import CompraRepository
from erp.servico.estoque_servico import EstoqueServico
from erp.servico.financeiro_servico import FinanceiroServico


class CompraServico:
    """
    Serviço de negócio para Compras
    """

    @staticmethod
    def registrar_compra(
        fornecedor: str,
        data_compra: str,
        itens: list,
        observacao: str = None
    ) -> int:
        """
        itens = [
            {"produto_id": int, "quantidade": float}
        ]
        """
        
        # 1. Criar compra (cabeçalho)
        compra_id = CompraRepository.criar_compra(
            fornecedor=fornecedor,
            data_compra=data_compra,
            observacao=observacao
        )
        
        # 2. Para cada item da compra:
        for item in itens:
            produto_id = item["produto_id"]
            quantidade = item["quantidade"]

        # 2.1 Registrar itens e entrada de estoque
        CompraRepository.adicionar_item(
            compra_id=compra_id,
            produto_id=produto_id,
            quantidade=quantidade
        )

        # 2.2 Gerar ENTRADA automática no estoque
        EstoqueServico.registrar_entrada(
            produto_id=produto_id,
            quantidade=quantidade,
            origem="Compra",
            observacao=f"Compra #{compra_id}"
        )
        
        # 3 APÓS o loop → gerar financeiro
        # (regra: financeiro só nasce depois que a compra terminou)
        valor_total = sum(item["quantidade"] * 10 for item in itens)  # valor fictício

        FinanceiroServico.gerar_conta_pagar(
            compra_id=compra_id,
            fornecedor=fornecedor,
            valor=valor_total
        )


       #4 Retornar o ID da compra
        return compra_id
    
    
    
    
    