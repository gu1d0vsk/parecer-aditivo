import streamlit as st
from datetime import date

def render_cabecalho(dados):
    """Renderiza os dados principais do contrato e gerência."""
    
    # Bloco principal de identificação
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            dados['num_contrato'] = st.text_input("Número do Contrato", placeholder="Ex: 20.23.0123.00")
            dados['fornecedor'] = st.text_input("Nome do Fornecedor")
        with col2:
            dados['objeto_resumido'] = st.text_input("Objeto Resumido", placeholder="Ex: Serviços de Limpeza")
            dados['num_processo'] = st.text_input("Número do Processo")
            
    st.divider()
    
    # Dados que antes ficavam na aba "Gerais"
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        dados['gerente_dcad'] = st.text_input("Gerente DCAD (Destinatário)", value="Felipe Mazza Mascarenhas")
    with col_g2:
        # Pega data de hoje automática, mas permite edição se quiser
        dados['data_hoje'] = date.today().strftime("%d/%m/%Y")
        st.caption(f"📅 Data do Parecer: {dados['data_hoje']}")
