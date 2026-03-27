from erp.db import get_connection


class AuditoriaRepository:

    @staticmethod
    def registrar(
        usuario_id: int,
        email_usuario: str,
        acao: str,
        recurso: str,
        detalhes: str = None,
        ip_origem: str = None
    ):
        sql = """
            INSERT INTO auditoria
            (usuario_id, email_usuario, acao, recurso, detalhes, ip_origem)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        with get_connection() as conn:
            conn.cursor().execute(
                sql,
                (usuario_id, email_usuario, acao, recurso, detalhes, ip_origem)
            )

    @staticmethod
    def listar(limit: int = 100):
        sql = """
            SELECT id, usuario_id, email_usuario,
                   acao, recurso, detalhes,
                   ip_origem, criado_em
            FROM auditoria
            ORDER BY criado_em DESC
            LIMIT %s
        """

        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (limit,))
            return cursor.fetchall()        