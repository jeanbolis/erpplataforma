from datetime import datetime
from erp.repositorio.auditoria_repo import AuditoriaRepository

class AuditoriaServico:

    @staticmethod
    def auditar(
        usuario_id: int,
        email_usuario: str,
        acao: str,
        recurso: str,
        detalhes: str | None = None
    ):
        AuditoriaRepository.registrar(
            usuario_id=usuario_id,
            email_usuario=email_usuario,
            acao=acao,
            recurso=recurso,
            detalhes=detalhes
        )

    @staticmethod
    def listar_auditoria_filtrada(
        usuario_id=None,
        acao=None,
        email_usuario=None,
        data_inicio=None,
        data_fim=None,
        page=1,
        page_size=20,
        order_by="criado_em",
        order_dir="DESC",
    ):
        registros = AuditoriaRepository.listar_com_filtros(
            usuario_id=usuario_id,
            acao=acao,
            email_usuario=email_usuario,
            data_inicio=data_inicio,
            data_fim=data_fim,
            page=page,
            page_size=page_size,
            order_by=order_by,
            order_dir=order_dir,
        )

        total = AuditoriaRepository.contar_com_filtros(
            usuario_id=usuario_id,
            acao=acao,
            email_usuario=email_usuario,
            data_inicio=data_inicio,
            data_fim=data_fim,
        )

        return {
            "dados": registros,
            "total": total
        }
        return AuditoriaRepository.listar_com_filtros(
            usuario_id=usuario_id,
            acao=acao,
            email_usuario=email_usuario,
            data_inicio=data_inicio,
            data_fim=data_fim,
            page=page,
            page_size=page_size,
            order_by=order_by,
            order_dir=order_dir,
        )