class NaoAutorizadoError(Exception):
    """Usuário não tem permissão para acessar o recurso."""
    pass

class TokenInvalidoError(Exception):
    """Token JWT inválido ou expirado."""
    pass