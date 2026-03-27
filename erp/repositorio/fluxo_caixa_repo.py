from erp.db import get_connection


class FluxoCaixaRepository:

    @staticmethod
    def entradas_por_periodo(data_inicio: str, data_fim: str) -> float:
        sql = """
            SELECT COALESCE(SUM(valor), 0) AS total
            FROM contas_receber
            WHERE status = 'RECEBIDO'
              AND data_baixa BETWEEN %s AND %s
        """

        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (data_inicio, data_fim))
            return cursor.fetchone()["total"]

    @staticmethod
    def saidas_por_periodo(data_inicio: str, data_fim: str) -> float:
        sql = """
            SELECT COALESCE(SUM(valor), 0) AS total
            FROM contas_pagar
            WHERE status = 'PAGO'
              AND data_baixa BETWEEN %s AND %s
        """

        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (data_inicio, data_fim))
            return cursor.fetchone()["total"]