from fastapi import APIRouter, Depends, Query
from erp.api.deps import get_usuario_autorizado
from erp.servico.auditoria_servico import AuditoriaServico

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