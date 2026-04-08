import bcrypt
from fastapi import HTTPException
from erp.repositorio.usuario_repo import UsuarioRepository
from erp.servico.token_servico import TokenServico
from erp.servico.auditoria_servico import AuditoriaServico


class UsuarioServico:

    # =========================================
    # CRIAÇÃO / AUTENTICAÇÃO
    # =========================================

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

        AuditoriaServico.auditar(
            usuario_id=usuario["id"],
            email_usuario=usuario["email"],
            acao="LOGIN",
            recurso="auth",
            detalhes="Login efetuado com sucesso"
        )

        return {
            "usuario": {
                "id": usuario["id"],
                "nome": usuario["nome"],
                "email": usuario["email"],
                "papeis": usuario["papeis"],
            },
            "token": token
        }

    # =========================================
    # TROCA DE SENHA
    # =========================================

    @staticmethod
    def trocar_senha(
        usuario_alvo_id: int,
        nova_senha: str,
        usuario_logado: dict,
        senha_atual: str | None = None
    ):
        usuario = UsuarioRepository.obter_por_id(usuario_alvo_id)
        if not usuario:
            raise HTTPException(404, "Usuário não encontrado")

        usuario_logado_id = int(usuario_logado["sub"])
        papeis = usuario_logado.get("papeis", [])
        eh_admin = "ADMIN" in papeis

        if usuario_logado_id != usuario_alvo_id and not eh_admin:
            raise HTTPException(403, "Você só pode trocar sua própria senha")

        if usuario_logado_id == usuario_alvo_id:
            if not senha_atual:
                raise HTTPException(400, "Senha atual obrigatória")

            if not bcrypt.checkpw(
                senha_atual.encode(),
                usuario["senha_hash"].encode()
            ):
                raise HTTPException(400, "Senha atual incorreta")

        nova_hash = bcrypt.hashpw(
            nova_senha.encode(),
            bcrypt.gensalt()
        ).decode()

        UsuarioRepository.atualizar_senha(usuario_alvo_id, nova_hash)

    # =========================================
    # ATIVAR / INATIVAR
    # =========================================

    @staticmethod
    def inativar_usuario(usuario_alvo_id: int, usuario_logado: dict):
        usuario_logado_id = int(usuario_logado["sub"])
        papeis = usuario_logado.get("papeis", [])

        if "ADMIN" not in papeis:
            raise HTTPException(403, "Apenas ADMIN pode inativar usuários")

        if usuario_logado_id == usuario_alvo_id:
            raise HTTPException(403, "Você não pode inativar seu próprio usuário")

        UsuarioRepository.inativar_usuario(usuario_alvo_id)

    @staticmethod
    def reativar_usuario(usuario_alvo_id: int, usuario_logado: dict):
        papeis = usuario_logado.get("papeis", [])

        if "ADMIN" not in papeis:
            raise HTTPException(403, "Apenas ADMIN pode reativar usuários")

        UsuarioRepository.reativar_usuario(usuario_alvo_id)

        AuditoriaServico.auditar(
            usuario_id=int(usuario_logado["sub"]),
            email_usuario=usuario_logado["email"],
            acao="REATIVAR_USUARIO",
            recurso=f"usuarios/{usuario_alvo_id}",
            detalhes="Usuário reativado por ADMIN"
        )

    # =========================================
    # CONSULTAS
    # =========================================

    @staticmethod
    def listar_usuarios():
        return UsuarioRepository.listar_usuarios()

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

    @staticmethod
    def obter_me(usuario_id: int):
        usuario = UsuarioRepository.obter_perfil(usuario_id)
        if not usuario:
            raise HTTPException(404, "Usuário não encontrado")

        usuario["papeis"] = UsuarioRepository.papeis_do_usuario(usuario_id)
        return usuario