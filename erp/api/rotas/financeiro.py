from fastapi import APIRouter, Depends
from erp.api.deps import get_usuario_autorizado
from erp.servico.relatorio_financeiro_servico import RelatorioFinanceiroServico

router = APIRouter(
    prefix="/financeiro",
    tags=["Financeiro"]
)


@router.get("/resumo")
def resumo_financeiro(
    usuario=Depends(get_usuario_autorizado("financeiro"))
):
    return RelatorioFinanceiroServico.resumo()