from erp.repositorio.financeiro_repo import FinanceiroRepository
from datetime import date, timedelta
from erp.repositorio.financeiro_repo import FinanceiroRepository


class FinanceiroServico:
    """
    Serviço de regras financeiras
    """

    @staticmethod
    def gerar_conta_pagar(
        compra_id: int,
        fornecedor: str,
        valor: float,
        dias_para_vencimento: int = 30
    ):
        data_vencimento = date.today() + timedelta(days=dias_para_vencimento)

        FinanceiroRepository.criar_conta_pagar(
            referencia_tipo="COMPRA",
            referencia_id=compra_id,
            fornecedor=fornecedor,
            valor=valor,
            data_vencimento=data_vencimento
        )

    @staticmethod
    def gerar_conta_receber(
        venda_id: int,
        cliente: str,
        valor: float,
        dias_para_vencimento: int = 30
    ):
        data_vencimento = date.today() + timedelta(days=dias_para_vencimento)

        FinanceiroRepository.criar_conta_receber(
            referencia_tipo="VENDA",
            referencia_id=venda_id,
            cliente=cliente,
            valor=valor,
            data_vencimento=data_vencimento
        )

        # ---------- BAIXA ----------
    @staticmethod
    def pagar_conta(conta_pagar_id: int):
        """
        Marca uma conta a pagar como paga
        """
        FinanceiroRepository.baixar_conta_pagar(conta_pagar_id)

    @staticmethod
    def receber_conta(conta_receber_id: int):
        """
        Marca uma conta a receber como recebida
        """
        FinanceiroRepository.baixar_conta_receber(conta_receber_id)