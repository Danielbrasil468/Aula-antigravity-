# corrigir_dados.py
import csv
import os

caminho_entrada = os.path.join("dados", "fornecedores _erro.csv")
pasta_resultados = "resultados"
caminho_saida = os.path.join(pasta_resultados, "fornecedores_corrigido.csv")
os.makedirs(pasta_resultados, exist_ok=True)

print("=" * 60)
print("CORREÇÃO E TRATAMENTO DE DADOS")
print("=" * 60)

# 1. Leitura do arquivo com erro (preservando o arquivo original)
linhas_corrigidas = []
with open(caminho_entrada, mode="r", encoding="utf-8") as f:
    leitor = csv.reader(f)
    header = next(leitor)
    linhas_corrigidas.append(header)
    
    for linha in leitor:
        if not linha:
            continue
        # Identifica o registro do fornecedor Delta com dado faltante (4 valores)
        if linha[0] == "Delta" and len(linha) == 4:
            # Reinsere o preco_unitario (110) e realinha as colunas:
            # ['Delta', '110', '4', '0.5', '9.5']
            linha_ajustada = ["Delta", "110", linha[1], linha[2], linha[3]]
            linhas_corrigidas.append(linha_ajustada)
            print(f"-> Registro 'Delta' alinhado: {linha_ajustada}")
        else:
            linhas_corrigidas.append(linha)

# 2. Gravação da nova base tratada em resultados/
with open(caminho_saida, mode="w", encoding="utf-8", newline="") as f:
    escritor = csv.writer(f)
    escritor.writerows(linhas_corrigidas)

print(f"-> Base corrigida gerada com sucesso em: {caminho_saida}")
print("=" * 60)

