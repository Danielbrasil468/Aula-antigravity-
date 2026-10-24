# grafico_criterios.py
import csv
import os
import matplotlib.pyplot as plt
import numpy as np

# 1. Caminhos
caminho_dados = os.path.join("dados", "fornecedores.csv")
pasta_resultados = "resultados"
os.makedirs(pasta_resultados, exist_ok=True)

# 2. Leitura dos dados
fornecedores = []
with open(caminho_dados, mode="r", encoding="utf-8") as f:
    leitor = csv.DictReader(f)
    for linha in leitor:
        fornecedores.append({
            "fornecedor": linha["fornecedor"],
            "preco": float(linha["preco_unitario"]),
            "prazo": float(linha["prazo_dias"]),
            "defeitos": float(linha["defeitos_pct"]),
            "suporte": float(linha["suporte_nota"])
        })

# 3. Melhores valores para normalização (1 a 10)
melhor_preco = min(item["preco"] for item in fornecedores)
melhor_prazo = min(item["prazo"] for item in fornecedores)
melhor_defeitos = min(item["defeitos"] for item in fornecedores)
melhor_suporte = max(item["suporte"] for item in fornecedores)

# Pesos da Matriz de Decisão
pesos = {
    "preco": 0.30,
    "prazo": 0.20,
    "defeitos": 0.30,
    "suporte": 0.20
}

# 4. Cálculo das notas por critério (brutas de 0 a 10 e ponderadas)
dados_processados = []
for f in fornecedores:
    s_preco = 10.0 * (melhor_preco / f["preco"])
    s_prazo = 10.0 * (melhor_prazo / f["prazo"])
    s_defeitos = 10.0 * (melhor_defeitos / f["defeitos"])
    s_suporte = 10.0 * (f["suporte"] / melhor_suporte)

    p_preco = s_preco * pesos["preco"]
    p_prazo = s_prazo * pesos["prazo"]
    p_defeitos = s_defeitos * pesos["defeitos"]
    p_suporte = s_suporte * pesos["suporte"]
    total = p_preco + p_prazo + p_defeitos + p_suporte

    dados_processados.append({
        "fornecedor": f["fornecedor"],
        "s_preco": round(s_preco, 2),
        "s_prazo": round(s_prazo, 2),
        "s_defeitos": round(s_defeitos, 2),
        "s_suporte": round(s_suporte, 2),
        "p_preco": round(p_preco, 2),
        "p_prazo": round(p_prazo, 2),
        "p_defeitos": round(p_defeitos, 2),
        "p_suporte": round(p_suporte, 2),
        "total": round(total, 2)
    })

# Ordenar do menor para o maior score para que o 1º lugar fique no topo do gráfico horizontal
dados_processados.sort(key=lambda x: x["total"])

nomes = [d["fornecedor"] for d in dados_processados]
p_precos = np.array([d["p_preco"] for d in dados_processados])
p_prazos = np.array([d["p_prazo"] for d in dados_processados])
p_defeitos = np.array([d["p_defeitos"] for d in dados_processados])
p_suportes = np.array([d["p_suporte"] for d in dados_processados])
totais = [d["total"] for d in dados_processados]

# 5. Configuração da paleta de cores (tons de Azul e Verde)
cor_preco = "#1B4F72"     # Azul escuro (Preço)
cor_prazo = "#1E8449"     # Verde floresta (Prazo)
cor_defeitos = "#2ECC71"  # Verde esmeralda (Qualidade/Defeitos)
cor_suporte = "#3498DB"   # Azul claro (Suporte)

# 6. Criação do Gráfico Horizontal
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))
y_pos = np.arange(len(nomes))
altura_barra = 0.55

# --- SUBPLOT 1: Composição Ponderada da Nota Final (Barras Empilhadas Horizontais) ---
b1 = ax1.barh(y_pos, p_precos, height=altura_barra, color=cor_preco, label="Preço (Peso 30%)", edgecolor="white")
b2 = ax1.barh(y_pos, p_prazos, height=altura_barra, left=p_precos, color=cor_prazo, label="Prazo (Peso 20%)", edgecolor="white")
b3 = ax1.barh(y_pos, p_defeitos, height=altura_barra, left=p_precos + p_prazos, color=cor_defeitos, label="Qualidade/Defeitos (Peso 30%)", edgecolor="white")
b4 = ax1.barh(y_pos, p_suportes, height=altura_barra, left=p_precos + p_prazos + p_defeitos, color=cor_suporte, label="Suporte (Peso 20%)", edgecolor="white")

# Rótulo com a nota final na ponta de cada barra
for i, total in enumerate(totais):
    ax1.text(total + 0.15, y_pos[i], f"{total:.2f} pts", va="center", fontweight="bold", fontsize=10)

ax1.set_yticks(y_pos)
ax1.set_yticklabels(nomes, fontsize=11, fontweight="bold")
ax1.set_xlim(0, 11)
ax1.set_xlabel("Nota Ponderada Acumulada (0 a 10)", fontsize=10)
ax1.set_title("1. Contribuição de Cada Critério na Nota Final Ponderada", fontsize=12, fontweight="bold", pad=10)
ax1.legend(loc="lower right", fontsize=9, framealpha=0.9)
ax1.grid(axis="x", linestyle="--", alpha=0.5)

# --- SUBPLOT 2: Desempenho Direto por Critério (Escala 0 a 10) ---
criterios = ["Preço", "Prazo", "Defeitos", "Suporte"]
cores_criterios = [cor_preco, cor_prazo, cor_defeitos, cor_suporte]
y_crit = np.arange(len(criterios))

# Mostra as notas de 0 a 10 para o vencedor (Delta) e o 2º colocado (Beta) para comparação direta
delta = next(d for d in dados_processados if d["fornecedor"] == "Delta")
beta = next(d for d in dados_processados if d["fornecedor"] == "Beta")

notas_delta = [delta["s_preco"], delta["s_prazo"], delta["s_defeitos"], delta["s_suporte"]]
notas_beta = [beta["s_preco"], beta["s_prazo"], beta["s_defeitos"], beta["s_suporte"]]

h = 0.35
ax2.barh(y_crit + h/2, notas_delta, height=h, color="#2ECC71", label="Fornecedor Delta (1º Lugar)", edgecolor="black")
ax2.barh(y_crit - h/2, notas_beta, height=h, color="#3498DB", label="Fornecedor Beta (2º Lugar)", edgecolor="black")

for i in range(len(criterios)):
    ax2.text(notas_delta[i] + 0.15, y_crit[i] + h/2, f"{notas_delta[i]:.1f}", va="center", fontsize=9, fontweight="bold")
    ax2.text(notas_beta[i] + 0.15, y_crit[i] - h/2, f"{notas_beta[i]:.1f}", va="center", fontsize=9)

ax2.set_yticks(y_crit)
ax2.set_yticklabels(criterios, fontsize=11, fontweight="bold")
ax2.set_xlim(0, 11.5)
ax2.set_xlabel("Nota do Critério (0 a 10)", fontsize=10)
ax2.set_title("2. Comparativo Detalhado por Critério: Delta (Verde) vs. Beta (Azul)", fontsize=12, fontweight="bold", pad=10)
ax2.legend(loc="lower right", fontsize=9, framealpha=0.9)
ax2.grid(axis="x", linestyle="--", alpha=0.5)

plt.tight_layout()

# 7. Salvar na pasta resultados
caminho_imagem = os.path.join(pasta_resultados, "grafico_criterios_fornecedores.png")
plt.savefig(caminho_imagem, dpi=150)
plt.close()

print(f"-> Novo gráfico gerado com sucesso em: {caminho_imagem}")

