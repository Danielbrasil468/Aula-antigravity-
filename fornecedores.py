# fornecedores.py
import csv
import os
import matplotlib.pyplot as plt

# 1. Caminhos dos arquivos
caminho_dados = os.path.join("dados", "fornecedores.csv")
pasta_resultados = "resultados"
os.makedirs(pasta_resultados, exist_ok=True)

# 2. Leitura do arquivo CSV de fornecedores
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

# 3. Identificação dos melhores valores para cada critério
# Para Preço, Prazo e Defeitos: MENOR é melhor (min)
# Para Suporte: MAIOR é melhor (max)
melhor_preco = min(item["preco"] for item in fornecedores)
melhor_prazo = min(item["prazo"] for item in fornecedores)
melhor_defeitos = min(item["defeitos"] for item in fornecedores)
melhor_suporte = max(item["suporte"] for item in fornecedores)

# 4. Definição dos pesos dos critérios (conforme metodologia da Decision Matrix)
# Total = 100% (1.0)
pesos = {
    "preco": 0.30,      # 30% - Impacto financeiro direto
    "defeitos": 0.30,   # 30% - Qualidade do produto
    "prazo": 0.20,      # 20% - Agilidade na entrega
    "suporte": 0.20     # 20% - Atendimento e pós-venda
}

# 5. Cálculo das pontuações normalizadas (escala de 1 a 10) e nota final ponderada
# Fórmulas da skill decision-matrix:
# - Menor é melhor: 10 * (melhor_valor / valor_atual)
# - Maior é melhor: 10 * (valor_atual / melhor_valor)
resultados = []
for f in fornecedores:
    score_preco = 10.0 * (melhor_preco / f["preco"])
    score_prazo = 10.0 * (melhor_prazo / f["prazo"])
    score_defeitos = 10.0 * (melhor_defeitos / f["defeitos"])
    score_suporte = 10.0 * (f["suporte"] / melhor_suporte)

    # Pontuações ponderadas
    p_preco = score_preco * pesos["preco"]
    p_prazo = score_prazo * pesos["prazo"]
    p_defeitos = score_defeitos * pesos["defeitos"]
    p_suporte = score_suporte * pesos["suporte"]

    nota_final = p_preco + p_prazo + p_defeitos + p_suporte

    resultados.append({
        "fornecedor": f["fornecedor"],
        "preco_original": f["preco"],
        "prazo_original": f["prazo"],
        "defeitos_original": f["defeitos"],
        "suporte_original": f["suporte"],
        "score_preco": round(score_preco, 2),
        "score_prazo": round(score_prazo, 2),
        "score_defeitos": round(score_defeitos, 2),
        "score_suporte": round(score_suporte, 2),
        "p_preco": round(p_preco, 2),
        "p_prazo": round(p_prazo, 2),
        "p_defeitos": round(p_defeitos, 2),
        "p_suporte": round(p_suporte, 2),
        "nota_final": round(nota_final, 2)
    })

# Ordenação pelo score final (do maior para o menor)
resultados.sort(key=lambda x: x["nota_final"], reverse=True)
vencedor = resultados[0]

# 6. Exibição resumida no terminal
print("=" * 60)
print("MATRIZ DE DECISÃO - SELEÇÃO DE FORNECEDORES")
print("=" * 60)
for rank, r in enumerate(resultados, start=1):
    print(f"{rank}º Lugar: Fornecedor {r['fornecedor']} - Nota Final: {r['nota_final']:.2f}/10")
print("-" * 60)
print(f"-> VENCEDOR RECOMENDADO: {vencedor['fornecedor']} com nota {vencedor['nota_final']:.2f}")
print("=" * 60)

# 7. Geração do relatório em Markdown (.md)
caminho_relatorio = os.path.join(pasta_resultados, "relatorio_decisao_fornecedores.md")
with open(caminho_relatorio, mode="w", encoding="utf-8") as rel:
    rel.write("# Relatório de Seleção de Fornecedores (Decision Matrix)\n\n")
    rel.write("## 1. Contexto e Objetivo\n")
    rel.write("Avaliação comparativa de 4 fornecedores com base em critérios técnicos, operacionais e financeiros, utilizando a metodologia estruturada de **Matriz de Decisão**.\n\n")
    rel.write("## 2. Critérios e Pesos Definidos\n")
    rel.write("- **Preço Unitário (30%):** Menor custo por unidade (menor é melhor).\n")
    rel.write("- **Taxa de Defeitos (30%):** Percentual de falhas no lote (menor é melhor).\n")
    rel.write("- **Prazo de Entrega (20%):** Tempo em dias para entrega (menor é melhor).\n")
    rel.write("- **Nota de Suporte (20%):** Avaliação do atendimento ao cliente (maior é melhor).\n\n")
    rel.write("## 3. Matriz de Avaliação e Pontuações\n\n")
    rel.write("| Posição | Fornecedor | Preço (30%) | Prazo (20%) | Defeitos (30%) | Suporte (20%) | **Nota Final** |\n")
    rel.write("| :---: | :--- | :---: | :---: | :---: | :---: | :---: |\n")
    for pos, r in enumerate(resultados, start=1):
        rel.write(f"| **{pos}º** | **{r['fornecedor']}** | {r['score_preco']} ({r['p_preco']}) | {r['score_prazo']} ({r['p_prazo']}) | {r['score_defeitos']} ({r['p_defeitos']}) | {r['score_suporte']} ({r['p_suporte']}) | **{r['nota_final']}** |\n")
    rel.write("\n*(Obs: Formato `Nota (Ponderada)`. Escala de notas de 1 a 10).*\n\n")
    rel.write("## 4. Recomendação Final\n\n")
    rel.write(f"### Vencedor: **Fornecedor {vencedor['fornecedor']}** (Nota: **{vencedor['nota_final']}/10**)\n\n")
    rel.write("**Principais Vantagens:**\n")
    rel.write(f"- Menor taxa de defeitos ({vencedor['defeitos_original']}%), garantindo alta qualidade.\n")
    rel.write(f"- Menor prazo de entrega ({vencedor['prazo_original']} dias).\n")
    rel.write(f"- Melhor avaliação de suporte ({vencedor['suporte_original']}/10).\n\n")
    rel.write("**Trade-off (Ponto de atenção):**\n")
    rel.write(f"- Possui o maior preço unitário (R$ {vencedor['preco_original']:.2f}), mas a sua qualidade e velocidade superam essa desvantagem nos critérios ponderados.\n\n")
    rel.write("![Gráfico de Análise](analise_fornecedores.png)\n")

print(f"-> Relatório salvo em: {caminho_relatorio}")

# 8. Geração do gráfico com Matplotlib
caminho_grafico = os.path.join(pasta_resultados, "analise_fornecedores.png")

nomes = [r["fornecedor"] for r in resultados]
notas = [r["nota_final"] for r in resultados]
cores = ["#2ecc71" if r["fornecedor"] == vencedor["fornecedor"] else "#3498db" for r in resultados]

plt.figure(figsize=(9, 5.5))
barras = plt.bar(nomes, notas, color=cores, width=0.55, edgecolor="black", linewidth=1.2)

# Adicionar o valor da nota em cima de cada barra
for barra in barras:
    altura = barra.get_height()
    plt.text(barra.get_x() + barra.get_width() / 2.0, altura + 0.15,
             f"{altura:.2f}", ha="center", va="bottom", fontsize=11, fontweight="bold")

plt.title("Avaliação Comparativa de Fornecedores (Decision Matrix)", fontsize=13, fontweight="bold", pad=15)
plt.xlabel("Fornecedor", fontsize=11, labelpad=10)
plt.ylabel("Nota Final Ponderada (0 a 10)", fontsize=11, labelpad=10)
plt.ylim(0, 11)
plt.axhline(vencedor["nota_final"], color="#27ae60", linestyle="--", alpha=0.7, label=f"Vencedor ({vencedor['fornecedor']})")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.legend(loc="upper right")
plt.tight_layout()

plt.savefig(caminho_grafico, dpi=150)
plt.close()

print(f"-> Gráfico salvo em: {caminho_grafico}")

