import csv


class ExportadorCSV:

    @staticmethod
    def exportar(dados: list, caminho_arquivo: str):
        if not dados:
            raise ValueError("Nenhum dado para exportar")

        campos = dados[0].keys()

        with open(caminho_arquivo, mode="w", newline="", encoding="utf-8") as arquivo:
            writer = csv.DictWriter(arquivo, fieldnames=campos, delimiter=";")
            writer.writeheader()
            writer.writerows(dados)