from erp.db import get_connection
from erp.db import get_connection
from datetime import date


class FinanceiroRepository:

    @staticmethod
    def criar_conta_pagar(
        referencia_tipo: str,
        referencia_id: int,
        fornecedor: str,
        valor: float,
        data_vencimento: str
    ):
        sql = """
            INSERT INTO contas_pagar
            (referencia_tipo, referencia_id, fornecedor, valor, data_vencimento)
            VALUES (%s, %s, %s, %s, %s)
        """

        with get_connection() as conn:
            conn.cursor().execute(
                sql,
                (referencia_tipo, referencia_id, fornecedor, valor, data_vencimento)
            )

    @staticmethod
    def criar_conta_receber(
        referencia_tipo: str,
        referencia_id: int,
        cliente: str,
        valor: float,
        data_vencimento: str
    ):
        sql = """
            INSERT INTO contas_receber
            (referencia_tipo, referencia_id, cliente, valor, data_vencimento)
            VALUES (%s, %s, %s, %s, %s)
        """

        with get_connection() as conn:
            conn.cursor().execute(
                sql,
                (referencia_tipo, referencia_id, cliente, valor, data_vencimento)
            )

    # --- conta a pagar ---
    @staticmethod
    def baixar_conta_pagar(conta_id: int):
        sql = """
            UPDATE contas_pagar
            SET status = 'PAGO',
                data_baixa = %s
            WHERE id = %s
              AND status = 'ABERTO'
        """

        with get_connection() as conn:
            conn.cursor().execute(sql, (date.today(), conta_id))

    # --- conta a receber ---
    @staticmethod
    def baixar_conta_receber(conta_id: int):
        sql = """
            UPDATE contas_receber
            SET status = 'RECEBIDO',
                data_baixa = %s
            WHERE id = %s
              AND status = 'ABERTO'
        """

        with get_connection() as conn:
            conn.cursor().execute(sql, (date.today(), conta_id))