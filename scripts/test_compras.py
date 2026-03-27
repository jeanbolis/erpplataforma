from erp.servico.compra_servico import CompraServico
from erp.servico.produto_servico import ProdutoServico
from erp.servico.estoque_servico import EstoqueServico
import time


def main():
    print("=== TESTE DE COMPRAS ===")

    # Criar produto
    codigo = f"COMP{int(time.time())}"
    produto_id = ProdutoServico.criar_produto({
        "codigo": codigo,
        "nome": "Produto Compra Teste"
    })

    print("Produto criado:", produto_id)

    # Registrar compra
    compra_id = CompraServico.registrar_compra(
        fornecedor="Fornecedor Teste Ltda",
        data_compra="2026-03-20",
        itens=[
            {"produto_id": produto_id, "quantidade": 100}
        ],
        observacao="Compra inicial de teste"
    )

    print("Compra registrada:", compra_id)

    # Conferir estoque
    saldo = EstoqueServico.consultar_saldo(produto_id)
    print("Saldo em estoque após compra:", saldo)


if __name__ == "__main__":
    main()