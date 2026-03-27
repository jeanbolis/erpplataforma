from erp.servico.relatorio_estoque_servico import RelatorioEstoqueServico
from erp.exportacao.exportador_csv import ExportadorCSV
from erp.exportacao.exportador_excel import ExportadorExcel


def main():
    print("=== EXPORTAÇÃO DE ESTOQUE ===")

    dados = RelatorioEstoqueServico.estoque_atual()

    ExportadorCSV.exportar(dados, "estoque_atual.csv")
    print("Arquivo estoque_atual.csv gerado")

    ExportadorExcel.exportar(dados, "estoque_atual.xlsx", nome_aba="Estoque")
    print("Arquivo estoque_atual.xlsx gerado")


if __name__ == "__main__":
    main()