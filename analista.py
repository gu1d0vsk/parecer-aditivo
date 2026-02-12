import streamlit as st

def render_analista_sidebar(dados):
    """Renderiza os campos de identificação do analista na Sidebar."""
    st.sidebar.divider()
    st.sidebar.caption("DADOS DO ANALISTA")
    
    dados['nome_analista'] = st.sidebar.text_input("Nome", value="Analista DCAD")
    dados['cargo_analista'] = st.sidebar.text_input("Cargo", value="Analista")
    dados['matricula'] = st.sidebar.text_input("Matrícula", value="XXXX")
