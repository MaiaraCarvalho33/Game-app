import streamlit as st
import pandas as pd

# Configura a página
st.set_page_config(page_title="Reviews de Jogos", layout="wide")

# Carrega o dataset
try:
    df = pd.read_csv("video_game_reviews.csv")
except FileNotFoundError:
    st.error("❌ Arquivo 'video_game_reviews.csv' não encontrado.")
    st.markdown("Faça upload manual ou baixe de: [Kaggle - Video Game Reviews](https://www.kaggle.com/datasets/jahnavipaliwal/video-game-reviews-and-ratings)")
    st.stop()

# Título
st.title("🎮 Análise Interativa de Reviews de Jogos")

# Filtro por plataforma
plataformas = df['Platform'].dropna().unique()
plataforma = st.selectbox("🕹️ Escolha uma plataforma:", sorted(plataformas))

# Filtra por plataforma
df_plataforma = df[df['Platform'] == plataforma]

# Filtro por gênero (com base na plataforma)
generos = df_plataforma['Genre'].dropna().unique()
genero = st.selectbox("📂 Escolha um gênero:", sorted(generos))

# Filtra por gênero também
df_filtrado = df_plataforma[df_plataforma['Genre'] == genero]

# Mostra os jogos disponíveis com base nos filtros
st.subheader(f"📋 Jogos para {plataforma} no gênero '{genero}'")
st.dataframe(df_filtrado[['Game Title', 'User Rating', 'User Review Text']].reset_index(drop=True))

# Detalhes do jogo selecionado (com base nos dois filtros)
st.subheader("🔍 Detalhes do Jogo Selecionado")
titulos_filtrados = df_filtrado['Game Title'].unique()

if len(titulos_filtrados) == 0:
    st.warning("⚠️ Nenhum jogo encontrado com os filtros selecionados.")
else:
    jogo = st.selectbox("🎮 Selecione um jogo:", titulos_filtrados)
    detalhes = df_filtrado[df_filtrado['Game Title'] == jogo].iloc[0]

    st.markdown(f"""
    **🎮 Título:** {detalhes['Game Title']}  
    **🧬 Gênero:** {detalhes['Genre']}  
    **⭐ Avaliação dos Usuários:** {detalhes['User Rating']}  
    **💰 Preço:** {detalhes['Price']}  
    **📝 Review:** {detalhes['User Review Text']}  
    **🎮 Modo de Jogo:** {detalhes['Game Mode']}  
    **👥 Número Mínimo de Jogadores:** {detalhes['Min Number of Players']}  
    """)
