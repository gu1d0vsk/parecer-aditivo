import streamlit as st

def render_quantitativo(dados):
    """Renderiza a aba de Alteração Quantitativa e valida os 25%."""
    st.subheader("Cálculo de Acréscimo e Supressão")
    st.caption("Base Legal: Lei 13.303/2016, Art. 81, §1º (Limite de 25%)")
    
    col_q1, col_q2 = st.columns(2)
    valor_atual = col_q1.number_input("Valor Atualizado do Contrato (Base) R$", min_value=0.01, format="%.2f")
    
    st.markdown("---")
    
    col_q3, col_q4 = st.columns(2)
    acrescimo = col_q3.number_input("Valor a ACRESCER (+)", min_value=0.0, format="%.2f")
    supressao = col_q4.number_input("Valor a SUPRIMIR (-)", min_value=0.0, format="%.2f")
    
    # Lógica
    if valor_atual > 0:
        perc_acrescimo = (acrescimo / valor_atual) * 100
        perc_supressao = (supressao / valor_atual) * 100
        novo_valor = valor_atual + acrescimo - supressao
        
        # Display Visual
        c1, c2, c3 = st.columns(3)
        c1.metric("Novo Valor Global", f"R$ {novo_valor:,.2f}")
        c2.metric("% Acréscimo", f"{perc_acrescimo:.2f}%", delta_color="inverse" if perc_acrescimo > 25 else "normal")
        c3.metric("% Supressão", f"{perc_supressao:.2f}%")
        
        # Validação
        if perc_acrescimo > 25:
            st.error(f"🚨 O acréscimo de {perc_acrescimo:.2f}% extrapola o limite legal de 25%!")
            aviso_legal = "O acréscimo extrapola o limite legal de 25%, exigindo justificativa excepcionalíssima."
        else:
            st.success("✅ Percentuais dentro do limite legal.")
            aviso_legal = "A alteração respeita o limite legal de 25% do valor inicial atualizado."

        # Texto Automático
        texto = (f"O valor inicial atualizado base é de R$ {valor_atual:,.2f}. "
                 f"Será realizado um acréscimo de R$ {acrescimo:,.2f} ({perc_acrescimo:.2f}%) "
                 f"e uma supressão de R$ {supressao:,.2f} ({perc_supressao:.2f}%). "
                 f"O novo valor global do contrato passa a ser R$ {novo_valor:,.2f}. "
                 f"{aviso_legal}")
        
        dados['texto_quantitativo'] = texto
