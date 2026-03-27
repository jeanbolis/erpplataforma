from erp.servico.estoque_servico import EstoqueServico
from erp.servico.produto_servico import ProdutoServico
from erp.excecoes import EstoqueInsuficienteError
import time


def main():
    print("=== TESTE VIA CAMADA DE SERVIÇO ===")

    codigo = f"SERV{int(time.time())}"
    produto_id = ProdutoServico.criar_produto({
        "codigo": codigo,
        "nome": "Produto Serviço Estoque"
    })

    print("Produto criado:", produto_id)

    EstoqueServico.registrar_entrada(produto_id, 40, origem="Compra")
    print("Entrada de 40 unidades")

    try:
        EstoqueServico.registrar_saida(produto_id, 60, origem="Venda")
    except EstoqueInsuficienteError as e:
        print("❌ ERRO:", e)

    EstoqueServico.registrar_saida(produto_id, 15, origem="Venda")
    print("Saída de 15 unidades")

    saldo = EstoqueServico.consultar_saldo(produto_id)
    print("Saldo final:", saldo)


if __name__ == "__main__":
    main()