from erp.repositorio.estoque_repo import EstoqueRepository
from erp.excecoes import EstoqueInsuficienteError


class EstoqueServico:
    """
    Camada de serviço para regras de negócio de estoque
    """

    @staticmethod
    def registrar_entrada(produto_id: int, quantidade: float, origem: str = None, observacao: str = None):
        if quantidade <= 0:
            raise ValueError("Quantidade de entrada deve ser maior que zero")

        EstoqueRepository.entrada(
            produto_id=produto_id,
            quantidade=quantidade,
            origem=origem,
            observacao=observacao
        )

    @staticmethod
    def registrar_saida(produto_id: int, quantidade: float, origem: str = None, observacao: str = None):
        if quantidade <= 0:
            raise ValueError("Quantidade de saída deve ser maior que zero")

        # Regra centralizada de negócio
        saldo_atual = EstoqueRepository.saldo_por_produto(produto_id)

        if quantidade > saldo_atual:
            raise EstoqueInsuficienteError(
                f"Saldo insuficiente. Saldo atual: {saldo_atual}, solicitado: {quantidade}"
            )

        EstoqueRepository.saida(
            produto_id=produto_id,
            quantidade=quantidade,
            origem=origem,
            observacao=observacao
        )

    @staticmethod
    def consultar_saldo(produto_id: int) -> float:
        return EstoqueRepository.saldo_por_produto(produto_id)