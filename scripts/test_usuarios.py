import time
from erp.servico.usuario_servico import UsuarioServico
from erp.servico.autorizacao_servico import AutorizacaoServico
from erp.repositorio.usuario_repo import UsuarioRepository


def main():
    print("=== TESTE DE USUÁRIOS ===")

    email = f"financeiro_{int(time.time())}@empresa.com"

    usuario_id = UsuarioServico.criar_usuario(
        nome="Usuario Financeiro",
        email=email,
        senha_plana="123456"
    )
    print("Usuário criado:", usuario_id)

    # 🔑 buscar papel FINANCEIRO
    papel_id = UsuarioRepository.obter_papel_por_nome("FINANCEIRO")

    # 🔗 vincular papel ao usuário recém-criado
    UsuarioRepository.vincular_papel(usuario_id, papel_id)

    # 🔐 autenticar
    usuario = UsuarioServico.autenticar(
        email=email,
        senha_plana="123456"
    )

    print("Usuário autenticado:", usuario["nome"])
    print("Papéis:", usuario["papeis"])

    print(
        "Pode acessar financeiro?",
        AutorizacaoServico.pode_acessar(usuario["papeis"], "financeiro")
    )

    print(
        "Pode acessar vendas?",
        AutorizacaoServico.pode_acessar(usuario["papeis"], "vendas")
    )


if __name__ == "__main__":
    main()