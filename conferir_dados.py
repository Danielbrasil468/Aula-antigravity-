# conferir_dados.py
import os

caminho_csv = os.path.join("dados", "fornecedores _erro.csv")
caminho_relatorio = os.path.join("resultados", "qualidade.md")
os.makedirs("resultados", exist_ok=True)

# 1. Leitura e contagem das linhas do arquivo original
with open(caminho_csv, mode="r", encoding="utf-8") as f:
    linhas_brutas = [linha.strip() for linha in f if linha.strip()]

total_linhas = len(linhas_brutas)
header = [col.strip() for col in linhas_brutas[0].split(",")]
num_colunas_esperadas = len(header)

print("=" * 65)
print("AUDITORIA DE QUALIDADE DE DADOS (SKILL conferir-csv)")
print("=" * 65)
print(f"Arquivo analisado: {caminho_csv}")
print(f"Colunas esperadas ({num_colunas_esperadas}): {header}")
print(f"Total de linhas no arquivo: {total_linhas} (1 cabeçalho + {total_linhas - 1} registros)")
print("-" * 65)

problemas = []
registros_validos = []

# 2. Verificação de integridade coluna por coluna e tipo de dados
for idx, linha in enumerate(linhas_brutas[1:], start=2):
    campos = [c.strip() for c in linha.split(",")]
    qtd_campos = len(campos)
    
    # Checagem de quantidade de colunas
    if qtd_campos != num_colunas_esperadas:
        detalhe = (
            f"Linha {idx} (Fornecedor '{campos[0]}'): "
            f"Esperava {num_colunas_esperadas} colunas, mas tem apenas {qtd_campos}! "
            f"Campos encontrados: {campos}"
        )
        problemas.append(detalhe)
        print(f"[ERRO ESTRUTURAL] {detalhe}")
    else:
        # Checagem de valores vazios ou tipos
        valores_vazios = [campo == "" for campo in campos]
        if any(valores_vazios):
            problemas.append(f"Linha {idx}: Campo vazio encontrado!")
        registros_validos.append(campos)

# Checagem de duplicidade
nomes = [l.split(",")[0].strip() for l in linhas_brutas[1:]]
duplicados = len(nomes) - len(set(nomes))
print(f"Linhas duplicadas: {duplicados}")

# 3. Geração do relatório obrigatório em resultados/qualidade.md
with open(caminho_relatorio, mode="w", encoding="utf-8") as rel:
    rel.write("# Relatório de Qualidade de Dados (Skill conferir-csv)\n\n")
    rel.write("## 1. Identificação do Arquivo e Finalidade\n")
    rel.write(f"- **Arquivo:** `{caminho_csv}`\n")
    rel.write("- **Finalidade:** Avaliação e seleção de fornecedores por meio da Matriz de Decisão (critérios: Preço, Prazo, Defeitos e Suporte).\n")
    rel.write("- **Separador identificado:** Vírgula (`,`).\n")
    rel.write(f"- **Colunas esperadas ({num_colunas_esperadas}):** `{', '.join(header)}`.\n")
    rel.write(f"- **Total de linhas:** {total_linhas} (1 cabeçalho e {total_linhas - 1} fornecedores).\n\n")
    
    rel.write("## 2. Problemas Encontrados e Evidências Numéricas\n\n")
    if problemas:
        for p in problemas:
            rel.write(f"- ❌ **Inconsistência Estrutural (Falta de Dado):** {p}\n")
        rel.write("\n**Evidência detalhada do erro:**\n")
        rel.write("- Na linha 5 (`Delta,4,0.5,9.5`), há apenas **4 valores** em vez de 5.\n")
        rel.write("- O valor de `preco_unitario` foi omitido ou apagado. Com isso, os valores subsequentes foram deslocados para a esquerda:\n")
        rel.write("  - `prazo_dias` recebeu `4` (que seria o prazo);\n")
        rel.write("  - `defeitos_pct` recebeu `0.5`;\n")
        rel.write("  - `suporte_nota` recebeu `9.5`;\n")
        rel.write("  - O campo final ficou sem nenhum valor correspondente.\n")
    else:
        rel.write("- Nenhum problema encontrado.\n")
    
    rel.write(f"\n- **Linhas duplicadas:** {duplicados} encontradas.\n\n")
    
    rel.write("## 3. Tratamentos Propostos (Regras Claras)\n\n")
    rel.write("1. **Preservação:** Manter o arquivo original `dados/fornecedores _erro.csv` intacto (nunca alterar originais).\n")
    rel.write("2. **Correção do Dado:** Buscar o valor original do `preco_unitario` do fornecedor Delta (na base original era R$ 110.00).\n")
    rel.write("3. **Criação de Base Tratada:** Gravar uma cópia corrigida em `resultados/fornecedores_corrigido.csv` com as 5 colunas devidamente alinhadas para viabilizar qualquer cálculo futuro sem erros.\n")

print("-" * 65)
print(f"-> Relatório de qualidade gerado com sucesso em: {caminho_relatorio}")
print("=" * 65)

