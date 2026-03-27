from erp.db import get_connection


class RelatorioFinanceiroRepository:

    @staticmethod
    def resumo_financeiro():
        sql = """
            SELECT
                (SELECT COALESCE(SUM(valor),0)
                 FROM contas_receber
                 WHERE status = 'ABERTO') AS receber_aberto,

                (SELECT COALESCE(SUM(valor),0)
                 FROM contas_receber
                 WHERE status = 'RECEBIDO') AS receber_baixado,

                (SELECT COALESCE(SUM(valor),0)
                 FROM contas_pagar
                 WHERE status = 'ABERTO') AS pagar_aberto,

                (SELECT COALESCE(SUM(valor),0)
                 FROM contas_pagar
                 WHERE status = 'PAGO') AS pagar_baixado
        """

        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            return cursor.fetchone()