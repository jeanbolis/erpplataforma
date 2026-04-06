from fastapi import APIRouter, Depends, HTTPException, Query
from erp.api.deps import get_usuario_autorizado
from erp.servico.auditoria_servico import AuditoriaServico
from erp.utils.exportacao import exportar_csv, exportar_excel

router = APIRouter(
    prefix="/auditoria",
    tags=["Auditoria"]
)

# ============================================================
# EXPORTAÇÕES (CSV / EXCEL) — COM FILTROS
# ============================================================

@router.get("/export/csv")
def exportar_auditoria_csv(
    usuario_id: int | None = Query(None),
    acao: str | None = Query(None),
    email_usuario: str | None = Query(None),
    data_inicio: str | None = Query(None),
    data_fim: str | None = Query(None),
    usuario_logado=Depends(get_usuario_autorizado("qualquer"))
):
    usuario_logado_id = int(usuario_logado["sub"])
    papeis = usuario_logado["papeis"]

    # Usuário comum só exporta a própria auditoria
    if "ADMIN" not in papeis:
        usuario_id = usuario_logado_id
        email_usuario = None  # evita tentar filtrar outros usuários

    dados = AuditoriaServico.listar_auditoria_filtrada(
        usuario_id=usuario_id,
        acao=acao,
        email_usuario=email_usuario,
        data_inicio=data_inicio,
        data_fim=data_fim,
        page=1,
        page_size=100_000,
        order_by="criado_em",
        order_dir="DESC",
    )

    return exportar_csv("auditoria.csv", dados)


@router.get("/export/excel")
def exportar_auditoria_excel(
    usuario_id: int | None = Query(None),
    acao: str | None = Query(None),
    email_usuario: str | None = Query(None),
    data_inicio: str | None = Query(None),
    data_fim: str | None = Query(None),
    usuario_logado=Depends(get_usuario_autorizado("qualquer"))
):
    usuario_logado_id = int(usuario_logado["sub"])
    papeis = usuario_logado["papeis"]

    if "ADMIN" not in papeis:
        usuario_id = usuario_logado_id
        email_usuario = None

    dados = AuditoriaServico.listar_auditoria_filtrada(
        usuario_id=usuario_id,
        acao=acao,
        email_usuario=email_usuario,
        data_inicio=data_inicio,
        data_fim=data_fim,
        page=1,
        page_size=100_000,
        order_by="criado_em",
        order_dir="DESC",
    )

    return exportar_excel("auditoria.xlsx", dados)


# ============================================================
# LISTAGEM GERAL — FILTROS + PAGINAÇÃO
# ============================================================

@router.get("")
def listar_auditoria(
    usuario_id: int | None = Query(None),
    acao: str | None = Query(None),
    email_usuario: str | None = Query(None),
    data_inicio: str | None = Query(None),
    data_fim: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    usuario_logado=Depends(get_usuario_autorizado("qualquer"))
):
    usuario_logado_id = int(usuario_logado["sub"])
    papeis = usuario_logado["papeis"]

    # Usuário comum só vê a própria auditoria
    if "ADMIN" not in papeis:
        usuario_id = usuario_logado_id
        email_usuario = None

    return AuditoriaServico.listar_auditoria_filtrada(
        usuario_id=usuario_id,
        acao=acao,
        email_usuario=email_usuario,
        data_inicio=data_inicio,
        data_fim=data_fim,
        page=page,
        page_size=page_size,
        order_by="criado_em",
        order_dir="DESC",
    )


# ============================================================
# AUDITORIA POR USUÁRIO (ROTA ESPECÍFICA)
# ============================================================

@router.get("/usuario/{usuario_id}")
def listar_auditoria_usuario(
    usuario_id: int,
    usuario_logado=Depends(get_usuario_autorizado("qualquer")),
    limit: int = Query(100, ge=1, le=500)
):
    usuario_logado_id = int(usuario_logado["sub"])
    papeis = usuario_logado["papeis"]

    if "ADMIN" not in papeis and usuario_logado_id != usuario_id:
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para acessar a auditoria deste usuário"
        )

    return AuditoriaServico.listar_auditoria_por_usuario(usuario_id, limit)