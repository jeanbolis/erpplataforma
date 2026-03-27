import pandas as pd


class ExportadorExcel:

    @staticmethod
    def exportar(dados: list, caminho_arquivo: str, nome_aba: str = "Relatorio"):
        if not dados:
            raise ValueError("Nenhum dado para exportar")

        df = pd.DataFrame(dados)
        df.to_excel(caminho_arquivo, index=False, sheet_name=nome_aba)
