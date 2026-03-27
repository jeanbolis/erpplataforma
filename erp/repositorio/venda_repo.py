from erp.db import get_connection


class VendaRepository:

    @staticmethod
    def criar_venda(cliente: str, data_venda: str, observacao: str = None) -> int:
        sql = """
            INSERT INTO vendas (cliente, data_venda, observacao)
            VALUES (%s, %s, %s)
        """

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (cliente, data_venda, observacao))
            return cursor.lastrowid

    @staticmethod
    def adicionar_item(venda_id: int, produto_id: int, quantidade: float):
        sql = """
            INSERT INTO vendas_itens (venda_id, produto_id, quantidade)
            VALUES (%s, %s, %s)
        """

        with get_connection() as conn:
            conn.cursor().execute(sql, (venda_id, produto_id, quantidade))