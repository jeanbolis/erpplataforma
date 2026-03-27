from erp.servico.usuario_servico import UsuarioServico
from erp.servico.token_servico import TokenServico
import time


def main():
    print("=== TESTE JWT ===")

    email = f"jwt_{int(time.time())}@empresa.com"

    UsuarioServico.criar_usuario(
        nome="Usuario JWT",
        email=email,
        senha_plana="123456"
    )

    # Vincular papel manualmente se necessário via SQL ou teste anterior

    resultado = UsuarioServico.autenticar_com_token(
        email=email,
        senha_plana="123456"
    )

    if not resultado:
        print("Falha no login")
        return

    print("Usuário autenticado:", resultado["usuario"])
    print("Token JWT:", resultado["token"])

    # Validar token
    payload = TokenServico.validar_token(resultado["token"])
    print("Payload decodificado:", payload)


if __name__ == "__main__":
    main()