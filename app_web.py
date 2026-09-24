import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Central de Agentes", page_icon="🤖", layout="wide")

st.title("🤖 Central de Agentes Automatizados")
st.markdown("Painel de gestão e monitoramento em tempo real dos robôs de automação.")

def carregar_dados():
    conexao = sqlite3.connect("mercado.db")
    
    df_atendimentos = pd.read_sql_query("SELECT id, data_hora, cliente, categoria, mensagem_original FROM atendimentos", conexao)
    df_faturas = pd.read_sql_query("SELECT id, data_registro, favorecido, valor FROM faturas", conexao)
    
    # Tenta carregar agendamentos (se existir)
    try:
        df_agendamentos = pd.read_sql_query("SELECT id, paciente, procedimento, data_consulta, status, data_registro FROM agendamentos", conexao)
    except Exception:
        df_agendamentos = pd.DataFrame()
        
    conexao.close()
    return df_atendimentos, df_faturas, df_agendamentos

try:
    df_atendimentos, df_faturas, df_agendamentos = carregar_dados()

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Atendimentos", len(df_atendimentos))
    col2.metric("Total Faturas", len(df_faturas))
    total_faturas = df_faturas["valor"].sum() if not df_faturas.empty else 0.0
    col3.metric("Valor Processado", f"R$ {total_faturas:,.2f}")
    col4.metric("Agendamentos Ativos", len(df_agendamentos))

    st.divider()

    aba1, aba2, aba3 = st.tabs([
        "💬 [Agente #2] Triagem", 
        "📄 [Agente #3] Faturas", 
        "📅 [Agente #4] Agendamentos Clínica"
    ])

    with aba1:
        st.subheader("Histórico de Atendimentos Recebidos")
        st.dataframe(df_atendimentos, use_container_width=True)

    with aba2:
        st.subheader("Lançamentos de Faturas e Comprovantes")
        st.dataframe(df_faturas, use_container_width=True)

    with aba3:
        st.subheader("Consultas e Agendamentos Automatizados")
        if df_agendamentos.empty:
            st.info("Nenhum agendamento registrado. Execute o agente_agendamento.py primeiro.")
        else:
            st.dataframe(df_agendamentos, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar os dados do banco mercado.db: {e}")