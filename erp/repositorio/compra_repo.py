from erp.db import get_connection


class CompraRepository:

    @staticmethod
    def criar_compra(fornecedor: str, data_compra: str, observacao: str = None) -> int:
        sql = """
            INSERT INTO compras (fornecedor, data_compra, observacao)
            VALUES (%s, %s, %s)
        """

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (fornecedor, data_compra, observacao))
            return cursor.lastrowid

    @staticmethod
    def adicionar_item(compra_id: int, produto_id: int, quantidade: float):
        sql = """
            INSERT INTO compras_itens (compra_id, produto_id, quantidade)
            VALUES (%s, %s, %s)
        """

        with get_connection() as conn:
            conn.cursor().execute(sql, (compra_id, produto_id, quantidade))