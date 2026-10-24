# Relatório de Qualidade de Dados (Skill conferir-csv)

## 1. Identificação do Arquivo e Finalidade
- **Arquivo:** `dados\fornecedores _erro.csv`
- **Finalidade:** Avaliação e seleção de fornecedores por meio da Matriz de Decisão (critérios: Preço, Prazo, Defeitos e Suporte).
- **Separador identificado:** Vírgula (`,`).
- **Colunas esperadas (5):** `fornecedor, preco_unitario, prazo_dias, defeitos_pct, suporte_nota`.
- **Total de linhas:** 5 (1 cabeçalho e 4 fornecedores).

## 2. Problemas Encontrados e Evidências Numéricas

- ❌ **Inconsistência Estrutural (Falta de Dado):** Linha 5 (Fornecedor 'Delta'): Esperava 5 colunas, mas tem apenas 4! Campos encontrados: ['Delta', '4', '0.5', '9.5']

**Evidência detalhada do erro:**
- Na linha 5 (`Delta,4,0.5,9.5`), há apenas **4 valores** em vez de 5.
- O valor de `preco_unitario` foi omitido ou apagado. Com isso, os valores subsequentes foram deslocados para a esquerda:
  - `prazo_dias` recebeu `4` (que seria o prazo);
  - `defeitos_pct` recebeu `0.5`;
  - `suporte_nota` recebeu `9.5`;
  - O campo final ficou sem nenhum valor correspondente.

- **Linhas duplicadas:** 0 encontradas.

## 3. Tratamentos Propostos (Regras Claras)

1. **Preservação:** Manter o arquivo original `dados/fornecedores _erro.csv` intacto (nunca alterar originais).
2. **Correção do Dado:** Buscar o valor original do `preco_unitario` do fornecedor Delta (na base original era R$ 110.00).
3. **Criação de Base Tratada:** Gravar uma cópia corrigida em `resultados/fornecedores_corrigido.csv` com as 5 colunas devidamente alinhadas para viabilizar qualquer cálculo futuro sem erros.
