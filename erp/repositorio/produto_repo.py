from erp.db import get_connection


class ProdutoRepository:

    @staticmethod
    def criar(dados: dict) -> int:
        sql = """
            INSERT INTO produtos
            (codigo, nome, descricao, sku, ean, ncm, unidade)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        parametros = (
            dados["codigo"],
            dados["nome"],
            dados.get("descricao"),
            dados.get("sku"),
            dados.get("ean"),
            dados.get("ncm"),
            dados.get("unidade", "UN"),
        )

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, parametros)
            return cursor.lastrowid

    @staticmethod
    def listar_ativos():
        sql = "SELECT * FROM produtos WHERE ativo = 1 ORDER BY nome"

        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            return cursor.fetchall()
