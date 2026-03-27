from erp.repositorio.produto_repo import ProdutoRepository


class ProdutoServico:
    """
    Camada de serviço para regras de negócio de produtos
    """

    @staticmethod
    def criar_produto(dados: dict) -> int:
        # Aqui no futuro podem entrar validações:
        # - código obrigatório
        # - nome obrigatório
        # - regras fiscais
        return ProdutoRepository.criar(dados)

    @staticmethod
    def listar_produtos_ativos():
        return ProdutoRepository.listar_ativos()

    @staticmethod
    def buscar_produtos(termo: str):
        return ProdutoRepository.buscar(termo)

    @staticmethod
    def atualizar_produto(produto_id: int, dados: dict):
        return ProdutoRepository.atualizar(produto_id, dados)

    @staticmethod
    def excluir_produto(produto_id: int):
        return ProdutoRepository.excluir(produto_id)