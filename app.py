import streamlit as st
from docxtpl import DocxTemplate
from io import BytesIO

# Importando os módulos que criamos
from modulos import analista
from modulos import cabecalho
from modulos import prazo
from modulos import financeiro
from modulos import quantitativo
from modulos import conclusao

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Gerador de Parecer - Aditivos", 
    page_icon="⚖️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS (Design Moderno, Centralizado e Sem Bordas Duplas) ---
st.markdown("""
<style>
    /* 1. FUNDO GERAL */
    [data-testid="stApp"] { 
        background-image: linear-gradient(rgb(2, 45, 44) 0%, rgb(0, 15, 15) 100%); 
        background-attachment: fixed; 
    }
    
    /* 2. SIDEBAR */
    [data-testid="stSidebar"] { 
        background-color: rgba(2, 45, 44, 0.7) !important; 
        backdrop-filter: blur(10px);
        border: none !important; 
    }

    /* 3. FORÇAR LARGURA 75% E CENTRALIZAR (Fim do visual esticado) */
    .main .block-container, [data-testid="block-container"] {
        max-width: 75% !important; 
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
    }
    
    /* LIMPEZA GERAL */
    .stDeployButton {display:none;} 
    #MainMenu {visibility: hidden;} 
    [data-testid="stHeader"] { background-color: transparent; }
    
    /* MATAR TODAS AS LINHAS DIVISÓRIAS (<hr>) DO STREAMLIT */
    hr {
        border: none !important;
        background-color: transparent !important;
        height: 0px !important;
        margin: 0px !important;
    }
    
    /* 4. TEXTOS E TÍTULOS (Tamanho ajustado) */
    .stMarkdown, .stText, p, label, span, div[data-testid="stCaptionContainer"], li { 
        color: #e8e8e8 !important; 
        font-size: 1.15rem !important; 
    }
    /* Garantindo que o Título Principal fique BEM grande */
    h1 { font-size: 3rem !important; font-weight: bold !important; color: #ffffff !important; }
    h2 { font-size: 2.2rem !important; }
    h3 { font-size: 1.8rem !important; }
    
    /* 5. CORREÇÃO DA BORDA DUPLA NOS INPUTS E TEXTAREAS */
    /* Deixa as caixas externas do Streamlit 100% transparentes */
    div[data-baseweb="base-input"], 
    div[data-baseweb="input"], 
    div[data-baseweb="textarea"],
    div[data-baseweb="textarea"] > div {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Pinta apenas a tag nativa de texto do HTML, matando o bug da borda quadrada */
    input[type="text"], input[type="number"], textarea {
        background-color: rgba(0, 0, 0, 0.4) !important;
        color: #ffffff !important;
        border-radius: 1.5rem !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important; /* Borda quase invisível só pra dar forma */
        padding: 0.8rem 1.5rem !important;
        font-size: 1.15rem !important;
        outline: none !important;
        width: 100% !important;
        box-shadow: none !important;
    }
    
    /* Textarea com borda levemente menor por causa da barra de rolagem */
    textarea {
        border-radius: 1rem !important; 
        padding-top: 1rem !important;
    }

    input:focus, textarea:focus {
        background-color: rgba(0, 0, 0, 0.6) !important;
        border: 1px solid rgb(0, 150, 151) !important;
    }

    /* Correção do Select Box (Dropdown) */
    div[data-baseweb="select"] > div { 
        background-color: rgba(0, 0, 0, 0.4) !important; 
        border-radius: 1.5rem !important; 
        border: none !important;
        padding: 0.2rem 1rem !important;
    }
    div[data-baseweb="select"] div { color: #e0e0e0 !important; font-size: 1.15rem !important; }

    /* 6. ESTILIZAÇÃO DAS ABAS (TABS) */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        border-bottom: none !important; 
        gap: 0.5rem; 
    }
    div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
        display: none !important; 
    }
    div[data-testid="stTabs"] button {
        background-color: rgba(0, 0, 0, 0.3) !important;
        border: none !important; 
        border-radius: 2rem !important; 
        margin-right: 0.5rem;
        padding: 0.6rem 1.5rem !important;
        font-size: 1.15rem !important;
        transition: background-color 0.3s ease;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        background-color: rgb(0, 150, 151) !important;
        color: white !important;
        font-weight: bold;
    }

    /* 7. BOTÕES GERAIS */
    div[data-testid="stButton"] > button { 
        background-color: rgb(0, 80, 81) !important; 
        color: #FFFFFF !important; 
        border-radius: 2rem !important; 
        border: none !important; 
        font-weight: bold; 
        padding: 1rem 2rem !important; 
        font-size: 1.2rem !important;
        transition: all 0.2s ease-in-out;
    }
    div[data-testid="stButton"] > button:hover { 
        transform: translateY(-2px); 
        box-shadow: 0 6px 15px rgba(0, 150, 151, 0.5); 
    }
    
    div[data-testid="stDownloadButton"] > button { 
        background-image: linear-gradient(90deg, rgb(221, 79, 5) 0%, rgb(255, 110, 30) 100%) !important; 
        color: #FFFFFF !important; 
        border-radius: 2rem !important; 
        border: none !important; 
        font-weight: bold;
        padding: 1rem 2rem !important;
        font-size: 1.2rem !important;
        box-shadow: 0 4px 10px rgba(221, 79, 5, 0.3);
    }
    div[data-testid="stDownloadButton"] > button:hover {
        transform: translateY(-2px); 
        box-shadow: 0 6px 15px rgba(221, 79, 5, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# --- DICIONÁRIO DE DADOS (Estado Global) ---
dados = {}

# --- SIDEBAR (Configuração do Aditivo) ---
with st.sidebar:
    st.title("⚙️ Configuração")
    st.markdown("Selecione os escopos do aditivo para montar as seções do parecer:")
    
    st.write("") 
    dados['is_renovacao'] = st.checkbox("⏳ Renovação (Prazo)", value=True)
    dados['is_prorrogacao'] = st.checkbox("📅 Prorrogação (Extensão)", value=False)
    dados['is_reajuste'] = st.checkbox("📈 Reajuste (Índice)", value=False)
    dados['is_repactuacao'] = st.checkbox("👷 Repactuação (CCT)", value=False)
    dados['is_quantitativo'] = st.checkbox("🔢 Alteração Quantitativa", value=False)
    
    st.write("") 
    
    # Chama o módulo do Analista
    analista.render_analista_sidebar(dados)

# --- CABEÇALHO (Dados do Contrato) ---
st.title("⚖️ Gerador de Parecer Técnico")
st.markdown("Preencha as informações abaixo para estruturar a minuta do parecer.")
st.write("") 
cabecalho.render_cabecalho(dados)
st.write("") 

# --- ABAS DINÂMICAS ---
lista_abas = []
if dados['is_renovacao'] or dados['is_prorrogacao']: lista_abas.append("⏳ Prazo")
if dados['is_reajuste']: lista_abas.append("📈 Reajuste")
if dados['is_repactuacao']: lista_abas.append("👷 Repactuação")
if dados['is_quantitativo']: lista_abas.append("🔢 Alt. Quantitativa")
lista_abas.append("✅ Conclusão")

if lista_abas:
    tabs = st.tabs(lista_abas)
    tab_map = dict(zip(lista_abas, tabs))

    if "⏳ Prazo" in tab_map:
        with tab_map["⏳ Prazo"]:
            st.write("") 
            prazo.render_prazo(dados)

    if "📈 Reajuste" in tab_map:
        with tab_map["📈 Reajuste"]:
            st.write("")
            financeiro.render_reajuste(dados)

    if "👷 Repactuação" in tab_map:
        with tab_map["👷 Repactuação"]:
            st.write("")
            financeiro.render_repactuacao(dados)

    if "🔢 Alt. Quantitativa" in tab_map:
        with tab_map["🔢 Alt. Quantitativa"]:
            st.write("")
            quantitativo.render_quantitativo(dados)

    with tab_map["✅ Conclusão"]:
        st.write("")
        conclusao.render_conclusao(dados)
else:
    st.info("👈 Selecione ao menos um escopo de aditivo na barra lateral para começar.")

# --- GERAÇÃO DO ARQUIVO ---
st.write("")
st.write("")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Gerar Documento do Parecer", use_container_width=True):
        try:
