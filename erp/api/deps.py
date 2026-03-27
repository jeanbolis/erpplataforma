from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from erp.middleware.autorizacao_jwt import MiddlewareAutorizacaoJWT
from erp.excecoes.autorizacao_excecoes import (
    TokenInvalidoError,
    NaoAutorizadoError
)

security = HTTPBearer()


def get_usuario_autorizado(recurso: str):
    def _verificar(
        credentials: HTTPAuthorizationCredentials = Security(security)
    ):
        token = credentials.credentials

        try:
            payload = MiddlewareAutorizacaoJWT.verificar(token, recurso)
            return payload
        except TokenInvalidoError as e:
            raise HTTPException(status_code=401, detail=str(e))
        except NaoAutorizadoError as e:
            raise HTTPException(status_code=403, detail=str(e))

    return _verificar