# termometro.py
import os
import matplotlib.pyplot as plt

# 1. Pontos conhecidos (Temperatura em °C, Corrente em mA):
# Ponto 1: (0 °C, 4 mA)
# Ponto 2: (100 °C, 20 mA)
x1, y1 = 0, 4
x2, y2 = 100, 20

# 2. Cálculo dos coeficientes da reta: y = ax + b
# 'a' é o coeficiente angular (inclinação)
a = (y2 - y1) / (x2 - x1)

# 'b' é o coeficiente linear (onde x = 0)
b = y1 - (a * x1)

# 3. Temperatura informada para teste (em graus Celsius)
x_alvo = 50
y_alvo = (a * x_alvo) + b

# 4. Classificação da temperatura
# - Baixa: até 30 °C
# - Média: até 60 °C (acima de 30 até 60)
# - Alta: acima de 60 °C
if x_alvo <= 30:
    classificacao = "Baixa"
elif x_alvo <= 60:
    classificacao = "Média"
else:
    classificacao = "Alta"

# 5. Avisos de segurança (faixas operacionais normais)
avisos = []
if x_alvo < 0 or x_alvo > 100:
    avisos.append("AVISO: Temperatura fora da faixa operacional de 0 a 100 ºC!")

if y_alvo < 4 or y_alvo > 20:
    avisos.append("AVISO: Corrente elétrica fora da faixa de 4 a 20 mA!")

# 6. Exibição dos dados e mensagens no terminal
print("=== RESULTADOS DO TERMÔMETRO ===")
print(f"Equação da reta: y = {a} * x + {b}")
print(f"Coeficiente angular (a): {a}")
print(f"Coeficiente linear (b): {b}")
print(f"Temperatura: {x_alvo} ºC")
print(f"Corrente calculada: {y_alvo} mA")
print(f"Classificação da temperatura: {classificacao}")

if avisos:
    for aviso in avisos:
        print(f"-> {aviso}")
else:
    print("-> Status: Temperatura e corrente dentro da faixa normal.")

# 7. Geração do gráfico com Matplotlib
# Traça a linha de calibração de 0 a 100 °C
x_linha = [0, 100]
y_linha = [a * x + b for x in x_linha]

plt.figure(figsize=(8, 5))
plt.plot(x_linha, y_linha, label="Relação Temperatura x Corrente", color="blue")
plt.scatter([x_alvo], [y_alvo], color="red", zorder=5, label=f"Ponto medido ({x_alvo} ºC, {y_alvo} mA)")

# Configurações dos eixos e legendas
plt.title("Termômetro: Temperatura vs. Corrente Elétrica")
plt.xlabel("Temperatura (ºC)")
plt.ylabel("Corrente Elétrica (mA)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()

# Garantir que a pasta resultados exista e salvar o gráfico nela
os.makedirs("resultados", exist_ok=True)
caminho_grafico = os.path.join("resultados", "grafico_termometro.png")
plt.savefig(caminho_grafico)
plt.close()

print(f"-> Gráfico salvo com sucesso em: {caminho_grafico}")
