import bcrypt
from erp.repositorio.usuario_repo import UsuarioRepository
from erp.servico.token_servico import TokenServico
from erp.servico.auditoria_servico import AuditoriaServico


class UsuarioServico:

    @staticmethod
    def criar_usuario(nome: str, email: str, senha_plana: str) -> int:
        senha_hash = bcrypt.hashpw(
            senha_plana.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        return UsuarioRepository.criar_usuario(nome, email, senha_hash)

    @staticmethod
    def autenticar(email: str, senha_plana: str):
        usuario = UsuarioRepository.obter_por_email(email)
        if not usuario:
            return None

        senha_ok = bcrypt.checkpw(
            senha_plana.encode("utf-8"),
            usuario["senha_hash"].encode("utf-8")
        )

        if not senha_ok:
            return None

        papeis = UsuarioRepository.papeis_do_usuario(usuario["id"])
        usuario["papeis"] = papeis
        return usuario

    @staticmethod
    def autenticar_com_token(email: str, senha_plana: str):
        usuario = UsuarioServico.autenticar(email, senha_plana)
        if not usuario:
            return None

        token = TokenServico.gerar_token(usuario)

        # ✅ AUDITORIA CORRETA – dentro do método, onde "usuario" existe
        AuditoriaServico.auditar(
            usuario=usuario,
            acao="LOGIN",
            recurso="autenticacao",
            detalhes="Login efetuado com sucesso"
        )

        return {
            "usuario": {
                "id": usuario["id"],
                "nome": usuario["nome"],
                "email": usuario["email"],
                "papeis": usuario["papeis"]
            },
            "token": token
        }
    
    @staticmethod
    def criar_usuario_com_papel(
        nome: str,
        email: str,
        senha_plana: str,
        papel_nome: str
    ) -> int:
        # 1. Criar usuário
        usuario_id = UsuarioServico.criar_usuario(
            nome=nome,
            email=email,
            senha_plana=senha_plana
        )

        # 2. Buscar ID do papel
        papel_id = UsuarioRepository.obter_papel_por_nome(papel_nome)
        if not papel_id:
            raise ValueError(f"Papel '{papel_nome}' não existe")

        # 3. Vincular papel
        UsuarioRepository.vincular_papel(usuario_id, papel_id)

        return usuario_id
    
    @staticmethod
    def listar_usuarios():
        return UsuarioRepository.listar_usuarios()
    
    @staticmethod
    def alterar_papel_usuario(usuario_id: int, papel_nome: str):
        papel_id = UsuarioRepository.obter_papel_por_nome(papel_nome)
        if not papel_id:
            raise ValueError(f"Papel '{papel_nome}' não existe")

        UsuarioRepository.atualizar_papel(usuario_id, papel_id)

    @staticmethod
    def trocar_senha(
        usuario_id: int,
        senha_atual: str,
        nova_senha: str
    ):
        usuario = UsuarioRepository.obter_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado")

        # Validar senha atual
        senha_ok = bcrypt.checkpw(
            senha_atual.encode("utf-8"),
            usuario["senha_hash"].encode("utf-8")
        )

        if not senha_ok:
            raise ValueError("Senha atual incorreta")

        # Gerar hash da nova senha
        nova_hash = bcrypt.hashpw(
            nova_senha.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        UsuarioRepository.atualizar_senha(usuario_id, nova_hash)

    @staticmethod
    def obter_por_id(usuario_id: int):
        sql = "SELECT * FROM usuarios WHERE id = %s"
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (usuario_id,))
            return cursor.fetchone()
        
    @staticmethod
    def resetar_senha_admin(usuario_id: int, nova_senha: str):
        usuario = UsuarioRepository.obter_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado")

        senha_hash = bcrypt.hashpw(
            nova_senha.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        UsuarioRepository.atualizar_senha(usuario_id, senha_hash)

    @staticmethod
    def inativar_usuario(usuario_id: int):
        usuario = UsuarioRepository.obter_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado")

        UsuarioRepository.inativar_usuario(usuario_id)

    @staticmethod
    def reativar_usuario(usuario_id: int):
        usuario = UsuarioRepository.obter_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado")

        UsuarioRepository.reativar_usuario(usuario_id)

    @staticmethod
    def obter_me(usuario_id: int):
        usuario = UsuarioRepository.obter_perfil(usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado")

        # Anexar papéis
        papeis = UsuarioRepository.papeis_do_usuario(usuario_id)
        usuario["papeis"] = papeis

        return usuario
    
    @staticmethod
    def listar_usuarios_paginado(
        page: int,
        page_size: int,
        order_by: str,
        order_dir: str
    ):
        return UsuarioRepository.listar_usuarios_paginado(
            page, page_size, order_by, order_dir
        )
