from fastapi import APIRouter, Depends
from erp.api.deps import get_usuario_autorizado
from erp.servico.relatorio_estoque_servico import RelatorioEstoqueServico
from fastapi import Security
from erp.api.security import security_bearer

dependencies=[Security(security_bearer)]

router = APIRouter(
    prefix="/estoque",
    tags=["Estoque"]
)


@router.get("/atual")
def estoque_atual(
    usuario=Depends(get_usuario_autorizado("estoque"))
):
    return RelatorioEstoqueServico.estoque_atual()