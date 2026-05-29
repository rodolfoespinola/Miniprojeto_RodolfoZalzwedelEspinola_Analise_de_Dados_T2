# 1. Importando as bibliotecas
import pandas as pd
import numpy as np

# 2. Abrindo csv com pandas
df = pd.read_csv('data/Base_Varejo.csv', sep=';')

# 3. Entendendo a base de dados
print("📋 Primeiras linhas do dataset:")
print(df.head(10))
print(f"📐 O dataset tem {df.shape[0]} linhas e {df.shape[1]} colunas")
print()
print("📋 Tipo de dado de cada coluna:")
print(df.dtypes)

def relatorio_qualidade(df):
    """Gera um relatório completo de qualidade do DataFrame."""
    
    print("=" * 60)
    print("       📊 RELATÓRIO DE QUALIDADE DOS DADOS - Base Varejo")
    print("=" * 60)
    print(f"\n🔢 Total de linhas:   {df.shape[0]:,}")
    print(f"📋 Total de colunas: {df.shape[1]:,}")
    print(f"🔄 Linhas duplicadas: {df.duplicated().sum():,}")
    
    print("\n📌 Valores ausentes por coluna:")
    nulos = df.isnull().sum()
    pct_nulos = (df.isnull().sum() / len(df) * 100).round(2)
    
    relatorio = pd.DataFrame({
        'Tipo': df.dtypes,
        'Nulos': nulos,
        '% Nulos': pct_nulos,
        'Únicos': df.nunique()
    })
    print(relatorio)
    print("=" * 60)
    print()

relatorio_qualidade(df)

# Quatro colunas vazias
# 96.553 linhas duplicadas

# 4. Iniciando as limpezas
# Copia do df origianl
df_limpo = df.copy()

# Removendo duplicatas, mantendo o primeiro, e reindexando os índices
print("=" * 60)
print("📋 INICIANDO REMOÇÃO DE DUPLICATAS")
print("=" * 60)
print(f"ANTES: {len(df_limpo)} linhas")
df_limpo = df_limpo.drop_duplicates(keep='first')
df_limpo = df_limpo.reset_index(drop=True)
print(f"DEPOIS: {len(df_limpo)} linhas")
print()
