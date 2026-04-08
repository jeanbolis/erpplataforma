from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from erp.api.deps import get_usuario_autorizado
from erp.servico.usuario_servico import UsuarioServico
from erp.servico.auditoria_servico import AuditoriaServico

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)

# =====================================
# MODELS
# =====================================

class UsuarioCreateRequest(BaseModel):
    nome: str
    email: str
    senha: str
    papel: str


class AlterarPapelRequest(BaseModel):
    papel: str


class TrocaSenhaRequest(BaseModel):
    senha_atual: str | None = None
    nova_senha: str


# =====================================
# USUÁRIOS
# =====================================

@router.post("")
def criar_usuario(
    dados: UsuarioCreateRequest,
    usuario_logado=Depends(get_usuario_autorizado("ADMIN"))
):
    try:
        usuario_id = UsuarioServico.criar_usuario_com_papel(
            nome=dados.nome,
            email=dados.email,
            senha_plana=dados.senha,
            papel_nome=dados.papel
        )

        AuditoriaServico.auditar(
            usuario_id=int(usuario_logado["sub"]),
            email_usuario=usuario_logado["email"],
            acao="CRIAR_USUARIO",
            recurso="usuarios",
            detalhes=f"Usuário '{dados.email}' criado com papel '{dados.papel}'"
        )

        return {"id": usuario_id}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("")
def listar_usuarios(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    order_by: str = Query("id"),
    order_dir: str = Query("asc"),
    usuario_logado=Depends(get_usuario_autorizado("ADMIN"))
):
    return UsuarioServico.listar_usuarios_paginado(
        page, page_size, order_by, order_dir
    )


@router.put("/{usuario_id}/papel")
def alterar_papel(
    usuario_id: int,
    dados: AlterarPapelRequest,
    usuario_logado=Depends(get_usuario_autorizado("ADMIN"))
):
    try:
        UsuarioServico.alterar_papel_usuario(usuario_id, dados.papel)

        AuditoriaServico.auditar(
            usuario_id=int(usuario_logado["sub"]),
            email_usuario=usuario_logado["email"],
            acao="ALTERAR_PAPEL",
            recurso="usuarios",
            detalhes=f"Papel alterado para '{dados.papel}'"
        )

        return {"message": "Papel atualizado"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# =====================================
# TROCA DE SENHA (ÚNICA E CORRETA)
# =====================================

@router.put("/{usuario_id}/senha")
def trocar_senha(
    usuario_id: int,
    dados: TrocaSenhaRequest,
    usuario_logado=Depends(get_usuario_autorizado("qualquer"))
):
    UsuarioServico.trocar_senha(
        usuario_alvo_id=usuario_id,
        nova_senha=dados.nova_senha,
        usuario_logado=usuario_logado,
        senha_atual=dados.senha_atual
    )

    return {"message": "Senha alterada com sucesso"}


# =====================================
# ATIVAR / INATIVAR
# =====================================

@router.put("/{usuario_id}/inativar")
def inativar_usuario(
    usuario_id: int,
    usuario_logado=Depends(get_usuario_autorizado("ADMIN"))
):
    UsuarioServico.inativar_usuario(usuario_id, usuario_logado)
    return {"message": "Usuário inativado"}


@router.put("/{usuario_id}/reativar")
def reativar_usuario(
    usuario_id: int,
    usuario_logado=Depends(get_usuario_autorizado("ADMIN"))
):
    UsuarioServico.reativar_usuario(usuario_id, usuario_logado)

    return {"message": "Usuário reativado com sucesso"}

# =====================================
# PERFIL
# =====================================

@router.get("/me")
def meu_perfil(
    usuario_logado=Depends(get_usuario_autorizado("qualquer"))
):
    return UsuarioServico.obter_me(int(usuario_logado["sub"]))