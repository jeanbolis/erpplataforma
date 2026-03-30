from erp.db import get_connection


class UsuarioRepository:

    @staticmethod
    def criar_usuario(nome: str, email: str, senha_hash: str) -> int:
        sql = """
            INSERT INTO usuarios (nome, email, senha_hash)
            VALUES (%s, %s, %s)
        """
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, (nome, email, senha_hash))
            return cur.lastrowid

    @staticmethod
    def obter_por_email(email: str):
        sql = "SELECT * FROM usuarios WHERE email = %s AND ativo = 1"

        with get_connection() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, (email,))
            return cur.fetchone()


    @staticmethod
    def vincular_papel(usuario_id: int, papel_id: int):
        sql = "INSERT INTO usuario_papel (usuario_id, papel_id) VALUES (%s, %s)"
        with get_connection() as conn:
            conn.cursor().execute(sql, (usuario_id, papel_id))

    @staticmethod
    def papeis_do_usuario(usuario_id: int):
        sql = """
            SELECT p.nome
            FROM papeis p
            JOIN usuario_papel up ON up.papel_id = p.id
            WHERE up.usuario_id = %s
        """
        with get_connection() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, (usuario_id,))
            return [r["nome"] for r in cur.fetchall()]
    
    @staticmethod
    def obter_papel_por_nome(nome: str):
        sql = "SELECT id FROM papeis WHERE nome = %s"
        with get_connection() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, (nome,))
            row = cur.fetchone()
            return row["id"] if row else None
        
    @staticmethod
    def listar_usuarios():
        sql = """
            SELECT
                u.id,
                u.nome,
                u.email,
                u.ativo,
                GROUP_CONCAT(p.nome ORDER BY p.nome SEPARATOR ', ') AS papeis
            FROM usuarios u
            LEFT JOIN usuario_papel up ON up.usuario_id = u.id
            LEFT JOIN papeis p ON p.id = up.papel_id
            GROUP BY u.id, u.nome, u.email, u.ativo
            ORDER BY u.id
        """

        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            return cursor.fetchall()
        
    @staticmethod
    def atualizar_papel(usuario_id: int, papel_id: int):
        sql_remover = "DELETE FROM usuario_papel WHERE usuario_id = %s"
        sql_inserir = """
            INSERT INTO usuario_papel (usuario_id, papel_id)
            VALUES (%s, %s)
        """

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_remover, (usuario_id,))
            cursor.execute(sql_inserir, (usuario_id, papel_id))

    @staticmethod
    def atualizar_senha(usuario_id: int, senha_hash: str):
        sql = "UPDATE usuarios SET senha_hash = %s WHERE id = %s"

        with get_connection() as conn:
            conn.cursor().execute(sql, (senha_hash, usuario_id))

    @staticmethod
    def obter_por_id(usuario_id: int):
        sql = "SELECT * FROM usuarios WHERE id = %s"
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (usuario_id,))
            return cursor.fetchone()
        
    @staticmethod
    def inativar_usuario(usuario_id: int):
        sql = "UPDATE usuarios SET ativo = 0 WHERE id = %s"

        with get_connection() as conn:
            conn.cursor().execute(sql, (usuario_id,))