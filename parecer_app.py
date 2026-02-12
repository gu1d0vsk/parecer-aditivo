import streamlit as st
from docxtpl import DocxTemplate
from io import BytesIO
from datetime import date

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gerador de Parecer - Aditivos", page_icon="⚖️", layout="wide")

# --- ESTILIZAÇÃO CSS (DARK NEON) ---
page_bg_img = """
<style>
    [data-testid="stApp"] { background-image: linear-gradient(rgb(2, 45, 44) 0%, rgb(0, 21, 21) 100%); background-attachment: fixed; }
    [data-testid="stSidebar"] { background-color: rgba(2, 45, 44, 0.95); border-right: 1px solid rgba(255, 255, 255, 0.1); }
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, label, span, div[data-testid="stCaptionContainer"] { color: #e0e0e0 !important; }
    div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input, div[data-testid="stTextArea"] textarea, div[data-testid="stSelectbox"] > div > div { 
        background-color: rgba(12, 19, 14, 0.5) !important; color: #e0e0e0 !important; border-radius: 1.5rem !important; border: 1px solid rgba(255, 255, 255, 0.2); padding-left: 1rem;
    }
    div[data-testid="stButton"] > button { background-color: rgb(0, 80, 81) !important; color: #FFFFFF !important; border-radius: 4rem; font-weight: bold; border: none; transition: all 0.3s ease; }
    div[data-testid="stButton"] > button:hover { transform: scale(1.02); box-shadow: 0 0 12px rgba(0, 80, 81, 0.8); }
    div[data-testid="stDownloadButton"] > button { background-color: rgb(221, 79, 5) !important; color: #FFFFFF !important; border-radius: 4rem; border: none; }
    footer {visibility: hidden;} .stDeployButton {display:none;}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

dados = {} 

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚖️ Configuração")
    st.caption("TIPO DE ADITIVO")
    
    is_renovacao = st.checkbox("Renovação (Prazo)", value=False)
    is_prorrogacao = st.checkbox("Prorrogação (Extensão)", value=False)
    is_reajuste = st.checkbox("Reajuste (Índice)", value=False)
    is_repactuacao = st.checkbox("Repactuação (CCT)", value=False)
    # NOVA OPÇÃO
    is_quantitativo = st.checkbox("Alteração Quantitativa (+/- Valor)", value=True)
    
    # Flags para o Word
    dados['is_renovacao'] = is_renovacao
    dados['is_prorrogacao'] = is_prorrogacao
    dados['is_reajuste'] = is_reajuste
    dados['is_repactuacao'] = is_repactuacao
    dados['is_quantitativo'] = is_quantitativo
    
    st.divider()
    st.caption("DADOS DO ANALISTA")
    dados['nome_analista'] = st.text_input("Nome", value="Analista DCAD")
    dados['cargo_analista'] = st.text_input("Cargo", value="Analista")
    dados['matricula'] = st.text_input("Matrícula", value="XXXX")

st.title("Gerador de Parecer Técnico")
st.markdown("Preencha os dados do aditivo.")
st.divider()

# --- BLOCO 1: CABEÇALHO ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        dados['num_contrato'] = st.text_input("Número do Contrato", placeholder="Ex: 20.23.0123.00")
        dados['fornecedor'] = st.text_input("Nome do Fornecedor")
    with col2:
        dados['objeto_resumido'] = st.text_input("Objeto Resumido", placeholder="Ex: Serviços de Limpeza")
        dados['num_processo'] = st.text_input("Número do Processo")

# --- ABAS DINÂMICAS ---
abas = ["📋 Dados Gerais"]
if is_renovacao or is_prorrogacao: abas.append("⏳ Prazo")
if is_reajuste: abas.append("📈 Reajuste")
if is_repactuacao: abas.append("👷 Repactuação")
if is_quantitativo: abas.append("🔢 Alt. Quantitativa") # Nova Aba
abas.append("✅ Conclusão")

tabs = st.tabs(abas)
tab_map = dict(zip(abas, tabs))

# --- ABA 1: DADOS GERAIS ---
with tab_map["📋 Dados Gerais"]:
    dados['gerente_dcad'] = st.text_input("Gerente DCAD", value="Felipe Mazza Mascarenhas")
    dados['data_hoje'] = date.today().strftime("%d/%m/%Y")

# --- ABA: PRAZO ---
if "⏳ Prazo" in tab_map:
    with tab_map["⏳ Prazo"]:
        if is_renovacao:
            st.markdown("### Renovação")
            meses = st.number_input("Meses", value=12)
            dados['periodo_renovacao'] = f"{meses} meses"
            dados['vantajosidade_texto'] = st.text_area("Justificativa Vantajosidade", value="Preços compatíveis com mercado e serviço satisfatório.")
        if is_prorrogacao:
            st.markdown("### Prorrogação")
            dados['motivo_prorrogacao'] = st.text_area("Motivo", placeholder="Atraso justificado...")

# --- ABA: REAJUSTE ---
if "📈 Reajuste" in tab_map:
    with tab_map["📈 Reajuste"]:
        col_i1, col_i2 = st.columns(2)
        indice = col_i1.selectbox("Índice", ["IPCA", "IGP-M"])
        perc = col_i2.number_input("% Acumulado", format="%.4f")
        dados['texto_reajuste'] = f"Aplicação de {indice} acumulado de {perc}%."

# --- ABA: REPACTUAÇÃO ---
if "👷 Repactuação" in tab_map:
    with tab_map["👷 Repactuação"]:
        dados['cct_numero'] = st.text_input("Nº CCT", placeholder="RJ000123/2024")
        dados['alteracoes_cct'] = st.text_area("Alterações Econômicas")

# --- NOVA ABA: ALTERAÇÃO QUANTITATIVA ---
if "🔢 Alt. Quantitativa" in tab_map:
    with tab_map["🔢 Alt. Quantitativa"]:
        st.subheader("Cálculo de Acréscimo e Supressão")
        st.caption("Base Legal: Lei 13.303/2016, Art. 81, §1º (Limite de 25%)")
        
        col_q1, col_q2 = st.columns(2)
        valor_atual = col_q1.number_input("Valor Atualizado do Contrato (R$)", min_value=0.01, format="%.2f")
        
        col_q3, col_q4 = st.columns(2)
        acrescimo = col_q3.number_input("Valor a ACRESCER (R$)", min_value=0.0, format="%.2f")
        supressao = col_q4.number_input("Valor a SUPRIMIR (R$)", min_value=0.0, format="%.2f")
        
        # Cálculos Automáticos
        if valor_atual > 0:
            perc_acrescimo = (acrescimo / valor_atual) * 100
            perc_supressao = (supressao / valor_atual) * 100
            novo_valor = valor_atual + acrescimo - supressao
            
            # Exibição Visual (Metrics)
            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("Novo Valor Global", f"R$ {novo_valor:,.2f}")
            col_m2.metric("% Acréscimo", f"{perc_acrescimo:.2f}%", delta_color="inverse" if perc_acrescimo > 25 else "normal")
            col_m3.metric("% Supressão", f"{perc_supressao:.2f}%")
            
            # Validação Legal (Limite de 25%)
            if perc_acrescimo > 25:
                st.error(f"🚨 ATENÇÃO: O acréscimo de {perc_acrescimo:.2f}% extrapola o limite legal de 25% (Lei 13.303/16)!")
                aviso_legal = "O acréscimo extrapola o limite legal de 25%, exigindo justificativa excepcionalíssima."
            else:
                st.success("✅ Percentuais dentro do limite legal (Art. 81, Lei 13.303).")
                aviso_legal = "A alteração respeita o limite legal de 25% do valor inicial atualizado."

            # Texto Gerado Automaticamente
            texto_quant = (f"O presente aditivo tem por objeto a alteração quantitativa do contrato. "
                           f"O valor inicial atualizado base é de R$ {valor_atual:,.2f}. "
                           f"Será realizado um acréscimo de R$ {acrescimo:,.2f} ({perc_acrescimo:.2f}%) "
                           f"e uma supressão de R$ {supressao:,.2f} ({perc_supressao:.2f}%). "
                           f"O novo valor global do contrato passa a ser R$ {novo_valor:,.2f}. "
                           f"{aviso_legal}")
            
            dados['texto_quantitativo'] = texto_quant
            
            with st.expander("Ver texto gerado para o Parecer"):
                st.write(texto_quant)

# --- ABA: CONCLUSÃO ---
with tab_map["✅ Conclusão"]:
    st.subheader("Parecer Final")
    check_doc = st.checkbox("Habilitação Regular?", value=True)
    check_orc = st.checkbox("Dotação Orçamentária?", value=True)
    
    if check_doc and check_orc:
        st.success("Parecer Favorável.")
    else:
        st.warning("Pendências identificadas.")

# --- BOTÃO DE DOWNLOAD ---
st.divider()
if st.button("🚀 Gerar Parecer (.docx)", use_container_width=True):
    try:
        doc = DocxTemplate("modelo_parecer.docx")
        doc.render(dados)
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        st.download_button("📥 Baixar Parecer", data=buffer, file_name=f"Parecer_{dados['num_contrato']}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    except Exception as e:
        st.error(f"Erro: {e}")
