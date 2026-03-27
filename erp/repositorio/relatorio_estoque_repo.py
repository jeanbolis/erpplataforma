from erp.db import get_connection


class RelatorioEstoqueRepository:

    @staticmethod
    def estoque_atual():
        sql = """
            SELECT
                p.id,
                p.codigo,
                p.nome,
                COALESCE(
                    SUM(
                        CASE
                            WHEN e.tipo_movimentacao = 'ENTRADA' THEN e.quantidade
                            WHEN e.tipo_movimentacao = 'SAIDA' THEN -e.quantidade
                        END
                    ), 0
                ) AS saldo
            FROM produtos p
            LEFT JOIN estoque_movimentacoes e
                ON e.produto_id = p.id
            WHERE p.ativo = 1
            GROUP BY p.id, p.codigo, p.nome
            ORDER BY p.nome
        """

        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            return cursor.fetchall()