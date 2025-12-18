"""
Exemplo: Gráficos Diagnósticos Estilo Statsmodels
==================================================

Este exemplo demonstra os novos gráficos profissionais em layout 2x2
inspirados na biblioteca statsmodels.

Características:
- Identificação: 4 painéis (série original, diferenciada, ACF, PACF)
- Diagnóstico: 4 painéis (resíduos, histograma+KDE, Q-Q plot, correlograma)
- Previsão: Com intervalos de confiança 95%
"""

import numpy as np
import pandas as pd

from boxjenkins import BoxJenkinsPandas

# Configurar seed para reprodutibilidade
np.random.seed(42)

# Simular série temporal AR(1) com drift
# Z_t = 0.7 * Z_{t-1} + 0.5 + epsilon_t
n = 200
series = [10]
for i in range(1, n):
    series.append(0.7 * series[-1] + 0.5 + np.random.normal(0, 1))

dates = pd.date_range(start="2020-01-01", periods=n, freq="D")

# Criar modelo com salvamento automático
print("=" * 60)
print("BOX-JENKINS com Gráficos Estilo Statsmodels")
print("=" * 60)

model = BoxJenkinsPandas(
    data=series,
    dates=dates,
    freq="D",
    run_name="demo_statsmodels_plots",
    show_plots=False,  # Apenas salvar, não exibir
)

print("\n📌 Fase 1: IDENTIFICAÇÃO")
print("-" * 60)
print("Gráfico 2x2: [Série Original] [Série Diferenciada]")
print("             [ACF Original]   [PACF Diferenciada]")
model.identificacao(d=1)

print("\n📌 Fase 2: ESTIMAÇÃO")
print("-" * 60)
print("Ajustando modelo ARIMA(1,1,0)...")
model.estimacao(p=1, q=0)

print("\n📌 Fase 3: DIAGNÓSTICO")
print("-" * 60)
print("Gráfico 2x2: [Resíduos Padronizados] [Histograma + KDE]")
print("             [Normal Q-Q Plot]       [Correlograma]")
model.diagnostico()

print("\n📌 Fase 4: PREVISÃO")
print("-" * 60)
print("Gerando previsões 30 dias com IC 95%...")
forecast = model.previsao(steps=30)

# Resumo final
print("\n" + "=" * 60)
print("✅ EXECUÇÃO COMPLETA")
print("=" * 60)
print(f"📁 Diretório de saída: {model.run_dir}")
print(f"\n📊 Gráficos gerados:")
print(f"   - 01_identificacao_d1.png   (16x10, ~470 KB)")
print(f"   - 03_diagnostico_p1_q0.png  (16x10, ~490 KB)")
print(f"   - 04_previsao_30steps.png   (14x7,  ~360 KB)")
print(f"\n📄 Arquivos de resultados:")
print(f"   - 02_estimacao.txt")
print(f"   - 03_diagnostico.txt")
print(f"   - 04_previsao.csv")
print(f"   - metadata.json")

# Estatísticas da previsão
print(f"\n📈 Resumo da Previsão:")
print(f"   Primeira previsão: {forecast.iloc[0]:.2f}")
print(f"   Última previsão:   {forecast.iloc[-1]:.2f}")
print(f"   Média das previsões: {forecast.mean():.2f}")
print(f"   Desvio padrão: {forecast.std():.2f}")

print("\n💡 Dica: Abra os arquivos PNG para visualizar os gráficos!")
print("=" * 60)
