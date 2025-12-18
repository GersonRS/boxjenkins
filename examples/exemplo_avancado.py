"""
Exemplo avançado: Testando diferentes configurações ARIMA
"""

import numpy as np
import pandas as pd

from boxjenkins import BoxJenkinsPandas


def testar_diferentes_modelos(data, dates, freq="D"):
    """
    Testa múltiplas configurações ARIMA e compara resultados

    Args:
        data: Lista de valores da série temporal
        dates: Índice de datas
        freq: Frequência temporal
    """

    # Configurações a testar
    configuracoes = [
        (1, 1, 0),  # ARIMA(1,1,0) - AR puro
        (0, 1, 1),  # ARIMA(0,1,1) - MA puro
        (1, 1, 1),  # ARIMA(1,1,1) - ARMA
        (2, 1, 0),  # ARIMA(2,1,0)
        (0, 1, 2),  # ARIMA(0,1,2)
    ]

    resultados = []

    for p, d, q in configuracoes:
        print("\n" + "=" * 70)
        print(f"Testando ARIMA({p},{d},{q})")
        print("=" * 70)

        # Criar novo modelo
        model = BoxJenkinsPandas(data, dates=dates, freq=freq)

        # Identificação
        model.identificacao(d=d)

        # Estimação
        model.estimacao(p=p, q=q)

        # Armazenar resultados
        resultado = {
            "modelo": f"ARIMA({p},{d},{q})",
            "p": p,
            "d": d,
            "q": q,
            "sigma2": model.sigma2,
            "phi": model.phi.tolist() if p > 0 else [],
            "theta": model.theta.tolist() if q > 0 else [],
        }
        resultados.append(resultado)

    # Comparar resultados
    print("\n" + "=" * 70)
    print("COMPARAÇÃO DE MODELOS")
    print("=" * 70)

    df_resultados = pd.DataFrame(resultados)
    print(df_resultados[["modelo", "sigma2"]])

    # Melhor modelo (menor sigma2)
    melhor_idx = df_resultados["sigma2"].idxmin()
    melhor = resultados[melhor_idx]

    print(f"\n🏆 Melhor modelo: {melhor['modelo']}")
    print(f"   Sigma² = {melhor['sigma2']:.4f}")

    return resultados, melhor


def exemplo_completo():
    """Exemplo completo com seleção automática de modelo"""

    # Gerar dados sintéticos mais complexos
    np.random.seed(123)
    n = 200
    dates = pd.date_range(start="2022-01-01", periods=n, freq="D")

    # Processo ARMA(1,1) + tendência + diferenciação necessária
    vals = [50]
    epsilon = [0]
    phi, theta = 0.6, 0.4

    for t in range(1, n):
        e_t = np.random.normal(0, 2)
        epsilon.append(e_t)

        # ARMA(1,1): w_t = phi * w_{t-1} + e_t - theta * e_{t-1}
        if t == 1:
            w_t = e_t
        else:
            w_t = phi * (vals[-1] - vals[-2]) + e_t - theta * epsilon[-2]

        vals.append(vals[-1] + w_t + 0.1)  # Com tendência

    # Testar diferentes modelos
    resultados, melhor = testar_diferentes_modelos(vals, dates, freq="D")

    # Usar melhor modelo para previsão
    print("\n" + "=" * 70)
    print(f"PREVISÃO COM MELHOR MODELO: {melhor['modelo']}")
    print("=" * 70)

    model_final = BoxJenkinsPandas(vals, dates=dates, freq="D")
    model_final.identificacao(d=melhor["d"])
    model_final.estimacao(p=melhor["p"], q=melhor["q"])
    model_final.diagnostico()
    forecast = model_final.previsao(steps=30)

    return model_final, forecast, resultados


if __name__ == "__main__":
    model, forecast, resultados = exemplo_completo()
