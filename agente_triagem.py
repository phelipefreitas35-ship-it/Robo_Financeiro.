import sqlite3
from datetime import datetime

def inicializar_tabela_atendimento():
    """Cria a tabela de atendimentos no banco SQLite existente."""
    conexao = sqlite3.connect("mercado.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atendimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT,
            cliente TEXT,
            mensagem_original TEXT,
            categoria TEXT,
            resposta_gerada TEXT
        )
    """)
    conexao.commit()
    conexao.close()

def triar_mensagem(mensagem_cliente):
    """Categoriza a mensagem e define uma resposta inicial."""
    msg = mensagem_cliente.lower()
    
    if "preço" in msg or "quanto custa" in msg or "comprar" in msg:
        categoria = "ORCAMENTO"
        resposta = "Olá! Nosso catálogo de serviços e valores foi enviado para o seu e-mail/WhatsApp."
    elif "erro" in msg or "problema" in msg or "ajuda" in msg:
        categoria = "SUPORTE"
        resposta = "Anotamos o seu pedido de suporte. Um técnico entrará em contato em até 15 minutos."
    else:
        categoria = "GERAL"
        resposta = "Olá! Como posso ajudar você hoje?"
        
    return categoria, resposta

def registrar_atendimento(cliente, mensagem):
    """Executa a triagem e salva o registro completo no SQLite."""
    categoria, resposta = triar_mensagem(mensagem)
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conexao = sqlite3.connect("mercado.db")
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO atendimentos (data_hora, cliente, mensagem_original, categoria, resposta_gerada)
        VALUES (?, ?, ?, ?, ?)
    """, (data_hora, cliente, mensagem, categoria, resposta))
    
    conexao.commit()
    conexao.close()
    
    print(f"[{data_hora}] Atendimento registrado para '{cliente}' | Categoria: {categoria}")
    print(f"-> Resposta Enviada: {resposta}\n")

if __name__ == "__main__":
    inicializar_tabela_atendimento()
    print("=== CENTRAL DE ATENDIMENTO - AGENTE #2 ===\n")
    
    # Testando 3 cenários reais de clientes
    registrar_atendimento("Cliente 1 - João", "Olá, quanto custa o serviço de automação?")
    registrar_atendimento("Cliente 2 - Maria", "Estou com um erro no meu sistema, precisa de ajuda")
    registrar_atendimento("Cliente 3 - Carlos", "Qual o horário de funcionamento de vocês?")