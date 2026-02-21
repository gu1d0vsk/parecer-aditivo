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

# --- CSS (Design Moderno, Títulos Corrigidos e Sem Bordas Duplas) ---
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

    /* 3. LARGURA DA PÁGINA (Limita a 75% e centraliza) */
    .main .block-container, [data-testid="block-container"] {
        max-width: 75% !important; 
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
    }
    
    /* LIMPEZA GERAL */
    .stDeployButton {display:none;} 
    #MainMenu {visibility: hidden;} 
    [data-testid="stHeader"] { background-color: transparent; }
    hr {
        border: none !important;
        background-color: transparent !important;
        height: 0px !important;
        margin: 0px !important;
    }
    
    /* 4. TEXTOS BASE E TÍTULOS (Correção do bug do Span) */
    /* Aplica fonte 1.15 só em textos comuns, não em spans gerais para não quebrar títulos */
    p, label, div[data-testid="stCaptionContainer"], li { 
        color: #e8e8e8 !important; 
        font-size: 1.15rem !important; 
    }
    
    /* Títulos da Área Principal (Gigantes e Imponentes) */
    .main h1, .main h1 span { 
        font-size: 3rem !important; 
        font-weight: bold !important; 
        color: #ffffff !important; 
    }
    .main h2, .main h2 span { font-size: 2.2rem !important; }
    .main h3, .main h3 span { font-size: 1.8rem !important; }
    
    /* Título da Sidebar (Menor para caber "Configuração" numa linha só) */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h1 span {
        font-size: 2rem !important;
    }
    
    /* 5. CORREÇÃO DEFINITIVA DAS BORDAS DUPLAS NOS INPUTS */
    /* Deixa TODAS as caixas pai (wrappers) invisíveis */
    div[data-testid="stTextInput"] div,
    div[data-testid="stNumberInput"] div,
    div[data-testid="stTextArea"] div,
    div[data-baseweb="select"] div {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Aplica a cor e borda APENAS onde você de fato digita ou seleciona */
    input[type="text"], input[type="number"], textarea, div[data-baseweb="select"] > div {
        background-color: rgba(0, 0, 0, 0.4) !important;
        color: #ffffff !important;
        border-radius: 1.5rem !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important; 
        padding: 0.8rem 1.5rem !important;
        font-size: 1.15rem !important;
        outline: none !important;
        width: 100% !important;
    }
    
    /* Ajuste fino para a caixa grande (Textarea) e Select */
    textarea {
        border-radius: 1rem !important; 
        padding-top: 1rem !important;
    }
    div[data-baseweb="select"] div { 
        color: #ffffff !important; 
    }

    /* Efeito de Foco (Ao clicar no input) */
    input:focus, textarea:focus {
        background-color: rgba(0, 0, 0, 0.6) !important;
        border: 1px solid rgb(0, 150, 151) !important;
    }

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
            doc = DocxTemplate("modelo_parecer.docx")
            doc.render(dados)
            
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            
            st.success("✨ Parecer estruturado com sucesso!")
            st.download_button(
                label="📥 Baixar Parecer (.docx)",
                data=buffer,
                file_name=f"Parecer_{dados.get('num_contrato', 'S/N')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Erro ao gerar documento: {e}")
            st.warning("Verifique se o arquivo 'modelo_parecer.docx' está na mesma pasta e se as tags coincidem.")
