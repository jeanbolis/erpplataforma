from erp.db import get_connection


class ProdutoRepository:

    # -------------------------
    # CREATE
    # -------------------------
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

    # -------------------------
    # READ - LISTAR ATIVOS
    # -------------------------
    @staticmethod
    def listar_ativos():
        sql = "SELECT * FROM produtos WHERE ativo = 1 ORDER BY nome"

        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            return cursor.fetchall()

    # -------------------------
    # READ - BUSCAR
    # -------------------------
    @staticmethod
    def buscar(termo: str):
        like = f"%{termo}%"

        sql = """
            SELECT * FROM produtos
            WHERE ativo = 1 AND (
                codigo LIKE %s OR
                nome LIKE %s OR
                sku LIKE %s OR
                ean LIKE %s
            )
            ORDER BY nome
        """

        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (like, like, like, like))
            return cursor.fetchall()

    # -------------------------
    # UPDATE
    # -------------------------
    @staticmethod
    def atualizar(produto_id: int, dados: dict):
        sql = """
            UPDATE produtos SET
                codigo = %s,
                nome = %s,
                descricao = %s,
                sku = %s,
                ean = %s,
                ncm = %s,
                unidade = %s
            WHERE id = %s
        """

        parametros = (
            dados["codigo"],
            dados["nome"],
            dados.get("descricao"),
            dados.get("sku"),
            dados.get("ean"),
            dados.get("ncm"),
            dados.get("unidade", "UN"),
            produto_id,
        )

        with get_connection() as conn:
            conn.cursor().execute(sql, parametros)

    # -------------------------
    # DELETE (LÓGICO)
    # -------------------------
    @staticmethod
    def excluir(produto_id: int):
        sql = "UPDATE produtos SET ativo = 0 WHERE id = %s"

        with get_connection() as conn:
            conn.cursor().execute(sql, (produto_id,))