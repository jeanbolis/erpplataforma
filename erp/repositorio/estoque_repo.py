from erp.db import get_connection


class EstoqueRepository:

    # -------------------------
    # ENTRADA DE ESTOQUE
    # -------------------------
    @staticmethod
    def entrada(produto_id: int, quantidade: float, origem: str = None, observacao: str = None):
        sql = """
            INSERT INTO estoque_movimentacoes
            (produto_id, tipo_movimentacao, quantidade, origem, observacao)
            VALUES (%s, 'ENTRADA', %s, %s, %s)
        """

        with get_connection() as conn:
            conn.cursor().execute(sql, (produto_id, quantidade, origem, observacao))

    # -------------------------
    # SAÍDA DE ESTOQUE
    # -------------------------
    from erp.db import get_connection
from erp.excecoes import EstoqueInsuficienteError


class EstoqueRepository:

    @staticmethod
    def entrada(produto_id: int, quantidade: float, origem: str = None, observacao: str = None):
        sql = """
            INSERT INTO estoque_movimentacoes
            (produto_id, tipo_movimentacao, quantidade, origem, observacao)
            VALUES (%s, 'ENTRADA', %s, %s, %s)
        """

        with get_connection() as conn:
            conn.cursor().execute(sql, (produto_id, quantidade, origem, observacao))

    @staticmethod
    def saida(produto_id: int, quantidade: float, origem: str = None, observacao: str = None):
        saldo_atual = EstoqueRepository.saldo_por_produto(produto_id)

        if quantidade > saldo_atual:
            raise EstoqueInsuficienteError(
                f"Saldo insuficiente. Saldo atual: {saldo_atual}, saída solicitada: {quantidade}"
            )

        sql = """
            INSERT INTO estoque_movimentacoes
            (produto_id, tipo_movimentacao, quantidade, origem, observacao)
            VALUES (%s, 'SAIDA', %s, %s, %s)
        """

        with get_connection() as conn:
            conn.cursor().execute(sql, (produto_id, quantidade, origem, observacao))

    @staticmethod
    def saldo_por_produto(produto_id: int) -> float:
        sql = """
            SELECT
                SUM(
                    CASE
                        WHEN tipo_movimentacao = 'ENTRADA' THEN quantidade
                        WHEN tipo_movimentacao = 'SAIDA' THEN -quantidade
                    END
                ) AS saldo
            FROM estoque_movimentacoes
            WHERE produto_id = %s
        """

        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (produto_id,))
            resultado = cursor.fetchone()
            return resultado["saldo"] or 0
    # -------------------------
    # SALDO DE ESTOQUE
    # -------------------------
    @staticmethod
    def saldo_por_produto(produto_id: int) -> float:
        sql = """
            SELECT
                SUM(
                    CASE
                        WHEN tipo_movimentacao = 'ENTRADA' THEN quantidade
                        WHEN tipo_movimentacao = 'SAIDA' THEN -quantidade
                    END
                ) AS saldo
            FROM estoque_movimentacoes
            WHERE produto_id = %s
        """

        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (produto_id,))
            resultado = cursor.fetchone()

            return resultado["saldo"] or 0