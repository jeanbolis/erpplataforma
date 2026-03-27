from erp.servico.fluxo_caixa_servico import FluxoCaixaServico
from datetime import date


def main():
    print("=== TESTE DE FLUXO DE CAIXA ===")

    hoje = date.today().isoformat()

    resumo = FluxoCaixaServico.resumo_por_periodo(
        data_inicio=hoje,
        data_fim=hoje
    )

    print("Período:", resumo["periodo"])
    print("Entradas:", resumo["entradas"])
    print("Saídas:", resumo["saidas"])
    print("Saldo:", resumo["saldo"])


if __name__ == "__main__":
    main()