# Análise Exploratória de Dados — Base Varejo

Mini-projeto avaliativo do Módulo 1 do curso Análise de Dados com Python - T2, do programa SCTEC.

Neste trabalho, foi realizada uma análise exploratória da base de dados Base_Varejo utilizando a biblioteca pandas. O objetivo foi aplicar os conceitos apresentados nas aulas, como a importação de dados, limpeza, tratamento de inconsistências, geração de estatísticas e agrupamentos.

---

## Como executar

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o script:

```bash
python notebook/Miniprojeto_RodolfoZalzwedelEspinola_Analise_de_Dados_T2.py
```

O arquivo `Base_Varejo.csv` precisa estar dentro da pasta `data/raw`.

---

## Insights obtidos

**1. A categoria Alementos foi a mais representativa da base**
A categoria Aliemntos concentrou 384.197 registros, representando mais da metade de toda a base. Também foi a categoria com a maior quantidade de produtos cadastrados, com 120 produtos únicos.

**2. Mulheres são a maioria dos clientes**
Nos agrupamentos realizados por gênero, foram identificados 519 clientes do sexo feminino e 481 clientes do sexo masculino. Além disso, as mulheres têm a maior quantidade de registros de compra em todas as categorias.

**3. Classe B concentra a maior parte das vendas**
Entre todas as categorias, os clientes classificados como classe econômica B apresentaram a maior quantidade de registros de compra.

**4. Presunto cozido destoa de todos os outros produtos**
Com 12.719 vendas, tem quase o dobro do segundo produto mais vendido, a Sardinha com 6610 registros.

**5. Foram encontrados registros sem categoria identificada**
Os 3.228 registros que vieram com "#N/D" nas colunas de categoria e nome do produto foram padronizados para "Sem Categoria".

---

## Reflexão sobre ETL e qualidade de dados

O mini-projeto conseguiu demonstrar a especificidades de um trabalho de análise de dados, incluindo a importãncia de preparar os dados antes de iniciar qualquer análise.

A base continha 830.000 linhas. Entre os problemas encontrados, havia registros duplicados, colunas totalmetne vazias e categorias preenchidas com valores inválidos.

Mais de 96.000 linhas totalmente duplicadas foram removidas, além de quatro colunas que continham apenas valores nulos. São números que poderiam inflar as contagens e exigir processamento desnecessário.

Outro passo realizado foi a conversão da coluna DATA para o formato datetime. A conversão permite futuras analises temporais e evita problemas relacionados os tipo de dados.

A padronização do texto, neste caso com `.strip().upper`, também foi uma etapa realizada. Sem a padronização, diferenças causadas por espaços ou variações de escrita, como "alimentos" e "ALIMENTOS", seriam agrupadas de forma distinta, sem consistência.

Uma das descobertas do projeto, é que muitas vezes questões sobre a qualidade dos dados são descobertas a medida que a análise avança, cabendo ao analista testar diferentes agupamentos e análises para ter uma melhor compreensão sobre os dados.
