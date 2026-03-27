from erp.servico.relatorio_vendas_servico import RelatorioVendasServico


def main():
    print("=== RELATÓRIO DE VENDAS POR PERÍODO ===")

    vendas = RelatorioVendasServico.vendas_por_periodo(
        data_inicio="2026-03-01",
        data_fim="2026-03-31"
    )

    if not vendas:
        print("Nenhuma venda no período")
        return

    for v in vendas:
        print(
            f"Venda {v['venda_id']} | "
            f"Cliente: {v['cliente']} | "
            f"Data: {v['data_venda']} | "
            f"Itens: {v['qtd_itens']} | "
            f"Qtd total: {v['total_itens']}"
        )


if __name__ == "__main__":
    main()