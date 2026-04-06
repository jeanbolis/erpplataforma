from erp.servico.token_servico import TokenServico
from erp.servico.autorizacao_servico import AutorizacaoServico
from erp.servico.auditoria_servico import AuditoriaServico
from erp.excecoes.autorizacao_excecoes import (
    NaoAutorizadoError,
    TokenInvalidoError
)



class MiddlewareAutorizacaoJWT:
    """
    Middleware de autorização baseado em JWT e papéis.
    """

    @staticmethod
    def verificar(token: str, recurso: str) -> dict:
        """
        Valida o token e verifica se o usuário pode acessar o recurso.
        Retorna o payload do token se autorizado.
        """

        if not token:
            raise TokenInvalidoError("Token não informado")

        try:
            payload = TokenServico.validar_token(token)
        except Exception as e:
            raise TokenInvalidoError(str(e))

        papeis = payload.get("papeis", [])

        autorizado = AutorizacaoServico.pode_acessar(papeis, recurso)
        if not autorizado:
            raise NaoAutorizadoError(
                f"Acesso negado ao recurso '{recurso}' para os papéis {papeis}"
            )
        
        AuditoriaServico.auditar(
            usuario_id=payload["sub"],
            email_usuario=payload["email"],
            acao="ACESSO",
            recurso=recurso,
            detalhes="Acesso autorizado via JWT"
        )
        return payload