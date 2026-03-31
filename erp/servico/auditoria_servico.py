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
    
    @staticmethod
    def listar_auditoria_por_usuario(usuario_id: int, limit: int = 100):
        return AuditoriaRepository.listar_por_usuario(usuario_id, limit)
    
    @staticmethod
    def listar_auditoria_filtrada(
        usuario_id: int | None,
        acao: str | None,
        data_inicio: str | None,
        data_fim: str | None,
        page: int,
        page_size: int,
        order_by: str,
        order_dir: str
    ):
        return AuditoriaRepository.listar_com_filtros(
            usuario_id=usuario_id,
            acao=acao,
            data_inicio=data_inicio,
            data_fim=data_fim,
            page=page,
            page_size=page_size,
            order_by=order_by,
            order_dir=order_dir
        )