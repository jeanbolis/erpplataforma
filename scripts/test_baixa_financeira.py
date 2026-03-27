from erp.servico.compra_servico import CompraServico
from erp.servico.venda_servico import VendaServico
from erp.servico.financeiro_servico import FinanceiroServico
from erp.servico.produto_servico import ProdutoServico
import time


def main():
    print("=== TESTE DE BAIXA FINANCEIRA ===")

    codigo = f"BAIXA{int(time.time())}"
    produto_id = ProdutoServico.criar_produto({
        "codigo": codigo,
        "nome": "Produto Baixa Financeira"
    })

    # COMPRA → gera conta a pagar
    compra_id = CompraServico.registrar_compra(
        fornecedor="Fornecedor Baixa",
        data_compra="2026-03-25",
        itens=[{"produto_id": produto_id, "quantidade": 10}]
    )
    print("Compra registrada:", compra_id)

    # VENDA → gera conta a receber
    venda_id = VendaServico.registrar_venda(
        cliente="Cliente Baixa",
        data_venda="2026-03-25",
        itens=[{"produto_id": produto_id, "quantidade": 5}]
    )
    print("Venda registrada:", venda_id)

    # ⚠️ IDs fictícios para exemplo didático:
    conta_pagar_id = 1
    conta_receber_id = 1

    # BAIXA FINANCEIRA
    FinanceiroServico.pagar_conta(conta_pagar_id)
    print("Conta a pagar baixada")

    FinanceiroServico.receber_conta(conta_receber_id)
    print("Conta a receber baixada")


if __name__ == "__main__":
    main()