"""
Exemplo básico de uso da biblioteca boxjenkins
Demonstra o workflow completo do ciclo Box-Jenkins
"""

import numpy as np
import pandas as pd

from boxjenkins import BoxJenkinsPandas


def exemplo_sintetico():
    """Exemplo com dados sintéticos - Random Walk com tendência"""

    print("=" * 70)
    print("EXEMPLO 1: Dados Sintéticos (Random Walk)")
    print("=" * 70)

    # Gerar dados sintéticos
    np.random.seed(42)
    dates = pd.date_range(start="2023-01-01", periods=100, freq="D")

    # Z_t = Z_{t-1} + 0.5 + ruído
    vals = [10]
    for i in range(1, 100):
        vals.append(vals[-1] + 0.5 + np.random.normal(0, 1))

    # Instanciar modelo (sem mostrar gráficos, apenas salvar)
    model = BoxJenkinsPandas(
        vals, dates=dates, freq="D", run_name="exemplo_sintetico", show_plots=False
    )  # Fase 1: Identificação
    print("\n[1/4] FASE DE IDENTIFICAÇÃO")
    model.identificacao(d=1)

    # Fase 2: Estimação
    print("\n[2/4] FASE DE ESTIMAÇÃO")
    model.estimacao(p=1, q=0)

    # Fase 3: Diagnóstico
    print("\n[3/4] FASE DE DIAGNÓSTICO")
    model.diagnostico()

    # Fase 4: Previsão
    print("\n[4/4] FASE DE PREVISÃO")
    forecast = model.previsao(steps=15)

    print("\n" + "=" * 70)
    print("EXEMPLO COMPLETO!")
    print("=" * 70)

    return model, forecast


def exemplo_com_csv(csv_path):
    """
    Exemplo com dados reais de um arquivo CSV

    Args:
        csv_path: Caminho para arquivo CSV com colunas [data, valor]
    """

    print("=" * 70)
    print("EXEMPLO 2: Dados Reais de CSV")
    print("=" * 70)

    # Carregar dados
    df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
    coluna_valor = df.columns[0]  # Primeira coluna de dados

    print(f"\nDados carregados: {len(df)} observações")
    print(f"Período: {df.index[0]} até {df.index[-1]}")
    print(f"\nEstatísticas:\n{df[coluna_valor].describe()}")

    # Preparar dados
    valores = df[coluna_valor].tolist()
    datas = df.index

    # Instanciar modelo (sem mostrar gráficos)
    model = BoxJenkinsPandas(
        valores, dates=datas, freq="D", run_name="exemplo_csv", show_plots=False
    )

    # Executar workflow completo
    print("\n[1/4] Identificação...")
    model.identificacao(d=1)

    print("\n[2/4] Estimação...")
    model.estimacao(p=1, q=1)

    print("\n[3/4] Diagnóstico...")
    model.diagnostico()

    print("\n[4/4] Previsão...")
    forecast = model.previsao(steps=30)

    return model, forecast


if __name__ == "__main__":
    # Exemplo 1: Dados sintéticos
    model1, forecast1 = exemplo_sintetico()

    # Exemplo 2: Dados reais (descomente se tiver o arquivo)
    # model2, forecast2 = exemplo_com_csv('precos_itub4.csv')
