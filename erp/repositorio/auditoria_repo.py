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

    @staticmethod
    def listar_por_usuario(usuario_id: int, limit: int = 100):
        sql = """
            SELECT
                id,
                usuario_id,
                email_usuario,
                acao,
                recurso,
                detalhes,
                ip_origem,
                criado_em
            FROM auditoria
            WHERE usuario_id = %s
            ORDER BY criado_em DESC
            LIMIT %s
        """
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (usuario_id, limit))
            return cursor.fetchall()

    @staticmethod
    def listar_com_filtros(
        usuario_id: int | None = None,
        acao: str | None = None,
        data_inicio: str | None = None,
        data_fim: str | None = None,
        limit: int = 100
    ):
        sql = """
            SELECT
                id,
                usuario_id,
                email_usuario,
                acao,
                recurso,
                detalhes,
                ip_origem,
                criado_em
            FROM auditoria
            WHERE 1 = 1
        """
        params = []

        if usuario_id:
            sql += " AND usuario_id = %s"
            params.append(usuario_id)

        if acao:
            sql += " AND acao = %s"
            params.append(acao)

        if data_inicio:
            sql += " AND criado_em >= %s"
            params.append(data_inicio)

        if data_fim:
            sql += " AND criado_em <= %s"
            params.append(data_fim)

        sql += " ORDER BY criado_em DESC LIMIT %s"
        params.append(limit)

        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, tuple(params))
            return cursor.fetchall()