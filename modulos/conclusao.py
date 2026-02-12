import streamlit as st

def render_conclusao(dados):
    """Renderiza a aba de conclusão e validações finais."""
    st.subheader("Parecer Final")
    
    c1, c2 = st.columns(2)
    check_doc = c1.checkbox("Habilitação Regular (SICAF/CNDs)?", value=True)
    check_orc = c2.checkbox("Existe Dotação Orçamentária?", value=True)
    
    st.markdown("---")
    
    if check_doc and check_orc:
        st.success("✅ Parecer Favorável.")
        dados['conclusao_texto'] = "Diante do exposto, opinamos favoravelmente ao prosseguimento do feito e assinatura do Termo Aditivo."
    else:
        st.warning("⚠️ Pendências identificadas.")
        dados['conclusao_texto'] = "Sugerimos o saneamento das pendências apontadas (regularidade fiscal ou orçamentária) antes da assinatura."
