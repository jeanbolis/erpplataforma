from erp.servico.venda_servico import VendaServico
from erp.servico.produto_servico import ProdutoServico
from erp.servico.estoque_servico import EstoqueServico
from erp.excecoes import EstoqueInsuficienteError
import time


def main():
    print("=== TESTE DE VENDAS ===")

    # Criar produto
    codigo = f"VENDA{int(time.time())}"
    produto_id = ProdutoServico.criar_produto({
        "codigo": codigo,
        "nome": "Produto Venda Teste"
    })

    print("Produto criado:", produto_id)

    # Entrada de estoque (simula compra prévia)
    EstoqueServico.registrar_entrada(produto_id, 50, origem="Compra")
    print("Estoque abastecido com 50 unidades")

    try:
        # Venda válida
        venda_id = VendaServico.registrar_venda(
            cliente="Cliente Teste",
            data_venda="2026-03-21",
            itens=[
                {"produto_id": produto_id, "quantidade": 30}
            ],
            observacao="Venda de teste"
        )

        print("Venda registrada:", venda_id)

    except EstoqueInsuficienteError as e:
        print("❌ ERRO AO VENDER:", e)

    saldo = EstoqueServico.consultar_saldo(produto_id)
    print("Saldo após venda:", saldo)


if __name__ == "__main__":
    main()