from erp.db import get_connection


class RelatorioVendasRepository:

    @staticmethod
    def vendas_por_periodo(data_inicio: str, data_fim: str):
        sql = """
            SELECT
                v.id AS venda_id,
                v.cliente,
                v.data_venda,
                COUNT(vi.id) AS qtd_itens,
                SUM(vi.quantidade) AS total_itens
            FROM vendas v
            JOIN vendas_itens vi
                ON vi.venda_id = v.id
            WHERE v.data_venda BETWEEN %s AND %s
            GROUP BY v.id, v.cliente, v.data_venda
            ORDER BY v.data_venda
        """

        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (data_inicio, data_fim))
            return cursor.fetchall()