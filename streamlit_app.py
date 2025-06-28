import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Configuração da página
st.set_page_config(page_title="Reviews de Jogos", layout="wide")

# Carrega o dataset
try:
    df = pd.read_csv("video_game_reviews.csv")
except FileNotFoundError:
    st.error("❌ Arquivo 'video_game_reviews.csv' não encontrado.")
    st.markdown("Faça upload manual ou baixe de: [Kaggle - Video Game Reviews](https://www.kaggle.com/datasets/jahnavipaliwal/video-game-reviews-and-ratings)")
    st.stop()

# Inicializa estado
if "plataforma_selecionada" not in st.session_state:
    st.session_state.plataforma_selecionada = None

# Título
st.title("🎮 Análise Interativa de Reviews de Jogos")

# Imagens por plataforma
imagens_plataformas = {
    'PC': 'https://cdn-icons-png.flaticon.com/512/732/732225.png',
    'PlayStation': 'https://upload.wikimedia.org/wikipedia/commons/4/4e/Playstation_logo_colour.svg',
    'Xbox': 'https://upload.wikimedia.org/wikipedia/commons/f/f9/Xbox_one_logo.svg',
    'Mobile': 'https://upload.wikimedia.org/wikipedia/commons/2/2d/Mobile-Smartphone-icon.png',
    'Nintendo Switch': 'https://www.nintendo.co.jp/common/v2/img/ncommon/_common/logo/switch.svg'
}

# Plataformas disponíveis no dataset
plataformas_disponiveis = [p for p in imagens_plataformas.keys() if p in df['Platform'].unique()]

# Interface visual com pulse apenas na plataforma selecionada
st.subheader("🕹️ Selecione uma plataforma:")

colunas = st.columns(len(plataformas_disponiveis))
for i, plataforma in enumerate(plataformas_disponiveis):
    with colunas[i]:
        if st.button(plataforma, key=f"botao_{plataforma}"):
            st.session_state.plataforma_selecionada = plataforma

# Redesenha os ícones com o efeito na imagem selecionada
colunas2 = st.columns(len(plataformas_disponiveis))
for i, plataforma in enumerate(plataformas_disponiveis):
    with colunas2[i]:
        if st.session_state.plataforma_selecionada == plataforma:
            components.html(f"""
                <style>
                    @keyframes pulse {{
                        0% {{ transform: scale(1); }}
                        50% {{ transform: scale(1.1); }}
                        100% {{ transform: scale(1); }}
                    }}
                    .pulse {{
                        animation: pulse 1s infinite;
                        width: 80px;
                    }}
                </style>
                <div style="text-align:center;">
                    <img src="{imagens_plataformas[plataforma]}" class="pulse">
                    <p>{plataforma}</p>
                </div>
            """, height=130)
        else:
            st.image(imagens_plataformas[plataforma], width=80, caption=plataforma)

# Se nenhuma plataforma foi escolhida ainda
if not st.session_state.plataforma_selecionada:
    st.stop()

# Dados filtrados
plataforma = st.session_state.plataforma_selecionada
df_plataforma = df[df['Platform'] == plataforma]

# Gêneros disponíveis
generos = df_plataforma['Genre'].dropna().unique()
genero = st.selectbox("📂 Escolha um gênero:", sorted(generos))

# Filtra por gênero
df_filtrado = df_plataforma[df_plataforma['Genre'] == genero]

# Exibe jogos
st.subheader(f"📋 Jogos para {plataforma} no gênero '{genero}'")
st.dataframe(df_filtrado[['Game Title']].reset_index(drop=True))

# Detalhes
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
