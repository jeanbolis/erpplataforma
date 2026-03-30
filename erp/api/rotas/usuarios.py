from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from erp.api.deps import get_usuario_autorizado
from erp.servico.usuario_servico import UsuarioServico
from erp.servico.auditoria_servico import AuditoriaServico
from pydantic import BaseModel



router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


class UsuarioCreateRequest(BaseModel):
    nome: str
    email: str
    senha: str
    papel: str


@router.post("")
def criar_usuario(
    dados: UsuarioCreateRequest,
    usuario_logado=Depends(get_usuario_autorizado("admin"))
):
    try:
        usuario_id = UsuarioServico.criar_usuario_com_papel(
            nome=dados.nome,
            email=dados.email,
            senha_plana=dados.senha,
            papel_nome=dados.papel
        )

        # Auditoria
        AuditoriaServico.auditar(
            usuario=usuario_logado,
            acao="CRIAR_USUARIO",
            recurso="usuarios",
            detalhes=f"Usuário '{dados.email}' criado com papel '{dados.papel}'"
        )

        return {
            "id": usuario_id,
            "mensagem": "Usuário criado com sucesso"
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("")
def listar_usuarios(
    usuario_logado=Depends(get_usuario_autorizado("admin"))
    ):
    return UsuarioServico.listar_usuarios()



class AlterarPapelRequest(BaseModel):
    papel: str


@router.put("/{usuario_id}/papel")
def alterar_papel(
    usuario_id: int,
    dados: AlterarPapelRequest,
    usuario_logado=Depends(get_usuario_autorizado("admin"))
):
    try:
        UsuarioServico.alterar_papel_usuario(usuario_id, dados.papel)

        AuditoriaServico.auditar(
            usuario=usuario_logado,
            acao="ALTERAR_PAPEL",
            recurso="usuarios",
            detalhes=f"Papel do usuário {usuario_id} alterado para '{dados.papel}'"
        )

        return {
            "mensagem": "Papel do usuário atualizado com sucesso"
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
class TrocaSenhaRequest(BaseModel):
    senha_atual: str
    nova_senha: str

@router.put("/{usuario_id}/senha")
def trocar_senha(
    usuario_id: int,
    dados: TrocaSenhaRequest,
    usuario_logado=Depends(get_usuario_autorizado("qualquer"))
):
    # Só pode trocar a própria senha
    if int(usuario_logado["sub"]) != usuario_id:
        raise HTTPException(status_code=403, detail="Você só pode trocar sua própria senha")

    try:
        UsuarioServico.trocar_senha(
            usuario_id=usuario_id,
            senha_atual=dados.senha_atual,
            nova_senha=dados.nova_senha
        )

        AuditoriaServico.auditar(
            usuario=usuario_logado,
            acao="TROCAR_SENHA",
            recurso="usuarios",
            detalhes="Senha alterada pelo próprio usuário"
        )

        return {"mensagem": "Senha alterada com sucesso"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

    
class ResetSenhaRequest(BaseModel):
    nova_senha: str

@router.put("/{usuario_id}/senha-reset")
def resetar_senha_admin(
    usuario_id: int,
    dados: ResetSenhaRequest,
    usuario_logado=Depends(get_usuario_autorizado("admin"))
):
    try:
        UsuarioServico.resetar_senha_admin(
            usuario_id=usuario_id,
            nova_senha=dados.nova_senha
        )

        AuditoriaServico.auditar(
            usuario=usuario_logado,
            acao="RESETAR_SENHA",
            recurso="usuarios",
            detalhes=f"Senha do usuário {usuario_id} redefinida por ADMIN"
        )

        return {"mensagem": "Senha redefinida com sucesso"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/{usuario_id}/inativar")
def inativar_usuario(
    usuario_id: int,
    usuario_logado=Depends(get_usuario_autorizado("admin"))
):
    # ADMIN não pode se auto-inativar
    if int(usuario_logado["sub"]) == usuario_id:
        raise HTTPException(
            status_code=400,
            detail="Você não pode inativar o próprio usuário"
        )

    try:
        UsuarioServico.inativar_usuario(usuario_id)

        AuditoriaServico.auditar(
            usuario=usuario_logado,
            acao="INATIVAR_USUARIO",
            recurso="usuarios",
            detalhes=f"Usuário {usuario_id} inativado"
        )

        return {"mensagem": "Usuário inativado com sucesso"}

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.put("/{usuario_id}/reativar")
def reativar_usuario(
    usuario_id: int,
    usuario_logado=Depends(get_usuario_autorizado("admin"))
):
    try:
        UsuarioServico.reativar_usuario(usuario_id)

        AuditoriaServico.auditar(
            usuario=usuario_logado,
            acao="REATIVAR_USUARIO",
            recurso="usuarios",
            detalhes=f"Usuário {usuario_id} reativado"
        )

        return {"mensagem": "Usuário reativado com sucesso"}

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/me")
def meu_perfil(
    usuario_logado=Depends(get_usuario_autorizado("qualquer"))
):
    try:
        usuario_id = int(usuario_logado["sub"])
        return UsuarioServico.obter_me(usuario_id)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("")
def listar_auditoria(
    usuario_id: int | None = None,
    acao: str | None = None,
    data_inicio: str | None = None,
    data_fim: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    order_by: str = Query("criado_em"),
    order_dir: str = Query("desc"),
    usuario_logado=Depends(get_usuario_autorizado("qualquer"))
):
    usuario_logado_id = int(usuario_logado["sub"])
    papeis = usuario_logado["papeis"]

    if "ADMIN" not in papeis:
        usuario_id = usuario_logado_id

    return AuditoriaServico.listar_auditoria_filtrada(
        usuario_id=usuario_id,
        acao=acao,
        data_inicio=data_inicio,
        data_fim=data_fim,
        page=page,
        page_size=page_size,
        order_by=order_by,
        order_dir=order_dir
    )    

@router.get("")
def listar_usuarios(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    order_by: str = Query("id"),
    order_dir: str = Query("asc"),
    usuario_logado=Depends(get_usuario_autorizado("admin"))
):
    return UsuarioServico.listar_usuarios_paginado(
        page, page_size, order_by, order_dir
    )
    