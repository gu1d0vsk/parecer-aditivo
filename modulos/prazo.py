import streamlit as st

def render_prazo(dados):
    """Renderiza o conteúdo da aba de Prazo (Renovação/Prorrogação)."""
    
    if dados.get('is_renovacao'):
        st.markdown("### 🔄 Renovação Contratual")
        col_r1, col_r2 = st.columns([1, 3])
        
        meses = col_r1.number_input("Renovar por (meses)", value=12, min_value=1)
        dados['periodo_renovacao'] = f"{meses} meses"
        
        dados['vantajosidade_texto'] = col_r2.text_area(
            "Justificativa da Vantajosidade", 
            value="A renovação é vantajosa pois os preços permanecem compatíveis com o mercado e o serviço vem sendo prestado a contento, conforme ateste da fiscalização.",
            height=100
        )
        st.divider()

    if dados.get('is_prorrogacao'):
        st.markdown("### ⏳ Prorrogação de Vigência")
        st.info("Utilizado para extensão de prazo para conclusão de etapas (sem renovação do escopo global).")
        dados['motivo_prorrogacao'] = st.text_area(
            "Motivo da Prorrogação", 
            placeholder="Ex: Atraso na entrega dos bens devido a greve na fábrica, conforme justificado pela contratada..."
        )
