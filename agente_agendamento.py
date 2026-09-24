import sqlite3
from datetime import datetime

def inicializar_banco():
    conexao = sqlite3.connect("mercado.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente TEXT NOT NULL,
            procedimento TEXT NOT NULL,
            data_consulta TEXT NOT NULL,
            status TEXT NOT NULL,
            data_registro TEXT NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()

def registrar_agendamento(paciente, procedimento, data_consulta, status="Confirmado"):
    inicializar_banco()
    conexao = sqlite3.connect("mercado.db")
    cursor = conexao.cursor()
    
    data_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO agendamentos (paciente, procedimento, data_consulta, status, data_registro)
        VALUES (?, ?, ?, ?, ?)
    """, (paciente, procedimento, data_consulta, status, data_registro))
    
    conexao.commit()
    conexao.close()
    print(f" Agendamento registrado para {paciente} - Status: {status}")

def executar_simulacao_agendamentos():
    print(" Executando Agente #4: Gestor de Agendamentos...")
    
    # Simulação de consultas agendadas via automação
    agendamentos_teste = [
        ("Dra. Beatriz Santos", "Consulta de Rotina", "2026-09-25 09:00", "Confirmado"),
        ("Carlos Eduardo", "Avaliação Odontológica", "2026-09-25 10:30", "Pendente PIX"),
        ("Fernanda Lima", "Exame de Sangue", "2026-09-25 14:00", "Lembrete Enviado"),
    ]
    
    for paciente, procedimento, data_c, st in agendamentos_teste:
        registrar_agendamento(paciente, procedimento, data_c, st)
        
    print(" Simulação do Agente #4 concluída com sucesso!")

if __name__ == "__main__":
    executar_simulacao_agendamentos()