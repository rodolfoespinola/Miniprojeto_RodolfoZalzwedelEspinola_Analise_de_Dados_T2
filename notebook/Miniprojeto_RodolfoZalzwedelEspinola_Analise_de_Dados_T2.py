# 1. Importando as bibliotecas
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 2. Abrindo csv com pandas
df = pd.read_csv('data/raw/Base_Varejo.csv', sep=';')

# Configurações para deixar a exibição mais legível
pd.set_option('display.max_columns', None)   # Mostrar todas as colunas 
pd.set_option('display.float_format', '{:.2f}'.format)  # 2 casas decimais

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

# Quatro colunas com 100% do conteúdo nulo
# 96.553 registros duplicados completos

# 4. Iniciando as limpezas
# Copia do df origianl
df_limpo = df.copy()

# Removendo duplicatas, mantendo o primeiro, e reindexando os índices
# Opção de remover as linhas com conteúdo 100% iguais, que podem indicaar erro de entrada
print("=" * 60)
print("📋 INICIANDO REMOÇÃO DE DUPLICATAS")
print("=" * 60)
print(f"ANTES: {len(df_limpo)} linhas")
duplicatas = df_limpo.duplicated().sum()
df_limpo = df_limpo.drop_duplicates(keep='first')
df_limpo = df_limpo.reset_index(drop=True)
print(f"DEPOIS: {len(df_limpo)} linhas")
print(f"Duplicatas removidas: {duplicatas}")
print()

# Removendo colunas vazias
df_limpo = df_limpo.drop(columns=["Unnamed: 10", "Unnamed: 11", "Unnamed: 12", "Unnamed: 13"])

# Convertendo data
print("=" * 60)
print("📋 INICIANDO CONVERSÃO DE DATA")
print("=" * 60)
df_limpo["DATA"] = pd.to_datetime(df_limpo["DATA"], dayfirst=True, errors="coerce")
# Cehcando datas inválidas
datas_invalidas = df_limpo["DATA"].isnull().sum()
print(f"Formato data alterado para: {df_limpo['DATA'].dtypes}")
print(f"Datas inválidas encontradas: {datas_invalidas}")
print()

# Padronização das colunas de texto para garantir consistência
df_limpo["PR_CAT"] = df_limpo["PR_CAT"].str.strip().str.upper()
df_limpo["PR_NOME"] = df_limpo["PR_NOME"].str.strip().str.upper()

# Após agrupamento, foram descobertos preenchimentos com #N/D. 
# Analisando para ver a quantidade de N/D
nd_cat = (df_limpo["PR_CAT"] == "#N/D").sum()
nd_nome = (df_limpo["PR_NOME"] == "#N/D").sum()
print("=" * 60)
print("📋 CATEGORIAS E PRODUTOS SEM ID")
print("=" * 60)
print(f"Categorias não identificadas: {nd_cat}")
print(f"Nomes de produto não identificados: {nd_nome}")

# Substituindo N/D por 'SEM CATEGORIA'.
# Usando lambda já que será uso pontual
df_limpo["PR_CAT"] = df_limpo["PR_CAT"].apply(
    lambda x: "SEM CATEGORIA" if x == "#N/D" else x
)
print("Nomenclatura padronizada para 'SEM CATEGORIA'")
print()


# 5. Estatísticas para a coluna filho
filhos = df_limpo["CL_FHL"]
print("=" * 60)
print("📊 ESTATÍSTICA DE FILHOS")
print("=" * 60)
print(f"Média: {filhos.mean():.2f}")
print(f"Mediana: {filhos.median()}")
print(f"Moda: {filhos.mode()[0]}")
print(f"Desvio padrão: {filhos.std():.2f}")
print(f"Máximo: {filhos.max()}")
print(f"Mínimo: {filhos.min()}")
print("\nQuartis e contagem:")
print(filhos.describe())
print()

# 6. Análise de Outliers
print("=" * 60)
print("🔍 ANÁLISE DE OUTLIERS")
print("=" * 60)
Q1 = df_limpo["CL_FHL"].quantile(0.25)
Q3 = df_limpo["CL_FHL"].quantile(0.75)

IQR = Q3 - Q1

lim_inf = Q1 - 1.5 * IQR
lim_sup = Q3 + 1.5 * IQR

outliers = df_limpo[
    (df_limpo["CL_FHL"] < lim_inf) |
    (df_limpo["CL_FHL"] > lim_sup)
]

print(f"Outliers encontrados: {len(outliers)}")
print()

# 7. Agrupamentos para conseguir insights
# Gerando um Resumo de Gênero
print("=" * 60)
print("📊 RESUMO GÊNERO")
print("=" * 60)
resumo_genero = df_limpo.groupby("CL_GENERO").agg(
    compras=("CO_ID", "nunique"),
    clientes_unicos=("CL_ID", "nunique"),
    media_filhos=("CL_FHL", "mean")
)
print(resumo_genero)
print()

# Gerando os 10 produtos mais vendidos
print("=" * 60)
print("📊 TOP 10 PRODUTOS VENDIDOS")
print("=" * 60)
top_produtos = df_limpo.groupby("PR_NOME").agg(
    total_vendido=("PR_ID", "count"),
    em_quantas_compras=("CO_ID", "nunique")
).sort_values("total_vendido", ascending=False).head(10)
print(top_produtos)
print()

# Gerando Resumo por Categoria
print("=" * 60)
print("📊 RESUMO POR CATEGORIA")
print("=" * 60)
resumo_categoria = df_limpo.groupby("PR_CAT").agg(
    total_vendas=("CO_ID", "count"),
    compras_unicas=("CO_ID", "nunique"),
    produtos=("PR_ID", "nunique")
).sort_values("total_vendas", ascending=False)
print(resumo_categoria)
print()

# Gerando Resumo por Classe Social
print("=" * 60)
print("📊 CATEGORIAS POR CLASSE SOCIAL")
print("=" * 60)
pivot_segmento = pd.pivot_table(
    df_limpo,
    index="PR_CAT",
    columns="CL_SEG",
    values="CO_ID",
    aggfunc="count",
    fill_value=0
)
print(pivot_segmento)
print()

# Gerando Categorias mais vendidas por gênero
print("=" * 60)
print("📊 CATEGORIAS POR GÊNERO")
print("=" * 60)
pivot_genero = pd.pivot_table(
    df_limpo,
    values="CO_ID",
    index="PR_CAT",
    columns="CL_GENERO",
    aggfunc="count",
    fill_value=0,
)
print(pivot_genero)
print()

# 8. Gerando um gráfico de barras para vendas por categoria
print("=" * 60)
print("📊 GERANDO GRÁFICO — TOTAL DE ITENS VENDIDOS POR CATEGORIA")
print("=" * 60)

categorias = resumo_categoria.index
total_itens = resumo_categoria["total_vendas"]
cores = sns.color_palette('Set2', n_colors=7)

fig, ax = plt.subplots(figsize=(10, 6))

barras = ax.bar(categorias,
                total_itens,
                color=cores,
                width=0.6,
                edgecolor='white',
                linewidth=1.5)

for barra in barras:
    total = barra.get_height()
    ax.text(
        barra.get_x() + barra.get_width() / 2,
        total + 5000,
        f'{int(total):,}',
        ha='center',
        va='bottom',
        fontsize=9,
        fontweight='bold'
    )

ax.set_title("Total de itens vendidos por categoria", fontsize=14, fontweight='bold')
ax.set_xlabel("Categoria", fontsize=12)
ax.set_ylabel("Total de itens", fontsize=12)

ax.yaxis.grid(True, linestyle='-', alpha=0.4)
ax.set_axisbelow(True)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig("reports/grafico_categorias.png")
plt.show()
print("Gráfico salvo em reports/grafico_categorias.png")
print()

# 9. Salvando base limpa
print("=" * 60)
print("📋 SALVANDO BASE LIMPA")
print("=" * 60)
df_limpo.to_csv("data/processed/df_limpo.csv", index=False)
print("Base limpa salva em data/processed/df_limpo.csv")
print()

# 10. Conclusões
print("=" * 60)
print("📋 CONCLUSÕES")
print("=" * 60)
print("Foram removidos 96.553 registros duplicados.")
print("Quatro colunas continham apenas valores nulos e foram removidas.")
print("A média dos filhos dos clientes foi de 1,15.")
print(("A categoria ALIMENTOS foi a mais vendida"))