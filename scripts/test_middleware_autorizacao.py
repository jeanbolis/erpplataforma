from erp.servico.usuario_servico import UsuarioServico
from erp.middleware.autorizacao_jwt import MiddlewareAutorizacaoJWT
from erp.excecoes.autorizacao_excecoes import NaoAutorizadoError
import time


def acao_financeira_protegida(token: str):
    MiddlewareAutorizacaoJWT.verificar(token, recurso="financeiro")
    print("✅ Ação financeira executada com sucesso")


def main():
    print("=== TESTE MIDDLEWARE JWT ===")

    email = f"mid_{int(time.time())}@empresa.com"

    UsuarioServico.criar_usuario(
        nome="Usuario Financeiro",
        email=email,
        senha_plana="123456"
    )

    # (paper_id 2 = FINANCEIRO)
    # Vincule pelo SQL se necessário:
    # INSERT INTO usuario_papel (usuario_id, papel_id) VALUES (..., 2)

    login = UsuarioServico.autenticar_com_token(
        email=email,
        senha_plana="123456"
    )

    token = login["token"]

    try:
        acao_financeira_protegida(token)
    except NaoAutorizadoError as e:
        print("⛔", e)


if __name__ == "__main__":
    main()