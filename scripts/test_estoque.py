from erp.repositorio.estoque_repo import EstoqueRepository
from erp.repositorio.produto_repo import ProdutoRepository
from erp.excecoes import EstoqueInsuficienteError


def main():
    print("=== TESTE DE ESTOQUE COM VALIDAÇÃO ===")

    produto_id = ProdutoRepository.criar({
        "codigo": "ESTVAL001",
        "nome": "Produto Estoque Validação"
    })
    print("Produto criado:", produto_id)

    EstoqueRepository.entrada(produto_id, 50, origem="Compra")
    print("Entrada de 50 unidades")

    try:
        EstoqueRepository.saida(produto_id, 60, origem="Venda")
    except EstoqueInsuficienteError as e:
        print("❌ ERRO:", e)

    EstoqueRepository.saida(produto_id, 20, origem="Venda")
    print("Saída de 20 unidades permitida")

    saldo = EstoqueRepository.saldo_por_produto(produto_id)
    print("Saldo final:", saldo)


if __name__ == "__main__":
    main()