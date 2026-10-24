# melhorar_graficos.py
import csv
import os
import matplotlib.pyplot as plt
import numpy as np

# Configurações de diretórios
caminho_dados = os.path.join("dados", "fornecedores.csv")
pasta_resultados = "resultados"
os.makedirs(pasta_resultados, exist_ok=True)

# 1. Carregamento dos dados originais
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

# 2. Normalização das notas (1 a 10) conforme a Decision Matrix
melhor_preco = min(item["preco"] for item in fornecedores)
melhor_prazo = min(item["prazo"] for item in fornecedores)
melhor_defeitos = min(item["defeitos"] for item in fornecedores)
melhor_suporte = max(item["suporte"] for item in fornecedores)

pesos = {"preco": 0.30, "defeitos": 0.30, "prazo": 0.20, "suporte": 0.20}

dados = []
for f in fornecedores:
    s_preco = 10.0 * (melhor_preco / f["preco"])
    s_prazo = 10.0 * (melhor_prazo / f["prazo"])
    s_defeitos = 10.0 * (melhor_defeitos / f["defeitos"])
    s_suporte = 10.0 * (f["suporte"] / melhor_suporte)

    total = (s_preco * pesos["preco"] +
             s_prazo * pesos["prazo"] +
             s_defeitos * pesos["defeitos"] +
             s_suporte * pesos["suporte"])

    dados.append({
        "fornecedor": f["fornecedor"],
        "preco_orig": f["preco"],
        "prazo_orig": f["prazo"],
        "defeitos_orig": f["defeitos"],
        "suporte_orig": f["suporte"],
        "s_preco": round(s_preco, 2),
        "s_prazo": round(s_prazo, 2),
        "s_defeitos": round(s_defeitos, 2),
        "s_suporte": round(s_suporte, 2),
        "total": round(total, 2)
    })

# Estilo visual profissional para gráficos (Skill chart-image)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#BDC3C7'
plt.rcParams['axes.linewidth'] = 0.8

# ==============================================================================
# GRÁFICO 1: MELHORIA DO GRÁFICO EXISTENTE DE NOTAS FINAIS (QUALIDADE EDITORIAL)
# ==============================================================================
dados_rank = sorted(dados, key=lambda x: x["total"], reverse=True)
nomes_rank = [d["fornecedor"] for d in dados_rank]
totais_rank = [d["total"] for d in dados_rank]
media_total = np.mean(totais_rank)

fig, ax = plt.subplots(figsize=(9, 5.5), dpi=150)
cores = ["#2ECC71" if d["fornecedor"] == "Delta" else "#2980B9" for d in dados_rank]

barras = ax.bar(nomes_rank, totais_rank, color=cores, width=0.52, edgecolor="#2C3E50", linewidth=1.1, zorder=3)

# Rótulos nas barras com destaque para o vencedor
for barra, d in zip(barras, dados_rank):
    altura = barra.get_height()
    rotulo = f"{altura:.2f}\n(1º Lugar)" if d["fornecedor"] == "Delta" else f"{altura:.2f}"
    ax.annotate(rotulo,
                xy=(barra.get_x() + barra.get_width() / 2, altura),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom', fontsize=10,
                fontweight='bold' if d["fornecedor"] == "Delta" else 'normal',
                color="#1E8449" if d["fornecedor"] == "Delta" else "#2C3E50")

# Linha de média comparativa
ax.axhline(media_total, color="#E74C3C", linestyle="--", linewidth=1.2, zorder=2,
           label=f"Média Geral ({media_total:.2f} pts)")

ax.set_title("Ranking Geral de Fornecedores - Matriz de Decisão", fontsize=13, fontweight='bold', pad=14)
ax.set_xlabel("Fornecedor", fontsize=11, labelpad=8)
ax.set_ylabel("Nota Final Ponderada (Escala 0 a 10)", fontsize=11, labelpad=8)
ax.set_ylim(0, 11)
ax.grid(axis='y', linestyle=':', alpha=0.6, zorder=1)
ax.legend(loc="upper right", framealpha=0.95)

# Rodapé com fonte e metodologia
plt.figtext(0.12, 0.01, "Fonte: dados/fornecedores.csv | Metodologia: Decision Matrix (Skill)",
            fontsize=8, color="#7F8C8D")
plt.tight_layout()

caminho_g1 = os.path.join(pasta_resultados, "analise_fornecedores_aprimorado.png")
plt.savefig(caminho_g1)
plt.close()

# ==============================================================================
# GRÁFICO 2: NOVO GRÁFICO RADAR (COMPARATIVO MULTIDIMENSIONAL 360°)
# ==============================================================================
categorias = ["Preço\n(Custo)", "Prazo\n(Agilidade)", "Qualidade\n(Menos Defeitos)", "Suporte\n(Atendimento)"]
N = len(categorias)
angulos = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angulos += angulos[:1]  # Fechar o círculo

fig, ax = plt.subplots(figsize=(7.5, 7.5), subplot_kw=dict(polar=True), dpi=150)

paleta_radar = {
    "Delta": ("#27AE60", 2.2, "-"),
    "Beta": ("#2980B9", 1.8, "--"),
    "Alfa": ("#F39C12", 1.4, ":"),
    "Gama": ("#95A5A6", 1.2, "-.")
}

for d in dados:
    valores = [d["s_preco"], d["s_prazo"], d["s_defeitos"], d["s_suporte"]]
    valores += valores[:1]
    cor, largura, estilo = paleta_radar[d["fornecedor"]]
    ax.plot(angulos, valores, label=f"{d['fornecedor']} ({d['total']:.2f})",
            color=cor, linewidth=largura, linestyle=estilo)
    ax.fill(angulos, valores, color=cor, alpha=0.1)

ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
ax.set_xticks(angulos[:-1])
ax.set_xticklabels(categorias, fontsize=10, fontweight='bold')
ax.set_ylim(0, 10.5)
ax.set_yticks([2, 4, 6, 8, 10])
ax.set_yticklabels(["2", "4", "6", "8", "10"], color="#7F8C8D", size=8)
ax.grid(color="#BDC3C7", linestyle="--", linewidth=0.7)

ax.set_title("Comparativo Multidimensional (Gráfico Radar)", fontsize=13, fontweight='bold', pad=22)
ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1), title="Fornecedor (Nota Final)", framealpha=0.95)
plt.figtext(0.08, 0.01, "Escala radial de 0 a 10 (10 = melhor desempenho no critério)", fontsize=8, color="#7F8C8D")
plt.tight_layout()

caminho_g2 = os.path.join(pasta_resultados, "grafico_radar_fornecedores.png")
plt.savefig(caminho_g2)
plt.close()

# ==============================================================================
# GRÁFICO 3: NOVO GRÁFICO DE TRADE-OFF (PREÇO VS. TAXA DE DEFEITOS)
# ==============================================================================
fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=150)

for d in dados:
    x = d["preco_orig"]
    y = d["defeitos_orig"]
    tamanho = d["prazo_orig"] * 60  # Bolha proporcional ao prazo de entrega
    cor = "#27AE60" if d["fornecedor"] == "Delta" else "#2980B9"

    ax.scatter(x, y, s=tamanho, color=cor, alpha=0.75, edgecolors="#1A252F", linewidth=1.5, zorder=3)
    ax.annotate(f"{d['fornecedor']}\n({d['prazo_orig']:.0f} dias)",
                xy=(x, y), xytext=(0, 10), textcoords="offset points",
                ha='center', fontsize=10, fontweight='bold')

ax.set_title("Trade-off: Preço Unitário vs. Taxa de Defeitos", fontsize=13, fontweight='bold', pad=14)
ax.set_xlabel("Preço Unitário em R$ (Menor é melhor →)", fontsize=11, labelpad=8)
ax.set_ylabel("Taxa de Defeitos em % (Menor é melhor ↓)", fontsize=11, labelpad=8)

# Linhas de referência de medianas para dividir quadrantes
ax.axvline(95, color="#BDC3C7", linestyle="--", linewidth=1, zorder=1)
ax.axhline(1.5, color="#BDC3C7", linestyle="--", linewidth=1, zorder=1)

ax.text(86, 0.6, "★ Alta Qualidade &\nMenor Preço (Ideal)", fontsize=9, color="#16A085", style='italic')
ax.text(101, 3.5, "⚠ Alto Preço &\nMais Defeitos", fontsize=9, color="#C0392B", style='italic')

ax.grid(True, linestyle=":", alpha=0.6, zorder=1)
plt.figtext(0.12, 0.01, "* O tamanho de cada bolha representa o prazo de entrega (bolhas menores entregam mais rápido).",
            fontsize=8, color="#7F8C8D")
plt.tight_layout()

caminho_g3 = os.path.join(pasta_resultados, "grafico_tradeoff_fornecedores.png")
plt.savefig(caminho_g3)
plt.close()

print("-> Todos os gráficos foram gerados e salvos com sucesso em resultados/:")
print(f"   1. {caminho_g1}")
print(f"   2. {caminho_g2}")
print(f"   3. {caminho_g3}")

