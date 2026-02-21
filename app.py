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

# --- CSS (Identidade Visual Melhorada) ---
st.markdown("""
<style>
    /* 1. FUNDO GERAL */
    [data-testid="stApp"] { 
        background-image: linear-gradient(rgb(2, 45, 44) 0%, rgb(0, 15, 15) 100%); 
        background-attachment: fixed; 
    }
    
    /* 2. SIDEBAR */
    [data-testid="stSidebar"] { 
        background-color: rgba(2, 45, 44, 0.7); 
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.05); 
    }

    /* 3. LIMPEZA E CORREÇÃO DA SIDEBAR */
    /* Esconde apenas o botão de deploy e o menu superior, mas mantém o controle da sidebar */
    .stDeployButton {display:none;} 
    #MainMenu {visibility: hidden;} 
    [data-testid="stHeader"] { background-color: transparent; }
    
    /* 4. TEXTOS */
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, label, span, div[data-testid="stCaptionContainer"] { 
        color: #e8e8e8 !important; 
    }
    
    /* 5. INPUTS COM EFEITO NEUMORPHISM SUAVE */
    div[data-baseweb="input"], div[data-baseweb="base-input"], div[data-baseweb="select"] > div { 
        background-color: transparent !important; 
        border: none !important; 
    }
    div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input, div[data-testid="stTextArea"] textarea, div[data-baseweb="select"] > div > div { 
        background-color: rgba(0, 0, 0, 0.2) !important; 
        color: #ffffff !important; 
        border-radius: 0.8rem !important; 
        border: 1px solid rgba(255, 255, 255, 0.1) !important; 
        padding-left: 1rem !important;
        transition: border 0.3s ease;
    }
    div[data-testid="stTextInput"] input:focus, div[data-testid="stNumberInput"] input:focus {
        border: 1px solid rgb(0, 150, 151) !important;
    }
    div[data-baseweb="select"] div { color: #e0e0e0 !important; }

    /* 6. ESTILIZAÇÃO DAS ABAS (TABS) */
    div[data-testid="stTabs"] button {
        background-color: transparent;
        border: none;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 0.5rem;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        border-bottom: 2px solid rgb(0, 150, 151);
        color: white !important;
        font-weight: bold;
    }

    /* 7. BOTÕES */
    div[data-testid="stButton"] > button { 
        background-color: rgb(0, 80, 81) !important; 
        color: #FFFFFF !important; 
        border-radius: 0.8rem; 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        font-weight: bold; 
        padding: 0.5rem 1rem;
        transition: all 0.2s ease-in-out;
    }
    div[data-testid="stButton"] > button:hover { 
        transform: translateY(-2px); 
        box-shadow: 0 4px 12px rgba(0, 150, 151, 0.4); 
        border-color: rgb(0, 150, 151);
    }
    
    div[data-testid="stDownloadButton"] > button { 
        background-image: linear-gradient(90deg, rgb(221, 79, 5) 0%, rgb(255, 110, 30) 100%) !important; 
        color: #FFFFFF !important; 
        border-radius: 0.8rem; 
        border: none; 
        font-weight: bold;
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
    st.divider()
    
    # Flags de controle de fluxo
    dados['is_renovacao'] = st.checkbox("⏳ Renovação (Prazo)", value=True)
    dados['is_prorrogacao'] = st.checkbox("📅 Prorrogação (Extensão)", value=False)
    dados['is_reajuste'] = st.checkbox("📈 Reajuste (Índice)", value=False)
    dados['is_repactuacao'] = st.checkbox("👷 Repactuação (CCT)", value=False)
    dados['is_quantitativo'] = st.checkbox("🔢 Alteração Quantitativa", value=False)
    
    st.divider()
    # Chama o módulo do Analista
    analista.render_analista_sidebar(dados)

# --- CABEÇALHO (Dados do Contrato) ---
st.title("⚖️ Gerador de Parecer Técnico")
st.markdown("Preencha as informações abaixo para estruturar a minuta do parecer.")
cabecalho.render_cabecalho(dados)

# --- ABAS DINÂMICAS ---
# Monta a lista de abas necessárias baseado nos checkboxes
lista_abas = []
if dados['is_renovacao'] or dados['is_prorrogacao']: lista_abas.append("⏳ Prazo")
if dados['is_reajuste']: lista_abas.append("📈 Reajuste")
if dados['is_repactuacao']: lista_abas.append("👷 Repactuação")
if dados['is_quantitativo']: lista_abas.append("🔢 Alt. Quantitativa")
lista_abas.append("✅ Conclusão")

# Cria as abas no Streamlit apenas se houver abas para mostrar
if lista_abas:
    tabs = st.tabs(lista_abas)
    tab_map = dict(zip(lista_abas, tabs))

    # --- RENDERIZAÇÃO DOS MÓDULOS NAS ABAS ---
    if "⏳ Prazo" in tab_map:
        with tab_map["⏳ Prazo"]:
            prazo.render_prazo(dados)

    if "📈 Reajuste" in tab_map:
        with tab_map["📈 Reajuste"]:
            financeiro.render_reajuste(dados)

    if "👷 Repactuação" in tab_map:
        with tab_map["👷 Repactuação"]:
            financeiro.render_repactuacao(dados)

    if "🔢 Alt. Quantitativa" in tab_map:
        with tab_map["🔢 Alt. Quantitativa"]:
            quantitativo.render_quantitativo(dados)

    with tab_map["✅ Conclusão"]:
        conclusao.render_conclusao(dados)
else:
    st.info("👈 Selecione ao menos um escopo de aditivo na barra lateral para começar.")

# --- GERAÇÃO DO ARQUIVO ---
st.divider()

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Gerar Documento do Parecer", use_container_width=True):
        try:
            # Carrega o modelo
            doc = DocxTemplate("modelo_parecer.docx")
            
            # Renderiza
            doc.render(dados)
            
            # Salva em memória
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
