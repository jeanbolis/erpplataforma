import jwt
from datetime import datetime, timedelta
from erp.seguranca import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRACAO_MINUTOS


class TokenServico:

    @staticmethod
    def gerar_token(usuario: dict) -> str:
        payload = {
            "sub": str(usuario["id"]),  # ✅ agora é string
            "email": usuario["email"],
            "papeis": usuario["papeis"],
            "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRACAO_MINUTOS)
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token

    @staticmethod
    def validar_token(token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                JWT_SECRET,
                algorithms=[JWT_ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expirado")
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Token inválido: {e}")