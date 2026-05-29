# 1. Importando as bibliotecas
import pandas as pd
import numpy as np

# 2. Abrindo csv com pandas
df = pd.read_csv('../data/Base_Varejo.csv', sep=';')

# 3. Entendendo a base de dados
print("📋 Primeiras linhas do dataset:")
print(df.head(10))
print(f"📐 O dataset tem {df.shape[0]} linhas e {df.shape[1]} colunas")
print()
print("📋 Tipo de dado de cada coluna:")
print(df.dtypes)


# 4. Fazendo o diagnóstico do DF
def diagnostico(df, nome="DataFrame"):
    """
    Mostra um relatório completo de qualidade dos dados.
    Use sempre antes de começar a limpeza!
    """
    print("=" * 55)
    print(f"  📊 DIAGNÓSTICO: {nome}")
    print("=" * 55)
    print(f"  Linhas:           {df.shape[0]:,}")
    print(f"  Colunas:          {df.shape[1]}")
    print(f"  Linhas duplicadas:{df.duplicated().sum():,}")
    print()
    
    nulos = df.isnull().sum()
    pct   = (nulos / len(df) * 100).round(1)
    
    print("  Coluna           | Tipo       | Nulos | % Nulos")
    print("  " + "-"*50)
    for col in df.columns:
        tipo = str(df[col].dtype)
        print(f"  {col:<18}| {tipo:<10} | {nulos[col]:<5} | {pct[col]}%")
    print("=" * 55)

# Rodando o diagnóstico no nosso dataset
diagnostico(df, "Base Varejo")

def relatorio_qualidade(df):
    """Gera um relatório completo de qualidade do DataFrame."""
    
    print("=" * 60)
    print("       📊 RELATÓRIO DE QUALIDADE DOS DADOS")
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

relatorio_qualidade(df)
