import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit.components.v1 as components
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# ========== CONFIGURAÇÃO INICIAL ==========
st.set_page_config(page_title="Reviews de Jogos", layout="wide")

# ===== CSS GLOBAL PARA BOTÕES ESTILIZADOS =====
st.markdown("""
    <style>
    .stButton > button {
        background-color: #2563eb !important;
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 8px 16px;
        font-weight: 500;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #1d4ed8 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ====== ABAS DE NAVEGAÇÃO ======
abas = {
    "🏠 Página Inicial": "inicio",
    "📊 Estatísticas": "estatisticas",
    "🎯 Sugestões Personalizadas": "recomendador",
    "🔍 Buscador de Jogos": "buscar",
    "💬 Análise de Reviews": "reviews",
    "📂 Pré-processamento ": "Pré-processamento",
    "🧠 Modelo de ML": "modelo",
    "📘 Sobre": "sobre"
}

cols = st.columns(len(abas))
if "aba_ativa" not in st.session_state:
    st.session_state.aba_ativa = "inicio"
for i, (nome, chave) in enumerate(abas.items()):
    with cols[i]:
        if st.button(nome):
            st.session_state.aba_ativa = chave
aba = st.session_state.aba_ativa

# ====== CARREGAMENTO DO DATASET ======
try:
    df = pd.read_csv("video_game_reviews.csv")
except FileNotFoundError:
    st.error("❌ Arquivo 'video_game_reviews.csv' não encontrado.")
    st.markdown("🔗 Baixe o dataset em: [Kaggle - Video Game Reviews](https://www.kaggle.com/datasets/jahnavipaliwal/video-game-reviews-and-ratings)")
    st.stop()


# ======================= INÍCIO ========================
if aba == "inicio":
    st.title("🎮 Análise Interativa de Reviews de Jogos")

    imagens_plataformas = {
        'PC': 'https://cdn-icons-png.flaticon.com/512/732/732225.png',
        'PlayStation': 'https://upload.wikimedia.org/wikipedia/commons/4/4e/Playstation_logo_colour.svg',
        'Xbox': 'https://upload.wikimedia.org/wikipedia/commons/f/f9/Xbox_one_logo.svg',
        'Mobile': 'https://upload.wikimedia.org/wikipedia/commons/2/2d/Mobile-Smartphone-icon.png',
        'Nintendo Switch': 'https://www.nintendo.co.jp/common/v2/img/ncommon/_common/logo/switch.svg'
    }

    if "plataforma_selecionada" not in st.session_state:
        st.session_state.plataforma_selecionada = None
    if "genero_selecionado" not in st.session_state:
        st.session_state.genero_selecionado = None

    plataformas_disponiveis = [p for p in imagens_plataformas if p in df['Platform'].unique()]
    st.subheader("Selecione uma plataforma:")

    colunas = st.columns(len(plataformas_disponiveis))
    for i, plataforma in enumerate(plataformas_disponiveis):
        with colunas[i]:
            if st.button(plataforma, key=f"botao_{plataforma}"):
                st.session_state.plataforma_selecionada = plataforma

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

    if not st.session_state.plataforma_selecionada:
        st.stop()

    plataforma = st.session_state.plataforma_selecionada
    df_plataforma = df[df['Platform'] == plataforma]

    icones_generos = {
        'Action': 'https://cdn-icons-png.flaticon.com/512/16391/16391182.png',
        'Adventure': 'https://cdn-icons-png.flaticon.com/512/5064/5064012.png',
        'RPG': 'https://cdn-icons-png.flaticon.com/512/10069/10069327.png',
        'Shooter': 'https://cdn-icons-png.flaticon.com/512/1030/1030305.png',
        'Puzzle': 'https://cdn-icons-png.flaticon.com/512/3162/3162297.png',
        'Sports': 'https://cdn-icons-png.flaticon.com/512/4163/4163679.png',
        'Racing': 'https://cdn-icons-png.flaticon.com/512/4259/4259278.png',
        'Fighting': 'https://cdn-icons-png.flaticon.com/512/2735/2735992.png',
        'Simulation': 'https://cdn-icons-png.flaticon.com/512/12011/12011550.png',
        'Strategy': 'https://cdn-icons-png.flaticon.com/512/3281/3281104.png',
        'Platformer': 'https://cdn-icons-png.flaticon.com/512/7401/7401039.png'
    }

    generos_disponiveis = [g for g in icones_generos if g in df_plataforma['Genre'].unique()]
    st.subheader(" Selecione um gênero:")

    colunas_gen = st.columns(len(generos_disponiveis))
    for i, genero_nome in enumerate(generos_disponiveis):
        with colunas_gen[i]:
            if st.button(genero_nome, key=f"botao_genero_{genero_nome}"):
                st.session_state.genero_selecionado = genero_nome

    colunas_gen2 = st.columns(len(generos_disponiveis))
    for i, genero_nome in enumerate(generos_disponiveis):
        with colunas_gen2[i]:
            if st.session_state.genero_selecionado == genero_nome:
                components.html(f"""
                    <style>
                        @keyframes pulse {{
                            0% {{ transform: scale(1); }}
                            50% {{ transform: scale(1.15); }}
                            100% {{ transform: scale(1); }}
                        }}
                        .pulse {{
                            animation: pulse 1s infinite;
                            width: 60px;
                        }}
                    </style>
                    <div style="text-align:center;">
                        <img src="{icones_generos[genero_nome]}" class="pulse">
                        <p>{genero_nome}</p>
                    </div>
                """, height=130)
            else:
                st.image(icones_generos[genero_nome], width=60, caption=genero_nome)

    if not st.session_state.genero_selecionado:
        st.stop()

    genero = st.session_state.genero_selecionado
    df_filtrado = df_plataforma[df_plataforma['Genre'] == genero]

    st.subheader(f" Jogos para {plataforma} no gênero '{genero}'")
    st.table(df_filtrado[['Game Title']].drop_duplicates().reset_index(drop=True))

elif aba == "estatisticas":
    st.title(" Estatísticas")

    # ==== GRÁFICO 1: Quantidade de Jogos por Plataforma ====
    st.subheader(" Quantidade de Jogos por Plataforma")

    if 'Min Number of Players' in df.columns:
        df_jogos = df.dropna(subset=['Min Number of Players'])
        contagem_jogos = df_jogos.groupby('Platform').size().reset_index(name='Quantidade')

        fig1 = px.bar(
            contagem_jogos,
            x='Platform',
            y='Quantidade',
            color='Quantidade',
            color_continuous_scale='blues',
            title=None
        )
        fig1.update_layout(
            xaxis_title="Plataforma",
            yaxis_title="Quantidade de Jogos",
            showlegend=False,
            hovermode=False,
            height=400,
            template="simple_white"
        )
        fig1.update_traces(textposition="none")
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.warning(" Coluna 'Min Number of Players' não encontrada.")

    # ==== GRÁFICO 2: Evolução das Avaliações ao Longo do Tempo ====
    st.subheader(" Evolução das Avaliações ao Longo do Tempo")

    ano_col = next((col for col in df.columns if col.lower() in ['year', 'release year']), None)

    if ano_col:
        df_ano = df.dropna(subset=['User Rating', ano_col])
        df_ano[ano_col] = df_ano[ano_col].astype(int)
        media_ano = df_ano.groupby(ano_col)['User Rating'].mean().reset_index().sort_values(by=ano_col)

        fig2 = px.line(
            media_ano,
            x=ano_col,
            y='User Rating',
            title=None,
            markers=True
        )
        fig2.update_traces(mode='lines+markers', line_shape='spline')
        fig2.update_layout(
            xaxis_title="Ano de Lançamento",
            yaxis_title="Média das Avaliações",
            hovermode='x unified',
            height=400,
            template='simple_white'
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning(" Coluna de ano ('Year' ou 'Release Year') não encontrada.")

    # ==== GRÁFICO 3: Top 10 Jogos com Melhor Avaliação ====
    st.subheader(" Top 10 Jogos com Melhor Avaliação")

    top10 = df[['Game Title', 'User Rating']].dropna().drop_duplicates()
    top10 = top10.sort_values(by='User Rating', ascending=False).head(10)

    fig3 = px.bar(
        top10,
        x='Game Title',
        y='User Rating',
        color='User Rating',
        color_continuous_scale='reds'
    )
    fig3.update_traces(textposition='none')
    fig3.update_layout(
        xaxis_title="Jogo",
        yaxis_title="Nota do Usuário",
        showlegend=False,
        height=400,
        template="simple_white"
    )
    st.plotly_chart(fig3, use_container_width=True)

    # ==== GRÁFICO 4: Modos de Jogo Disponíveis (Multiplayer ou Não) ====
    st.subheader(" Modos de Jogo Disponíveis")

    modo_coluna = next((col for col in df.columns if col.lower() in ['game mode', 'mode', 'multiplayer']), None)

    if modo_coluna:
        df[modo_coluna] = df[modo_coluna].astype(str).str.strip().str.lower()
        df['Modo de Jogo'] = df[modo_coluna].apply(
            lambda x: 'Multiplayer' if x in ['yes', 'true', '1'] else 'Singleplayer'
        )

        modos_contagem = df['Modo de Jogo'].value_counts().reset_index()
        modos_contagem.columns = ['Modo de Jogo', 'Quantidade']

        fig_modos = px.bar(
            modos_contagem,
            x='Modo de Jogo',
            y='Quantidade',
            color='Modo de Jogo',
            color_discrete_map={'Multiplayer': '#2ecc71', 'Singleplayer': '#e74c3c'}
        )
        fig_modos.update_traces(marker_line_color='black', marker_line_width=1.2)
        fig_modos.update_layout(
            title="Distribuição de Jogos Multiplayer e Singleplayer",
            xaxis_title="Modo de Jogo",
            yaxis_title="Número de Jogos",
            showlegend=False,
            height=400,
            template="simple_white"
        )
        st.plotly_chart(fig_modos, use_container_width=True)
    else:
        st.warning(" Nenhuma coluna de modo de jogo encontrada no dataset.")







# ============== SUGESTÕES PERSONALIZADAS =================
elif aba == "recomendador":
    st.title("🎯 Sugestões Personalizadas")

    genero = st.selectbox(" Gênero:", sorted(df['Genre'].dropna().unique()))
    faixa_preco = st.slider(" Preço (USD):", float(df['Price'].min()), float(df['Price'].max()), (0.0, 60.0))
    faixa_nota = st.slider(" Avaliação:", float(df['User Rating'].min()), float(df['User Rating'].max()), (0.0, 5.0))

    recomendados = df[
        (df['Genre'] == genero) &
        (df['Price'].between(*faixa_preco)) &
        (df['User Rating'].between(*faixa_nota))
    ][['Game Title', 'Platform', 'Price', 'User Rating']].drop_duplicates()

    st.subheader(" Jogos Recomendados")

    if recomendados.empty:
        st.warning(" Não foi possível encontrar jogos com os critérios selecionados.")
    else:
        st.dataframe(recomendados.reset_index(drop=True), use_container_width=True)

# ===== ABA: BUSCADOR DE JOGOS =====

# ===== ABA: BUSCADOR DE JOGOS =====

# DEFINA O DICIONÁRIO AQUI 👇👇👇
icones_generos = {
    'Action': 'https://cdn-icons-png.flaticon.com/512/16391/16391182.png',
    'Adventure': 'https://cdn-icons-png.flaticon.com/512/5064/5064012.png',
    'RPG': 'https://cdn-icons-png.flaticon.com/512/10069/10069327.png',
    'Shooter': 'https://cdn-icons-png.flaticon.com/512/1030/1030305.png',
    'Puzzle': 'https://cdn-icons-png.flaticon.com/512/3162/3162297.png',
    'Sports': 'https://cdn-icons-png.flaticon.com/512/4163/4163679.png',
    'Racing': 'https://cdn-icons-png.flaticon.com/512/4259/4259278.png',
    'Fighting': 'https://cdn-icons-png.flaticon.com/512/2735/2735992.png',
    'Simulation': 'https://cdn-icons-png.flaticon.com/512/12011/12011550.png',
    'Strategy': 'https://cdn-icons-png.flaticon.com/512/3281/3281104.png',
    'Platformer': 'https://cdn-icons-png.flaticon.com/512/7401/7401039.png'
}

# CORRETO AGORA:
if aba == "buscar":
    st.title("🔍 Buscador de Jogos")

    # Seleção do jogo
    jogo = st.selectbox("Digite ou selecione um jogo:", sorted(df['Game Title'].dropna().unique()))
    dados = df[df['Game Title'] == jogo].iloc[0]

    # Ícone do gênero
    genero = dados['Genre']
    icone_genero = icones_generos.get(genero, "https://cdn-icons-png.flaticon.com/512/5064/5064012.png")

    # Cartão com os dados e ícones com efeito glow
    st.markdown(f"""
    <style>
    .icone-glow:hover {{
        filter: drop-shadow(0 0 5px #2563eb);
        transition: 0.3s ease;
    }}
    </style>

    <div style="background-color:#f4f8ff; padding:20px; border-radius:12px; 
                box-shadow: 2px 2px 8px rgba(0,0,0,0.1); font-family:Segoe UI;">
      <h4 style="margin-top:0;">
        <img src="https://cdn-icons-png.flaticon.com/512/4738/4738879.png" class="icone-glow" width="28" 
             style="vertical-align:middle; margin-right:8px;">
        <b>{dados['Game Title']}</b>
      </h4>

      <p>
        <img src="https://cdn-icons-png.flaticon.com/512/942/942826.png" class="icone-glow" width="20" style="vertical-align:middle;"> 
        <strong>Avaliação:</strong> <span style="color:#2563eb;">{dados['User Rating']}</span>
      </p>

      <p>
        <img src="{icone_genero}" class="icone-glow" width="20" style="vertical-align:middle;"> 
        <strong>Gênero:</strong> {genero}
      </p>

      <p>
        <img src="https://cdn-icons-png.flaticon.com/512/8228/8228400.png" class="icone-glow" width="20" style="vertical-align:middle;"> 
        <strong>Review:</strong> <i>“{dados['User Review Text']}”</i>
      </p>

      <p>
        <img src="https://cdn-icons-png.flaticon.com/512/15408/15408140.png" class="icone-glow" width="20" style="vertical-align:middle;"> 
        <strong>Modo de Jogo:</strong> {dados['Game Mode']}
      </p>

      <p>
        <img src="https://cdn-icons-png.flaticon.com/512/8436/8436229.png" class="icone-glow" width="20" style="vertical-align:middle;"> 
        <strong>Preço:</strong> <span style="color:green;">R$ {dados['Price']:.2f}</span>
      </p>
    </div>
    """, unsafe_allow_html=True)





if aba == "reviews":
    st.title(" Análise de Reviews")

    from streamlit.components.v1 import html

    icones_generos = {
        'Action': 'https://cdn-icons-png.flaticon.com/512/16391/16391182.png',
        'Adventure': 'https://cdn-icons-png.flaticon.com/512/5064/5064012.png',
        'RPG': 'https://cdn-icons-png.flaticon.com/512/10069/10069327.png',
        'Shooter': 'https://cdn-icons-png.flaticon.com/512/1030/1030305.png',
        'Puzzle': 'https://cdn-icons-png.flaticon.com/512/3162/3162297.png',
        'Sports': 'https://cdn-icons-png.flaticon.com/512/4163/4163679.png',
        'Racing': 'https://cdn-icons-png.flaticon.com/512/4259/4259278.png',
        'Fighting': 'https://cdn-icons-png.flaticon.com/512/2735/2735992.png',
        'Simulation': 'https://cdn-icons-png.flaticon.com/512/12011/12011550.png',
        'Strategy': 'https://cdn-icons-png.flaticon.com/512/3281/3281104.png',
        'Platformer': 'https://cdn-icons-png.flaticon.com/512/7401/7401039.png'
    }

    generos_disponiveis = [g for g in icones_generos if g in df['Genre'].unique()]
    st.subheader(" Selecione um gênero:")

    colunas_gen = st.columns(len(generos_disponiveis))
    for i, genero_nome in enumerate(generos_disponiveis):
        with colunas_gen[i]:
            if st.button(genero_nome, key=f"btn_review_genero_{genero_nome}"):
                st.session_state.genero_review = genero_nome

    if "genero_review" not in st.session_state:
        st.stop()

    genero_escolhido = st.session_state.genero_review

    colunas_gen2 = st.columns(len(generos_disponiveis))
    for i, genero_nome in enumerate(generos_disponiveis):
        with colunas_gen2[i]:
            if genero_nome == genero_escolhido:
                components.html(f"""
                    <style>
                        @keyframes pulse {{
                            0% {{ transform: scale(1); }}
                            50% {{ transform: scale(1.15); }}
                            100% {{ transform: scale(1); }}
                        }}
                        .pulse {{
                            animation: pulse 1s infinite;
                            width: 60px;
                        }}
                    </style>
                    <div style="text-align:center;">
                        <img src="{icones_generos[genero_nome]}" class="pulse">
                        <p><b>{genero_nome}</b></p>
                    </div>
                """, height=130)
            else:
                st.image(icones_generos[genero_nome], width=60, caption=genero_nome)

    df_gen = df[(df['Genre'] == genero_escolhido) & df['User Review Text'].notna()]

    if df_gen.empty:
        st.warning(" Nenhuma review disponível para este gênero.")
    else:
        st.subheader(" Nuvem de Palavras")
        texto = " ".join(df_gen['User Review Text'].astype(str))
        wordcloud = WordCloud(width=800, height=300, background_color='white').generate(texto)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

        # ========== REVIEWS POSITIVAS ==========
        st.subheader("💚 Reviews mais positivas")
        top_reviews = df_gen.sort_values(by='User Rating', ascending=False).head(5)

        for _, row in top_reviews.iterrows():
            jogo = row['Game Title']
            review = row['User Review Text'][:150] + "..." if len(row['User Review Text']) > 150 else row['User Review Text']
            nota_real = round(row['User Rating'], 1)
            estrelas_qtd = round(nota_real / 20, 2)
            inteiras = int(estrelas_qtd)
            meia = 0.5 if estrelas_qtd - inteiras >= 0.25 and estrelas_qtd - inteiras < 0.75 else 0
            vazias = 5 - inteiras - (1 if meia else 0)
            estrelas_html = (
                '<span class="dourado">★</span>' * inteiras +
                ('<span class="dourado" style="opacity:0.5;">★</span>' if meia else '') +
                '<span class="cinza">★</span>' * vazias
            )

            html(f"""
            <style>
                .card {{
                    background: #e9fbe5;
                    border-radius: 12px;
                    padding: 15px;
                    margin-bottom: 15px;
                    transition: all 0.3s ease;
                    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
                }}
                .card:hover {{
                    background: #d3f5c6;
                    transform: scale(1.02);
                }}
                .stars span {{
                    font-size: 24px;
                    transition: color 0.3s ease;
                }}
                .stars .dourado {{
                    color: gold;
                }}
                .stars .cinza {{
                    color: gray;
                }}
                .emoji {{
                    font-size: 24px;
                    margin-left: 10px;
                }}
            </style>
            <div class="card">
                <b>{jogo} </b><br>
                {review}
                <div class="stars" style="margin-top: 10px;">
                    {estrelas_html} <span class="emoji">{'😊' if nota_real >= 80 else '😐'}</span>
                </div>
            </div>
            """, height=150)

        # ========== REVIEWS NEGATIVAS ==========
        st.subheader("💔 Reviews mais negativas")
        bottom_reviews = df_gen.sort_values(by='User Rating', ascending=True).head(5)

        for _, row in bottom_reviews.iterrows():
            jogo = row['Game Title']
            review = row['User Review Text'][:150] + "..." if len(row['User Review Text']) > 150 else row['User Review Text']
            nota_real = round(row['User Rating'], 1)
            estrelas_qtd = round(nota_real / 20, 2)
            inteiras = int(estrelas_qtd)
            meia = 0.5 if estrelas_qtd - inteiras >= 0.25 and estrelas_qtd - inteiras < 0.75 else 0
            vazias = 5 - inteiras - (1 if meia else 0)
            estrelas_html = (
                '<span class="dourado">★</span>' * inteiras +
                ('<span class="dourado" style="opacity:0.5;">★</span>' if meia else '') +
                '<span class="cinza">★</span>' * vazias
            )

            html(f"""
            <style>
                .card {{
                    background: #fde5e5;
                    border-radius: 12px;
                    padding: 15px;
                    margin-bottom: 15px;
                    transition: background 0.3s ease, transform 0.3s ease;
                    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
                }}
                .card:hover {{
                    background: #f8cccc;
                    transform: scale(1.02);
                }}
                .stars span {{
                    font-size: 24px;
                    transition: color 0.3s ease;
                }}
                .stars .dourado {{
                    color: gold;
                }}
                .stars .cinza {{
                    color: gray;
                }}
                .emoji {{
                    font-size: 24px;
                    margin-left: 10px;
                }}
            </style>
            <div class="card">
                <b>{jogo} </b><br>
                {review}
                <div class="stars" style="margin-top: 10px;">
                    {estrelas_html} <span class="emoji">{'😞' if nota_real < 25 else '😐'}</span>
                </div>
            </div>
            """, height=150)
########
elif aba == "Pré-processamento":
    st.title("Pré-processamento dos Dados")

    # Carregamento do dataset
    try:
        dados = pd.read_csv("video_game_reviews.csv")
    except FileNotFoundError:
        st.error("Arquivo de dados não encontrado. Verifique o nome ou caminho.")
        st.stop()

    # Explicação do Problema
    st.markdown("### Explicação do Problema")
    st.markdown("""
    O projeto busca prever se um jogo possui modo multiplayer com base em variáveis conhecidas previamente. 
    Essa previsão pode ser útil, por exemplo, para desenvolvedores que desejam estimar características de engajamento do jogo ou para consumidores em sistemas de recomendação.

    A variável alvo é `Multiplayer`, com valores possíveis: Yes ou No — ou seja, trata-se de uma tarefa de classificação binária.
    """)

    # Etapas do Pré-processamento
    st.markdown("### Etapas de Pré-processamento")

    st.markdown("#### 1. Leitura e Análise Inicial")
    st.markdown("""
    O conjunto de dados foi carregado a partir do Kaggle. Para compreender a estrutura e identificar possíveis problemas, 
    realizou-se uma análise exploratória com ferramentas como `pandas_profiling` e inspeção de tipos e consistência das variáveis.
    
    Justificativa: essa etapa inicial é fundamental para entender a qualidade dos dados e direcionar os tratamentos posteriores.
    """)

    # === 2. Criação de Novas Variáveis ===
    st.markdown("#### 2. Criação de Novas Variáveis")
    st.markdown("""
    Foram criadas variáveis auxiliares para capturar informações latentes que podem ajudar na classificação:

    - `Game_Length_Category`: categoriza o tempo de jogo (`Game Length (Hours)`) em Curta, Média ou Longa.
    - `Multiplayer_bin`: conversão da variável alvo para valores numéricos (1 para Yes, 0 para No).
    - `Is_Online`: identifica se o modo principal é online.
    - `Faixa_Preco`: agrupa os jogos em faixas de preço (Baixo, Médio e Alto).

    Justificativa: essas variáveis criam segmentações úteis e padronizadas que facilitam a aprendizagem dos modelos.
    """)

    import numpy as np
    if 'Game Length (Hours)' in dados.columns:
        dados['Game_Length_Category'] = pd.cut(
            dados['Game Length (Hours)'],
            bins=[0, 10, 30, 1000],
            labels=['Curta', 'Média', 'Longa']
        )
    dados['Multiplayer_bin'] = (dados['Multiplayer'].str.strip().str.lower() == 'yes').astype(int)
    dados['Is_Online'] = (dados['Game Mode'].str.strip().str.lower() == 'online').astype(int)
    if 'Price' in dados.columns:
        dados['Faixa_Preco'] = pd.cut(
            dados['Price'],
            bins=[-np.inf, 20, 50, np.inf],
            labels=['Baixo', 'Médio', 'Alto']
        )

    # === 3. Transformações Numéricas ===
    st.markdown("#### 3. Transformações Numéricas")
    st.markdown("""
    As variáveis numéricas `User Rating`, `Price` e `Game Length (Hours)` foram padronizadas com `StandardScaler`.

    Justificativa: a padronização é necessária para evitar que variáveis com escalas muito diferentes influenciem desproporcionalmente os modelos.
    """)

    from sklearn.preprocessing import StandardScaler
    import seaborn as sns  # <- Importação adicionada
    variaveis_continuas = ['User Rating', 'Price', 'Game Length (Hours)']
    for var in variaveis_continuas:
        if var in dados.columns:
            dados[var] = StandardScaler().fit_transform(dados[[var]])

    st.markdown("Distribuição Após Padronização")
    for var in variaveis_continuas:
        if var in dados.columns:
            fig, ax = plt.subplots(figsize=(7, 3))
            sns.histplot(dados[var], kde=True, ax=ax, color='orange')
            ax.set_title(f"{var} - Após Padronização")
            st.pyplot(fig)

    # === 4. Codificação de Categóricas ===
    st.markdown("#### 4. Codificação de Variáveis Categóricas")
    st.markdown("""
    Variáveis como `Genre`, `Platform`, `Game Mode` e `Age Group Targeted` foram codificadas via One-Hot Encoding.

    Justificativa: algoritmos de machine learning não conseguem processar texto diretamente. O One-Hot Encoding converte categorias em colunas binárias.
    """)

    st.markdown("Distribuição dos Gêneros Mais Frequentes")
    import plotly.express as px
    if 'Genre' in dados.columns:
        genero_plot = dados['Genre'].value_counts().reset_index()
        genero_plot.columns = ['Genre', 'Count']
        fig = px.bar(genero_plot.head(10), x='Genre', y='Count', title='Top 10 Gêneros de Jogos')
        st.plotly_chart(fig, use_container_width=True)

    # === 5. Mapeamento de Qualidade ===
    st.markdown("#### 5. Mapeamento de Qualidade")
    st.markdown("""
    Variáveis subjetivas como `Graphics Quality`, `Soundtrack Quality` e `Story Quality` foram convertidas para uma escala ordinal de 1 (pior) a 5 (melhor):

    - Poor → 1  
    - Average → 2  
    - Medium → 3  
    - Good → 4  
    - Excellent → 5

    Justificativa: com a conversão ordinal, os modelos conseguem compreender a ordem de qualidade, permitindo inferências mais precisas.
    """)

    mapa_qualidade = {'Poor': 1, 'Average': 2, 'Medium': 3, 'Good': 4, 'Excellent': 5}
    for col in ['Graphics Quality', 'Soundtrack Quality', 'Story Quality']:
        if col in dados.columns:
            dados[col] = dados[col].map(mapa_qualidade)

    if 'Graphics Quality' in dados.columns:
        st.markdown("Relação entre Qualidade Gráfica e Avaliação do Usuário")
        fig = px.box(dados, x="Graphics Quality", y="User Rating", title="User Rating por Qualidade Gráfica")
        st.plotly_chart(fig, use_container_width=True)

####
elif aba == "modelo":
    st.title("Modelo de Machine Learning")

    # ======== 1. Explicação do Problema =========
    st.markdown("## Explicação do Problema de Machine Learning")
    st.markdown("""
    Este projeto tem como objetivo prever se um jogo possui ou não **modo multiplayer**, com base em informações como:
    - Gênero (`Genre`)
    - Plataforma (`Platform`)
    - Preço (`Price`)

    A variável-alvo é `Multiplayer`, com respostas categóricas: "Yes" ou "No".  
    Assim, trata-se de um **problema de classificação binária**, em que o modelo aprenderá a identificar padrões que indiquem a presença ou ausência do modo multiplayer.
    """)

    # ======== 2. Sobre o Conjunto de Dados =========
    st.markdown("## Conjunto de Dados Utilizado")
    st.markdown("""
    Utiliza-se um subconjunto limpo e pré-processado do dataset original proveniente do Kaggle, contendo:
    - Jogos com valores válidos em `Genre`, `Platform`, `Price` e `Multiplayer`.
    - Conversão da variável `Multiplayer` para formato binário (`Multiplayer_bin`), com 1 representando "Yes" e 0 representando "No".
    """)

    # ======== 3. Importações e Normalização =========
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    import streamlit.components.v1 as components

    df.columns = df.columns.str.strip().str.title().str.replace(" ", "")

    colunas_necessarias = ['Genre', 'Platform', 'Price', 'Multiplayer']
    if df.empty or any(col not in df.columns for col in colunas_necessarias):
        st.warning("O conjunto de dados está incompleto ou não carregado.")
    else:
        # ======== 4. Preparação dos Dados =========
        @st.cache_data
        def preparar_dados(df):
            dados = df[['Genre', 'Platform', 'Price', 'Multiplayer']].dropna()
            dados = dados[dados['Multiplayer'].str.lower().isin(['yes', 'no'])].copy()
            dados['Multiplayer_bin'] = dados['Multiplayer'].str.lower().map({'yes': 1, 'no': 0})
            return dados

        @st.cache_resource
        def treinar_modelo(dados):
            X = dados[['Genre', 'Platform', 'Price']]
            y = dados['Multiplayer_bin']

            preproc = ColumnTransformer([
                ('cat', OneHotEncoder(handle_unknown='ignore'), ['Genre', 'Platform']),
                ('num', StandardScaler(), ['Price'])
            ])

            modelo = Pipeline([
                ('prep', preproc),
                ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
            ])

            modelo.fit(X, y)
            return modelo

        dados = preparar_dados(df)
        modelo = treinar_modelo(dados)

        # ======== 5. Justificativa do Modelo =========
        st.markdown("## Justificativa da Escolha do Modelo")
        st.markdown("""
        O algoritmo escolhido foi o **Random Forest Classifier** pelas seguintes razões:
        - É eficiente para tarefas de classificação com variáveis categóricas e numéricas.
        - Não exige normalidade nos dados e é robusto contra overfitting.
        - Capta relações não lineares e interações entre variáveis de forma automática.
        - É interpretável e tem boa performance em problemas tabulares como este.
        """)

        # ======== 6. HTML – Multiplayer com Tetris ========
        multiplayer_html = '''
        <div id="multiplayer-canvas-container">
          <canvas id="multiplayerCanvas" width="320" height="250"></canvas>
        </div>
        <style>
          #multiplayer-canvas-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #1a1a1a;
            border-radius: 12px;
            box-shadow: 0 0 20px rgba(0,255,0,0.4);
            z-index: 9999;
          }
        </style>
        <script>
        const canvas = document.getElementById("multiplayerCanvas");
        const ctx = canvas.getContext("2d");
        let tetrisY = 0;

        function drawConsole() {
          ctx.fillStyle = "#0ff";
          ctx.fillRect(110, 30, 100, 60);
          ctx.fillStyle = "#000";
          ctx.fillRect(120, 40, 80, 40);

          // Tetris
          ctx.fillStyle = "#0f0"; ctx.fillRect(130, 40 + tetrisY % 40, 10, 10);
          ctx.fillStyle = "#f00"; ctx.fillRect(150, 40 + (tetrisY + 10) % 40, 10, 10);
          ctx.fillStyle = "#00f"; ctx.fillRect(170, 40 + (tetrisY + 20) % 40, 10, 10);

          ctx.fillStyle = "#0ff";
          ctx.fillRect(140, 100, 40, 5);
        }

        function drawController(x, y) {
          ctx.fillStyle = "gray";
          ctx.beginPath();
          ctx.roundRect(x, y, 90, 40, 8); ctx.fill();
          ctx.strokeStyle = "white";
          ctx.beginPath();
          ctx.moveTo(x + 45, y); ctx.bezierCurveTo(x + 45, y - 20, x + 25, y - 25, x + 35, y - 40); ctx.stroke();
          ctx.fillStyle = "black";
          ctx.beginPath(); ctx.arc(x + 15, y + 20, 5, 0, 2*Math.PI); ctx.fill();
          ctx.beginPath(); ctx.arc(x + 70, y + 12, 4, 0, 2*Math.PI); ctx.fill();
          ctx.beginPath(); ctx.arc(x + 80, y + 22, 4, 0, 2*Math.PI); ctx.fill();
          ctx.beginPath(); ctx.arc(x + 70, y + 32, 4, 0, 2*Math.PI); ctx.fill();
          ctx.beginPath(); ctx.arc(x + 60, y + 22, 4, 0, 2*Math.PI); ctx.fill();
        }

        function animate() {
          ctx.clearRect(0, 0, canvas.width, canvas.height);
          drawConsole();
          drawController(50 + Math.sin(Date.now()/300)*4, 160);
          drawController(170 - Math.sin(Date.now()/300)*4, 160);
          tetrisY += 1;
          if (tetrisY > 40) tetrisY = 0;
          requestAnimationFrame(animate);
        }
        animate();
        </script>
        '''

        # ======== 7. HTML – Singleplayer com Tetris ========
        singleplayer_html = '''
        <div id="singleplayer-canvas-container">
          <canvas id="singleCanvas" width="320" height="250"></canvas>
        </div>
        <style>
          #singleplayer-canvas-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #1a1a1a;
            border-radius: 12px;
            box-shadow: 0 0 20px rgba(255,255,0,0.4);
            z-index: 9999;
          }
        </style>
        <script>
        const canvas = document.getElementById("singleCanvas");
        const ctx = canvas.getContext("2d");
        let tetrisY = 0;

        function drawConsole() {
          ctx.fillStyle = "#ff0";
          ctx.fillRect(110, 30, 100, 60);
          ctx.fillStyle = "#000";
          ctx.fillRect(120, 40, 80, 40);

          // Tetris
          ctx.fillStyle = "#0f0"; ctx.fillRect(130, 40 + tetrisY % 40, 10, 10);
          ctx.fillStyle = "#f00"; ctx.fillRect(150, 40 + (tetrisY + 10) % 40, 10, 10);
          ctx.fillStyle = "#00f"; ctx.fillRect(170, 40 + (tetrisY + 20) % 40, 10, 10);

          ctx.fillStyle = "#ff0";
          ctx.fillRect(140, 100, 40, 5);
        }

        function drawController(x, y) {
          ctx.fillStyle = "gray";
          ctx.beginPath();
          ctx.roundRect(x, y, 90, 40, 8); ctx.fill();
          ctx.strokeStyle = "white";
          ctx.beginPath();
          ctx.moveTo(x + 45, y); ctx.bezierCurveTo(x + 45, y - 20, x + 25, y - 25, x + 35, y - 40); ctx.stroke();
          ctx.fillStyle = "black";
          ctx.beginPath(); ctx.arc(x + 15, y + 20, 5, 0, 2*Math.PI); ctx.fill();
          ctx.beginPath(); ctx.arc(x + 70, y + 12, 4, 0, 2*Math.PI); ctx.fill();
          ctx.beginPath(); ctx.arc(x + 80, y + 22, 4, 0, 2*Math.PI); ctx.fill();
          ctx.beginPath(); ctx.arc(x + 70, y + 32, 4, 0, 2*Math.PI); ctx.fill();
          ctx.beginPath(); ctx.arc(x + 60, y + 22, 4, 0, 2*Math.PI); ctx.fill();
        }

        function animate() {
          ctx.clearRect(0, 0, canvas.width, canvas.height);
          drawConsole();
          drawController(115 + Math.sin(Date.now()/300)*5, 160);
          tetrisY += 1;
          if (tetrisY > 40) tetrisY = 0;
          requestAnimationFrame(animate);
        }
        animate();
        </script>
        '''

        # ======== 8. Interface Interativa =========
        st.markdown("## Faça uma Previsão com Base nos Dados")

        genero = st.selectbox("Gênero do jogo", sorted(dados['Genre'].unique()))
        plataforma = st.selectbox("Plataforma", sorted(dados['Platform'].unique()))
        preco = st.slider("Preço do jogo (USD)",
                          int(dados['Price'].min()),
                          int(dados['Price'].max()),
                          int(dados['Price'].median()))

        if st.button("Prever"):
            entrada = pd.DataFrame([[genero, plataforma, preco]], columns=['Genre', 'Platform', 'Price'])
            pred = modelo.predict(entrada)
            prob = modelo.predict_proba(entrada)[0][1]

            st.markdown("### Resultado da Previsão")
            if pred[0] == 1:
                st.success(f"Este jogo provavelmente possui modo multiplayer. Confiança: {prob:.1%}")
                components.html(multiplayer_html, height=280)
            else:
                st.warning(f"Este jogo provavelmente **não** possui modo multiplayer. Confiança: {(1 - prob):.1%}")
                components.html(singleplayer_html, height=280)
######sobre
elif aba == "sobre":
    st.markdown("""
        <style>
            .brilho {
                font-size: 36px;
                font-weight: bold;
                background: linear-gradient(90deg, #007cf0, #00dfd8, #007cf0);
                background-size: 300%;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: brilho 4s ease-in-out infinite;
                text-align: center;
            }

            @keyframes brilho {
                0% { background-position: 0% }
                50% { background-position: 100% }
                100% { background-position: 0% }
            }

            .caixa {
                background-color: #f0f8ff;
                padding: 20px;
                border-radius: 12px;
                margin-bottom: 20px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                transition: transform 0.3s ease, background 0.3s ease;
            }

            .caixa:hover {
                transform: scale(1.02);
                background-color: #e6f7ff;
            }

            hr.animado {
                height: 4px;
                border: none;
                background: linear-gradient(to right, #00dfd8, #007cf0);
                animation: desliza 3s infinite linear;
                background-size: 200% auto;
            }

            @keyframes desliza {
                0% { background-position: 0% }
                100% { background-position: 200% }
            }
        </style>

        <div class="brilho">Sobre o Projeto</div>
        <br>

        <div class="caixa">
            <h4>Origem da Base de Dados</h4>
            <p>
                O conjunto de dados utilizado foi obtido no <b>Kaggle</b>:
                <a href="https://www.kaggle.com/datasets/jahnavipaliwal/video-game-reviews-and-ratings" target="_blank">
                    Video Game Reviews and Ratings
                </a>.
            </p>
            <p>
                A base inclui informações como: nome do jogo, plataforma, gênero, notas dos usuários, resenhas, duração média, faixa etária recomendada, preços e qualidades percebidas (gráfico, trilha sonora e história).
            </p>
        </div>

        <hr class="animado">

        <div class="caixa">
            <h4>Objetivos do Projeto</h4>
            <ul>
                <li>Explorar interativamente os jogos da base com filtros por gênero e plataforma</li>
                <li>Exibir estatísticas visuais e comparativas sobre avaliações, tipos de jogos e preferências</li>
                <li>Realizar análise textual das resenhas dos usuários (nuvem de palavras, sentimentos)</li>
                <li>Construir um modelo preditivo capaz de estimar se um jogo possui modo multiplayer</li>
            </ul>
        </div>

        <hr class="animado">

        <div class="caixa">
            <h4>Pré-processamento para Machine Learning</h4>
            <p>O modelo de machine learning desenvolvido teve como base diversas etapas de tratamento de dados, incluindo:</p>
            <ul>
                <li>Criação de novas variáveis, como tempo de jogo categorizado e faixa de preço</li>
                <li>Padronização de variáveis numéricas como nota do usuário, preço e duração</li>
                <li>Codificação de variáveis categóricas com One-Hot Encoding</li>
                <li>Mapeamento ordinal de variáveis de qualidade percebida (1 a 5)</li>
            </ul>
            <p>Após o pré-processamento, foi construído um modelo com <b>Random Forest</b> para prever a presença de modo multiplayer com base em variáveis como gênero, plataforma e preço.</p>
        </div>

        <hr class="animado">

        <div class="caixa">
            <h4>Tecnologias Utilizadas</h4>
            <ul>
                <li><b>Streamlit</b> – Interface web interativa</li>
                <li><b>Pandas</b> – Manipulação e limpeza de dados</li>
                <li><b>Plotly</b> – Visualização de gráficos interativos</li>
                <li><b>Matplotlib / Seaborn</b> – Gráficos estáticos e estatísticos</li>
                <li><b>Scikit-learn</b> – Construção do modelo preditivo</li>
                <li><b>WordCloud</b> – Nuvem de palavras das resenhas</li>
                <li><i>TextBlob / VADER</i> – Análise de sentimentos (opcional)</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    # Pac-Man animado
    components.html('''<div id="pacman-canvas-container">
      <canvas id="pacmanCanvas" width="300" height="300"></canvas>
    </div>
    <style>
      #pacman-canvas-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 300px;
        height: 300px;
        z-index: 1;
        background: black;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(255,255,0,0.4);
      }
      canvas {
        display: block;
      }
    </style>
    <script>
    const canvas = document.getElementById("pacmanCanvas");
    const ctx = canvas.getContext("2d");
    const pacman = {x: 30, y: 30, radius: 15, speed: 2, dirX: 1, dirY: 1, steps: 0};
    const ghosts = [
      { x: 250, y: 50, color: "red", dirX: -1, dirY: 0 },
      { x: 50, y: 250, color: "cyan", dirX: 1, dirY: -1 },
      { x: 250, y: 250, color: "pink", dirX: -1, dirY: -1 },
      { x: 50, y: 50, color: "orange", dirX: 0, dirY: 1 }
    ];
    let dots = [];
    for (let i = 20; i < 280; i += 40) {
      for (let j = 20; j < 280; j += 40) {
        dots.push({ x: i, y: j, eaten: false });
      }
    }
    function drawPacman() {
      const angle = 0.3;
      ctx.beginPath();
      const angleOpen = Math.PI * angle;
      const direction = Math.atan2(pacman.dirY, pacman.dirX);
      ctx.moveTo(pacman.x, pacman.y);
      ctx.arc(pacman.x, pacman.y, pacman.radius, direction + angleOpen, direction - angleOpen, false);
      ctx.closePath();
      ctx.fillStyle = "yellow";
      ctx.fill();
    }
    function drawGhost(g) {
      const x = g.x; const y = g.y; const r = 14; const footCount = 4;
      const footWidth = r / footCount;
      ctx.beginPath();
      ctx.arc(x, y, r, Math.PI, 0, false);
      ctx.lineTo(x + r, y + r);
      for (let i = 0; i < footCount; i++) {
        ctx.arc(x + r - (i * footWidth * 2 + footWidth / 2), y + r, footWidth / 2, 0, Math.PI, true);
      }
      ctx.lineTo(x - r, y + r); ctx.closePath(); ctx.fillStyle = g.color; ctx.fill();
      ctx.beginPath(); ctx.fillStyle = "white";
      ctx.arc(x - 5, y - 5, 4, 0, 2 * Math.PI); ctx.arc(x + 5, y - 5, 4, 0, 2 * Math.PI); ctx.fill();
      ctx.beginPath(); ctx.fillStyle = "blue";
      ctx.arc(x - 5, y - 5, 2, 0, 2 * Math.PI); ctx.arc(x + 5, y - 5, 2, 0, 2 * Math.PI); ctx.fill();
    }
    function drawDots() {
      ctx.fillStyle = "white";
      for (let d of dots) {
        if (!d.eaten) {
          ctx.beginPath();
          ctx.arc(d.x, d.y, 3, 0, 2 * Math.PI);
          ctx.fill();
        }
      }
    }
    function updatePacman() {
      pacman.x += pacman.speed * pacman.dirX;
      pacman.y += pacman.speed * pacman.dirY;
      pacman.steps++;
      if (pacman.steps % 60 === 0) {
        const dirs = [{ dx: 1, dy: 0 }, { dx: -1, dy: 0 }, { dx: 0, dy: 1 }, { dx: 0, dy: -1 }];
        const d = dirs[Math.floor(Math.random() * dirs.length)];
        pacman.dirX = d.dx; pacman.dirY = d.dy;
      }
      if (pacman.x > canvas.width - pacman.radius || pacman.x < pacman.radius)
        pacman.dirX *= -1;
      if (pacman.y > canvas.height - pacman.radius || pacman.y < pacman.radius)
        pacman.dirY *= -1;
      for (let d of dots) {
        const dx = pacman.x - d.x; const dy = pacman.y - d.y;
        if (!d.eaten && Math.sqrt(dx * dx + dy * dy) < pacman.radius) {
          d.eaten = true;
        }
      }
    }
    function updateGhosts() {
      for (let g of ghosts) {
        g.x += g.dirX * 1.5;
        g.y += g.dirY * 1.5;
        if (g.x < 10 || g.x > 290) g.dirX *= -1;
        if (g.y < 10 || g.y > 290) g.dirY *= -1;
      }
    }
    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      drawDots(); drawPacman(); ghosts.forEach(drawGhost);
      updatePacman(); updateGhosts();
      requestAnimationFrame(animate);
    }
    animate();
    </script>''', height=360)

    # ======== 7. Assinatura ========
    st.markdown("---")
    st.caption("Desenvolvido por Maiara • Projeto de Análise de Reviews de Jogos com Streamlit")
