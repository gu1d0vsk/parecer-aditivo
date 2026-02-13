import streamlit as st
from docxtpl import DocxTemplate
from io import BytesIO

# Importando os módulos que criamos
import modulos/analista
import modulos/cabecalho
import modulos/prazo
import modulos/financeiro
import modulos/quantitativo
import modulos/conclusao

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gerador de Parecer - Aditivos", page_icon="⚖️", layout="wide")

# --- CSS (Identity Visual) ---
st.markdown("""
<style>
    /* 1. FUNDO GERAL */
    [data-testid="stApp"] { background-image: linear-gradient(rgb(2, 45, 44) 0%, rgb(0, 21, 21) 100%); background-attachment: fixed; }
    
    /* 2. SIDEBAR */
    [data-testid="stSidebar"] { background-color: rgba(2, 45, 44, 0.95); border-right: 1px solid rgba(255, 255, 255, 0.1); }

    /* 3. LIMPEZA */
    header {visibility: hidden;} .stDeployButton {display:none;} [data-testid="stStatusWidget"] {display:none;}
    
    /* 4. TEXTOS */
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, label, span, div[data-testid="stCaptionContainer"] { color: #e0e0e0 !important; }
    
    /* 5. INPUTS TRANSPARENTES */
    div[data-baseweb="input"], div[data-baseweb="base-input"], div[data-baseweb="select"] > div { background-color: transparent !important; border: none !important; }
    div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input, div[data-testid="stTextArea"] textarea, div[data-baseweb="select"] > div > div { 
        background-color: rgba(12, 19, 14, 0.5) !important; color: #e0e0e0 !important; border-radius: 1.5rem !important; border: 1px solid rgba(255, 255, 255, 0.2) !important; padding-left: 1rem !important;
    }
    div[data-baseweb="select"] div { color: #e0e0e0 !important; }

    /* 6. BOTÕES */
    div[data-testid="stButton"] > button { background-color: rgb(0, 80, 81) !important; color: #FFFFFF !important; border-radius: 4rem; border: none; font-weight: bold; }
    div[data-testid="stButton"] > button:hover { transform: scale(1.02); box-shadow: 0 0 12px rgba(0, 80, 81, 0.8); }
    div[data-testid="stDownloadButton"] > button { background-color: rgb(221, 79, 5) !important; color: #FFFFFF !important; border-radius: 4rem; border: none; }
</style>
""", unsafe_allow_html=True)

# --- DICIONÁRIO DE DADOS (Estado Global) ---
dados = {}

# --- SIDEBAR (Configuração do Aditivo) ---
with st.sidebar:
    st.title("⚖️ Configuração")
    st.caption("SELECIONE AS PARTES DO PARECER")
    
    # Flags de controle de fluxo
    dados['is_renovacao'] = st.checkbox("Renovação (Prazo)", value=True)
    dados['is_prorrogacao'] = st.checkbox("Prorrogação (Extensão)", value=False)
    dados['is_reajuste'] = st.checkbox("Reajuste (Índice)", value=False)
    dados['is_repactuacao'] = st.checkbox("Repactuação (CCT)", value=False)
    dados['is_quantitativo'] = st.checkbox("Alteração Quantitativa", value=False)
    
    # Chama o módulo do Analista
    analista.render_analista_sidebar(dados)

# --- CABEÇALHO (Dados do Contrato) ---
st.title("Gerador de Parecer Técnico")
cabecalho.render_cabecalho(dados)

# --- ABAS DINÂMICAS ---
# Monta a lista de abas necessárias baseado nos checkboxes
lista_abas = []
if dados['is_renovacao'] or dados['is_prorrogacao']: lista_abas.append("⏳ Prazo")
if dados['is_reajuste']: lista_abas.append("📈 Reajuste")
if dados['is_repactuacao']: lista_abas.append("👷 Repactuação")
if dados['is_quantitativo']: lista_abas.append("🔢 Alt. Quantitativa")
lista_abas.append("✅ Conclusão")

# Cria as abas no Streamlit
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

# --- GERAÇÃO DO ARQUIVO ---
st.divider()

if st.button("🚀 Gerar Parecer (.docx)", use_container_width=True):
    try:
        # Carrega o modelo
        doc = DocxTemplate("modelo_parecer.docx")
        
        # Renderiza
        doc.render(dados)
        
        # Salva em memória
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        st.success("Parecer gerado com sucesso!")
        st.download_button(
            label="📥 Baixar Parecer",
            data=buffer,
            file_name=f"Parecer_{dados.get('num_contrato', 'S/N')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Erro ao gerar documento: {e}")
        st.warning("Verifique se o arquivo 'modelo_parecer.docx' está na mesma pasta.")
