from fastapi import APIRouter, Depends, Query
from erp.api.deps import get_usuario_autorizado
from erp.servico.auditoria_servico import AuditoriaServico
from fastapi import Query


router = APIRouter(
    prefix="/auditoria",
    tags=["Auditoria"]
)


@router.get("")
def listar_auditoria(
    usuario=Depends(get_usuario_autorizado("financeiro")),
    limit: int = Query(100, ge=1, le=500)
):
    return AuditoriaServico.listar_auditorias(limit)

@router.get("/{usuario_id}")
def listar_auditoria_usuario(
    usuario_id: int,
    usuario_logado=Depends(get_usuario_autorizado("qualquer")),
    limit: int = Query(100, ge=1, le=500)
):
    usuario_logado_id = int(usuario_logado["sub"])
    papeis = usuario_logado.get("papeis", [])

    # Regra de acesso:
    # - ADMIN pode ver qualquer usuário
    # - usuário comum só vê a própria auditoria
    if "ADMIN" not in papeis and usuario_logado_id != usuario_id:
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para acessar a auditoria deste usuário"
        )

    return AuditoriaServico.listar_auditoria_por_usuario(usuario_id, limit)



@router.get("")
def listar_auditoria_filtrada(
    usuario_id: int | None = Query(None),
    acao: str | None = Query(None),
    data_inicio: str | None = Query(None),
    data_fim: str | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    usuario_logado=Depends(get_usuario_autorizado("qualquer"))
):
    usuario_logado_id = int(usuario_logado["sub"])
    papeis = usuario_logado.get("papeis", [])

    # Regra de acesso
    if "ADMIN" not in papeis:
        # usuário comum só pode ver a própria auditoria
        usuario_id = usuario_logado_id

    return AuditoriaServico.listar_auditoria_filtrada(
        usuario_id=usuario_id,
        acao=acao,
        data_inicio=data_inicio,
        data_fim=data_fim,
        limit=limit
    )