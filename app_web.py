import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Central de Agentes", page_icon="🤖", layout="wide")

st.title("🤖 Central de Agentes Automatizados")
st.markdown("Painel de gestão e monitoramento em tempo real dos robôs de automação.")

# Conexão com o banco de dados
def carregar_dados():
    conexao = sqlite3.connect("mercado.db")
    
    # Carrega atendimentos
    df_atendimentos = pd.read_sql_query("SELECT id, data_hora, cliente, categoria, mensagem_original FROM atendimentos", conexao)
    
    # Carrega faturas
    df_faturas = pd.read_sql_query("SELECT id, data_registro, favorecido, valor FROM faturas", conexao)
    
    conexao.close()
    return df_atendimentos, df_faturas

try:
    df_atendimentos, df_faturas = carregar_dados()

    # Métricas principais
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Atendimentos", len(df_atendimentos))
    col2.metric("Total de Faturas Processadas", len(df_faturas))
    total_faturas = df_faturas["valor"].sum() if not df_faturas.empty else 0.0
    col3.metric("Valor Total Processado", f"R$ {total_faturas:,.2f}")

    st.divider()

    # Abas para cada agente
    aba1, aba2 = st.tabs(["💬 [Agente #2] Atendimentos & Triagem", "📄 [Agente #3] Comprovantes & Faturas"])

    with aba1:
        st.subheader("Histórico de Atendimentos Recebidos")
        if df_atendimentos.empty:
            st.info("Nenhum atendimento registrado ainda.")
        else:
            st.dataframe(df_atendimentos, use_container_width=True)

    with aba2:
        st.subheader("Lançamentos de Faturas e Comprovantes")
        if df_faturas.empty:
            st.info("Nenhuma fatura registrada ainda.")
        else:
            st.dataframe(df_faturas, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar os dados do banco mercado.db: {e}")