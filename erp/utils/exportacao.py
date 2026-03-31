import csv
from io import StringIO, BytesIO
from fastapi.responses import StreamingResponse

from openpyxl import Workbook


def exportar_csv(nome_arquivo: str, dados: list[dict]):
    buffer = StringIO()

    if dados:
        writer = csv.DictWriter(buffer, fieldnames=dados[0].keys())
        writer.writeheader()
        writer.writerows(dados)

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={nome_arquivo}"
        }
    )


def exportar_excel(nome_arquivo: str, dados: list[dict]):
    wb = Workbook()
    ws = wb.active
    ws.title = "Auditoria"

    if dados:
        ws.append(list(dados[0].keys()))
        for item in dados:
            ws.append(list(item.values()))

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename={nome_arquivo}"
        }
    )
