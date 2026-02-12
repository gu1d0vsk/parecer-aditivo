import streamlit as st
from docxtpl import DocxTemplate
from io import BytesIO
from datetime import date

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gerador de Parecer - Aditivos", page_icon="⚖️", layout="wide")

# --- ESTILIZAÇÃO CSS (IDENTIDADE DARK NEON) ---
page_bg_img = """
<style>
    /* Fundo Geral */
    [data-testid="stApp"] {
        background-image: linear-gradient(rgb(2, 45, 44) 0%, rgb(0, 21, 21) 100%);
        background-attachment: fixed;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(2, 45, 44, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Cabeçalho e Textos */
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, label, span, div[data-testid="stCaptionContainer"] {
        color: #e0e0e0 !important;
    }
    
    /* Inputs Estilizados */
    div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input, div[data-testid="stTextArea"] textarea, div[data-testid="stSelectbox"] > div > div { 
        background-color: rgba(12, 19, 14, 0.5) !important;
        color: #e0e0e0 !important;
        border-radius: 1.5rem !important; 
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding-left: 1rem;
    }
    div[data-testid="stTextInput"] input:focus, div[data-testid="stTextArea"] textarea:focus {
        border-color: rgb(221, 79, 5) !important;
        box-shadow: 0 0 10px rgba(221, 79, 5, 0.2);
    }

    /* Botões Neon */
    div[data-testid="stButton"] > button { 
        background-color: rgb(0, 80, 81) !important; 
        color: #FFFFFF !important; 
        border-radius: 4rem; 
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }
    div[data-testid="stButton"] > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 12px rgba(0, 80, 81, 0.8);
    }
    
    /* Botão de Download (Laranja) */
    div[data-testid="stDownloadButton"] > button {
        background-color: rgb(221, 79, 5) !important; 
        color: #FFFFFF !important; 
        border-radius: 4rem;
        border: none;
        color: white !important;
    }
    
    /* Checkboxes */
    div[data-testid="stCheckbox"] label span { line-height: 1.5; }
    
    /* Limpeza */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE DADOS ---
dados = {} 

# --- SIDEBAR: O CÉREBRO DA SELEÇÃO ---
with st.sidebar:
    st.title("⚖️ Configuração do Parecer")
    st.markdown("Selecione o que está sendo analisado neste aditivo.")
    st.divider()
    
    st.caption("TIPO DE ADITIVO (Pode marcar vários)")
    
    # Checkboxes que controlam a lógica
    # Usamos st.checkbox porque pode ser Renovação + Reajuste ao mesmo tempo
    is_renovacao = st.checkbox("Renovação (Prazo Contínuo)", value=True)
    is_prorrogacao = st.checkbox("Prorrogação (Extensão de Prazo)", value=False)
    is_reajuste = st.checkbox("Reajuste (Índice / IPCA)", value=False)
    is_repactuacao = st.checkbox("Repactuação (CCT / Mão de Obra)", value=False)
    
    # Salvando flags para o Word
    dados['is_renovacao'] = is_renovacao
    dados['is_prorrogacao'] = is_prorrogacao
    dados['is_reajuste'] = is_reajuste
    dados['is_repactuacao'] = is_repactuacao
    
    st.divider()
    
    # Dados do Analista (Isso quase nunca muda, fica aqui pra facilitar)
    st.caption("DADOS DO ANALISTA")
    nome_analista = st.text_input("Seu Nome", value="Analista DCAD")
    cargo_analista = st.text_input("Seu Cargo", value="Analista")
    matricula = st.text_input("Matrícula", value="XXXX")
    
    dados['nome_analista'] = nome_analista
    dados['cargo_analista'] = cargo_analista
    dados['matricula'] = matricula

# --- CABEÇALHO DA PÁGINA ---
st.title("Gerador de Parecer Técnico")
st.markdown("Preencha os dados abaixo. As abas mudam conforme sua seleção na lateral.")
st.divider()

# --- BLOCO 1: CABEÇALHO DO DOCUMENTO (MEMO) ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        dados['num_contrato'] = st.text_input("Número do Contrato", placeholder="Ex: 20.23.0123.00")
        dados['fornecedor'] = st.text_input("Nome do Fornecedor")
    with col2:
        dados['objeto_resumido'] = st.text_input("Objeto Resumido", placeholder="Ex: Serviços de Limpeza")
        dados['num_processo'] = st.text_input("Número do Processo/Requisição")

# --- BLOCO 2: ABAS DINÂMICAS ---
# Criamos as abas baseadas no que foi marcado
abas = ["📋 Dados Gerais"]

if is_renovacao or is_prorrogacao:
    abas.append("⏳ Prazo (Renov/Prorrog)")
if is_reajuste:
    abas.append("📈 Reajuste (Índice)")
if is_repactuacao:
    abas.append("👷 Repactuação (CCT)")

abas.append("✅ Conclusão")

tabs = st.tabs(abas)
tab_map = dict(zip(abas, tabs))

# --- CONTEÚDO DAS ABAS ---

# ABA 1: DADOS GERAIS
with tab_map["📋 Dados Gerais"]:
    st.subheader("Informações Iniciais")
    col_a, col_b = st.columns(2)
    dados['gerente_dcad'] = col_a.text_input("Gerente DCAD (Destinatário)", value="Felipe Mazza Mascarenhas")
    dados['data_hoje'] = date.today().strftime("%d/%m/%Y")
    
    st.info("💡 Dica: O texto introdutório do parecer será gerado automaticamente com base nessas informações.")

# ABA 2: PRAZO (Se houver Renovação ou Prorrogação)
if "⏳ Prazo (Renov/Prorrog)" in tab_map:
    with tab_map["⏳ Prazo (Renov/Prorrog)"]:
        st.subheader("Justificativa de Prazo")
        
        if is_renovacao:
            st.markdown("### Detalhes da Renovação")
            col_r1, col_r2 = st.columns(2)
            meses_renov = col_r1.number_input("Renovar por quantos meses?", value=12)
            dados['periodo_renovacao'] = f"{meses_renov} meses"
            
            dados['vantajosidade_texto'] = st.text_area("Justificativa da Vantajosidade", 
                value="A renovação é vantajosa pois os preços permanecem compatíveis com o mercado e o serviço vem sendo prestado a contento.", height=100)
                
        if is_prorrogacao:
            st.markdown("### Detalhes da Prorrogação")
            dados['motivo_prorrogacao'] = st.text_area("Motivo da Prorrogação", placeholder="Ex: Atraso na entrega devido a greve na fábrica...")

# ABA 3: REAJUSTE (Se houver)
if "📈 Reajuste (Índice)" in tab_map:
    with tab_map["📈 Reajuste (Índice)"]:
        st.subheader("Cálculo de Índice")
        col_ind1, col_ind2, col_ind3 = st.columns(3)
        indice_nome = col_ind1.selectbox("Índice", ["IPCA", "IGP-M", "INPC", "ICTI"])
        percentual = col_ind2.number_input("Percentual Acumulado (%)", format="%.4f")
        periodo_txt = col_ind3.text_input("Período de Apuração", placeholder="Ex: jan/23 a dez/23")
        
        dados['texto_reajuste'] = f"Foi aplicado o índice {indice_nome} acumulado de {percentual}% referente ao período de {periodo_txt}."

# ABA 4: REPACTUAÇÃO (Se houver)
if "👷 Repactuação (CCT)" in tab_map:
    with tab_map["👷 Repactuação (CCT)"]:
        st.subheader("Alteração da Convenção Coletiva")
        dados['cct_numero'] = st.text_input("Número da CCT no MTE", placeholder="Ex: RJ000123/2024")
        dados['alteracoes_cct'] = st.text_area("Resumo das Alterações Econômicas", placeholder="Houve aumento de piso salarial para R$ 1.500,00 e Vale Refeição para R$ 25,00.")

# ABA FINAL: CONCLUSÃO
with tab_map["✅ Conclusão"]:
    st.subheader("Verificações Finais")
    
    check_doc = st.checkbox("Documentação de Habilitação Regular (SICAF, CNDs)?", value=True)
    check_orc = st.checkbox("Existe dotação orçamentária?", value=True)
    
    if check_doc and check_orc:
        st.success("Parecer favorável à assinatura do Aditivo.")
        dados['conclusao_texto'] = "Diante do exposto, opinamos favoravelmente ao prosseguimento do feito e assinatura do Termo Aditivo."
    else:
        st.error("Existem pendências.")
        dados['conclusao_texto'] = "Sugerimos o saneamento das pendências apontadas antes da assinatura."

# --- GERAÇÃO DO ARQUIVO ---
st.divider()

col_vazio, col_btn, col_vazio2 = st.columns([1, 2, 1])

with col_btn:
    if st.button("🚀 Gerar Parecer (.docx)", use_container_width=True):
        try:
            # Carrega o modelo (Atenção: Você precisará editar seu DOCX para ter essas tags!)
            doc = DocxTemplate("modelo_parecer.docx") # Renomeie seu arquivo para este nome
            doc.render(dados)
            
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            
            st.success("Parecer gerado com sucesso!")
            st.download_button(
                label="📥 Baixar Parecer Editado",
                data=buffer,
                file_name=f"Parecer_{dados['num_contrato']}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Erro ao gerar: {e}")
            st.warning("Verifique se o arquivo 'modelo_parecer.docx' está na pasta e tem as tags corretas.")
