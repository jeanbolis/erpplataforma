import time
from erp.repositorio.produto_repo import ProdutoRepository


def main():
    codigo = f"P{int(time.time())}"

    print("=== CRIANDO PRODUTO ===")
    produto_id = ProdutoRepository.criar({
        "codigo": codigo,
        "nome": "Produto CRUD",
        "descricao": "Produto para testar CRUD",
        "sku": f"SKU-{codigo}"
    })
    print("Produto criado com ID:", produto_id)

    print("\n=== LISTANDO PRODUTOS ===")
    for p in ProdutoRepository.listar_ativos():
        print(p)

    print("\n=== BUSCANDO 'CRUD' ===")
    encontrados = ProdutoRepository.buscar("CRUD")
    for p in encontrados:
        print(p)

    print("\n=== ATUALIZANDO PRODUTO ===")
    
    ProdutoRepository.atualizar(produto_id, {
    "codigo": codigo,
    "nome": "Produto CRUD Atualizado",
    "descricao": "Produto atualizado com sucesso",
    "sku": f"SKU-{codigo}"

    })

    print("\nProduto após atualização:")
    for p in ProdutoRepository.buscar("Atualizado"):
        print(p)

    print("\n=== EXCLUINDO PRODUTO (DELETE LÓGICO) ===")
    ProdutoRepository.excluir(produto_id)

    print("\nProdutos ativos após exclusão:")
    for p in ProdutoRepository.listar_ativos():
        print(p)


if __name__ == "__main__":
    main()