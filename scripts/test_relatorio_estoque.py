from erp.servico.relatorio_estoque_servico import RelatorioEstoqueServico


def main():
    print("=== RELATÓRIO DE ESTOQUE ATUAL ===")

    for item in RelatorioEstoqueServico.estoque_atual():
        print(f"{item['codigo']} | {item['nome']} | Saldo: {item['saldo']}")


if __name__ == "__main__":
    main()