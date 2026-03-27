from erp.repositorio.auditoria_repo import AuditoriaRepository


class AuditoriaServico:

    @staticmethod
    def auditar(
        usuario: dict,
        acao: str,
        recurso: str,
        detalhes: str = None,
        ip_origem: str = None
    ):
        AuditoriaRepository.registrar(
            usuario_id=int(usuario.get("sub")) if "sub" in usuario else usuario.get("id"),
            email_usuario=usuario.get("email"),
            acao=acao,
            recurso=recurso,
            detalhes=detalhes,
            ip_origem=ip_origem
        )

    @staticmethod
    def listar_auditorias(limit: int = 100):
        return AuditoriaRepository.listar(limit)