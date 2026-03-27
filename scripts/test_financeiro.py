from erp.servico.compra_servico import CompraServico
from erp.servico.venda_servico import VendaServico
from erp.servico.produto_servico import ProdutoServico
from erp.servico.estoque_servico import EstoqueServico
import time


def main():
    print("=== TESTE FINANCEIRO COMPLETO ===")

    codigo = f"FIN{int(time.time())}"
    produto_id = ProdutoServico.criar_produto({
        "codigo": codigo,
        "nome": "Produto Financeiro Teste"
    })

    print("Produto criado:", produto_id)

    # COMPRA (gera contas a pagar + entrada de estoque)
    compra_id = CompraServico.registrar_compra(
        fornecedor="Fornecedor Financeiro",
        data_compra="2026-03-22",
        itens=[
            {"produto_id": produto_id, "quantidade": 50}
        ],
        observacao="Compra teste financeiro"
    )
    print("Compra registrada:", compra_id)

    # VENDA (gera contas a receber + saída de estoque)
    venda_id = VendaServico.registrar_venda(
        cliente="Cliente Financeiro",
        data_venda="2026-03-23",
        itens=[
            {"produto_id": produto_id, "quantidade": 20}
        ],
        observacao="Venda teste financeiro"
    )
    print("Venda registrada:", venda_id)

    saldo = EstoqueServico.consultar_saldo(produto_id)
    print("Saldo de estoque final:", saldo)


if __name__ == "__main__":
    main()