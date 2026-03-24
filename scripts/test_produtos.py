from erp.repositorio.produto_repo import ProdutoRepository


def main():
    produto = {
        "codigo": "P001",
        "nome": "Produto Teste ERP",
        "descricao": "Primeiro produto cadastrado no ERP"
    }

    produto_id = ProdutoRepository.criar(produto)
    print("Produto criado com ID:", produto_id)

    print("\nProdutos ativos cadastrados:")
    for p in ProdutoRepository.listar_ativos():
        print(p)


if __name__ == "__main__":
    main()