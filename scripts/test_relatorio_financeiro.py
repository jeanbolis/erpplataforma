from erp.servico.relatorio_financeiro_servico import RelatorioFinanceiroServico


def main():
    print("=== RELATÓRIO FINANCEIRO RESUMIDO ===")

    r = RelatorioFinanceiroServico.resumo()

    print("A RECEBER (ABERTO):", r["receber_aberto"])
    print("A RECEBER (BAIXADO):", r["receber_baixado"])
    print("A PAGAR (ABERTO):", r["pagar_aberto"])
    print("A PAGAR (BAIXADO):", r["pagar_baixado"])


if __name__ == "__main__":
    main()