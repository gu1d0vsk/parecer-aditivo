import streamlit as st

def render_reajuste(dados):
    """Renderiza conteúdo da aba Reajuste."""
    st.subheader("Cálculo de Reajuste (Índice)")
    col_i1, col_i2 = st.columns(2)
    
    indice = col_i1.selectbox("Índice Aplicado", ["IPCA", "IGP-M", "INPC", "ICTI", "Outro"])
    perc = col_i2.number_input("Percentual Acumulado (%)", format="%.4f")
    periodo = st.text_input("Período de Apuração", placeholder="Ex: jan/2023 a dez/2023")
    
    dados['texto_reajuste'] = f"Foi aplicado o índice {indice} acumulado de {perc}% referente ao período de {periodo}."

def render_repactuacao(dados):
    """Renderiza conteúdo da aba Repactuação."""
    st.subheader("Repactuação (Mão de Obra)")
    
    dados['cct_numero'] = st.text_input("Número da CCT / Registro MTE", placeholder="Ex: RJ000123/2024")
    
    col_r1, col_r2 = st.columns(2)
    piso_antigo = col_r1.number_input("Piso Salarial Anterior (R$)", format="%.2f")
    piso_novo = col_r2.number_input("Piso Salarial Novo (R$)", format="%.2f")
    
    dados['alteracoes_cct'] = st.text_area(
        "Resumo das Alterações Econômicas",
        value=f"Houve alteração do piso salarial da categoria de R$ {piso_antigo:,.2f} para R$ {piso_novo:,.2f}, além de reajuste nos benefícios de Vale Alimentação."
    )
