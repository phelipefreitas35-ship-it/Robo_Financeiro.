import sqlite3

def exibir_resumo_atendimentos():
    """Consulta e exibe os atendimentos salvos pelo Agente #2."""
    conexao = sqlite3.connect("mercado.db")
    cursor = conexao.cursor()
    
    print("\n" + "="*50)
    print("      CENTRAL DE AGENTES - PAINEL DE CONTROLE")
    print("="*50)
    print("\n--- [AGENTE #2] HISTÓRICO DE ATENDIMENTOS ---")
    
    cursor.execute("SELECT id, data_hora, cliente, categoria, mensagem_original FROM atendimentos")
    registros = cursor.fetchall()
    
    if not registros:
        print("Nenhum atendimento registrado até o momento.")
    else:
        for reg in registros:
            print(f"ID: {reg[0]} | Data: {reg[1]} | Cliente: {reg[2]}")
            print(f"   Categoria: [{reg[3]}] | Mensagem: \"{reg[4]}\"")
            print("-" * 50)
            
    conexao.close()

if __name__ == "__main__":
    exibir_resumo_atendimentos()