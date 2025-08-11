import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
# Define o título da página, o ícone e o layout para ocupar a largura inteira.
st.set_page_config(
    page_title="Filmes Avaliados",
    page_icon="icon.png",
    layout="wide",
)

# --- Carregamento dos dados ---
df = pd.read_csv('NotasFilmes_gpt.csv', encoding='latin1')

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")# Preparar as opções para cada filtro
pais_opcao = ['Todos'] + list(df['Pais'].unique())
ano_opcao = ['Todos'] + sorted(df['Ano'].unique().tolist())
nota_opcao = ['Todos'] + sorted(df['Nota'].unique().tolist())
custo_opcao = ['Todos'] + sorted(df['Custo'].unique().tolist())
lucro_opcao = ['Todos'] + sorted(df['Lucro'].unique().tolist())

# Filtros na sidebar
ano_selecionado = st.sidebar.selectbox('Ano', ano_opcao)
pais_selecionado = st.sidebar.selectbox('Pais', pais_opcao)
custo_selecionado = st.sidebar.selectbox('Custo', custo_opcao)
lucro_selecionado = st.sidebar.selectbox('Lucro', lucro_opcao)
nota_selecionada = st.sidebar.selectbox('Notas', nota_opcao)

# Agora use essas variáveis para filtrar seu DataFrame normalmente


# Preparar as opções para cada filtro (igual antes)
pais_opcao = ['Todos'] + list(df['Pais'].unique())
ano_opcao = ['Todos'] + sorted(df['Ano'].unique().tolist())
nota_opcao = ['Todos'] + sorted(df['Nota'].unique().tolist())
custo_opcao = ['Todos'] + sorted(df['Custo'].unique().tolist())
lucro_opcao = ['Todos'] + sorted(df['Lucro'].unique().tolist())
    
# Agora filtra o dataframe conforme escolhas
df_filtrado = df.copy()# 1. Configurações e imports

# 3. Exibe o título e descrição do dashboard
st.title( "🎞️ Dashboard de Análise de Filmes Avaliados")
st.markdown("Explore os dados dos meus filme avaliados nos últimos anos. Utilize os filtros para refinar sua análise.")

# 4. Calcula e mostra as métricas (KPIs)
st.subheader("Métricas gerais")

if not df_filtrado.empty:
    nota_media = df_filtrado['Nota'].mean()
    lucro_maximo = df_filtrado['Lucro'].max()
    total_registros = df_filtrado.shape[0]
    custo_maximo = df_filtrado['Custo'].max()
else:
    nota_media, lucro_maximo, total_registros, custo_maximo = 0, 0, 0, 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Nota média", f"{nota_media:.2f}")
col2.metric("Lucro máximo", f"${lucro_maximo:,.0f}")
col3.metric("Total de filmes", f"{total_registros:,}")
col4.metric("Custo máximo", f"${custo_maximo:,.0f}")

st.markdown("---")


col_graf1, col_graf2 = st.columns(2)

def new_func(ano_selecionado, df_filtrado):
    if not df_filtrado.empty:
        # Ranking por ano: média das notas por filme naquele ano, top 10
        top_filmes_ano = (
            df_filtrado.groupby(['Ano', 'Filme'])['Nota']
            .mean()
            .reset_index()
        )
        
        # Se quiser o ranking para o ano selecionado, use o filtro do ano, senão geral:
        if ano_selecionado != 'Todos':
            top_ano = top_filmes_ano[top_filmes_ano['Ano'] == ano_selecionado]
            top_ano = top_ano.nlargest(10, 'Nota').sort_values('Nota', ascending=True)
            titulo = f"Top 10 filmes com maiores avaliações em {ano_selecionado}"
        else:
            # Gráfico geral: top 10 filmes com maior média geral
            geral = df_filtrado.groupby('Filme')['Nota'].mean().reset_index()
            top_ano = geral.nlargest(10, 'Nota').sort_values('Nota', ascending=True)
            titulo = "Top 10 filmes com maiores avaliações gerais"
        
        grafico_filmes = px.bar(
            top_ano,
            x='Nota',
            y='Filme',
            orientation='h',
            title=titulo,
            labels={'Notas': 'Média das Notas', 'Filme': 'Filme'}
        )
        grafico_filmes.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_filmes, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de filmes.")

with col_graf1:
    new_func(ano_selecionado, df_filtrado)

import plotly.express as px

with col_graf2:
    if not df_filtrado.empty:
        # Agrupa lucro médio por país
        lucro_medio_pais = df_filtrado.groupby('Pais')['Lucro'].mean().reset_index()
        
        grafico_paises = px.choropleth(
            lucro_medio_pais,
            locations='Pais',
            locationmode='country names',  # usa nome do país
            color='Lucro',
            color_continuous_scale='RdYlGn',
            title='Lucro médio dos filmes por país',
            labels={'Lucro': 'Lucro médio (USD)', 'Pais': 'País'}
        )
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.")

# 5. Depois seu resto do conteúdo, gráficos etc.

if pais_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Pais'] == pais_selecionado]

if ano_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Ano'] == ano_selecionado]

if nota_selecionada != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Nota'] == nota_selecionada]

if custo_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Custo'] == custo_selecionado]

if lucro_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Lucro'] == lucro_selecionado]

# Exibe os dados filtrados
st.dataframe(df_filtrado)



