import sqlite3

def exibir_painel_geral():
    """Consulta e exibe os dados consolidados de todos os agentes."""
    conexao = sqlite3.connect("mercado.db")
    cursor = conexao.cursor()
    
    print("\n" + "="*55)
    print("      CENTRAL DE AGENTES - PAINEL DE CONTROLE")
    print("="*55)
    
    # 1. Consulta Agente #2 (Atendimentos)
    print("\n--- [AGENTE #2] HISTÓRICO DE ATENDIMENTOS ---")
    cursor.execute("SELECT id, data_hora, cliente, categoria, mensagem_original FROM atendimentos")
    atendimentos = cursor.fetchall()
    
    if not atendimentos:
        print("Nenhum atendimento registrado.")
    else:
        for reg in atendimentos:
            print(f"ID: {reg[0]} | Data: {reg[1]} | Cliente: {reg[2]}")
            print(f"   Categoria: [{reg[3]}] | Mensagem: \"{reg[4]}\"")
            print("-" * 55)
            
    # 2. Consulta Agente #3 (Faturas)
    print("\n--- [AGENTE #3] LANÇAMENTOS DE FATURAS E COMPROVANTES ---")
    cursor.execute("SELECT id, data_registro, favorecido, valor FROM faturas")
    faturas = cursor.fetchall()
    
    if not faturas:
        print("Nenhuma fatura registrada.")
    else:
        total = 0.0
        for fat in faturas:
            print(f"ID: {fat[0]} | Data: {fat[1]} | Favorecido: {fat[2]} | Valor: R$ {fat[3]:.2f}")
            total += fat[3]
        print("-" * 55)
        print(f" TOTAL PROCESSADO EM FATURAS: R$ {total:.2f}")
        
    conexao.close()

if __name__ == "__main__":
    exibir_painel_geral()