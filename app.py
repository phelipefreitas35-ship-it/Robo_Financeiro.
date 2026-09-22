import sqlite3
import time
from datetime import datetime
from google import genai
import yfinance as yf

# Configuração do cliente Gemini (Mantenha as aspas)
API_KEY = "SUA_CHAVE_AQUI"
client = genai.Client(api_key=API_KEY)


def inicializar_banco():
    """Cria o banco de dados e a tabela se ainda não existirem."""
    conexao = sqlite3.connect("mercado.db")
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_mercado (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT,
            ativo TEXT,
            preco REAL,
            variacao_pct REAL
        )
    """)

    conexao.commit()
    conexao.close()


def salvar_no_banco(dados):
    """Salva os preços e variações coletadas no banco SQLite."""
    conexao = sqlite3.connect("mercado.db")
    cursor = conexao.cursor()

    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for ticker, info in dados.items():
        cursor.execute("""
            INSERT INTO historico_mercado (data_hora, ativo, preco, variacao_pct)
            VALUES (?, ?, ?, ?)
        """, (data_atual, info['nome'], info['preco_atual'], info['variacao_pct']))

    conexao.commit()
    conexao.close()
    print("[Sucesso] Dados salvos no banco SQLite ('mercado.db')!")


def obter_dados_mercado():
    print("Coletando dados financeiros...")
    tickers = {
        "BRL=X": "Dólar",
        "^BVSP": "Ibovespa",
        "BTC-USD": "Bitcoin",
    }

    dados = {}

    for ticker, nome in tickers.items():
        acao = yf.Ticker(ticker)
        historico = acao.history(period="5d")

        if historico.empty:
            continue

        preco_atual = float(historico["Close"].iloc[-1])
        preco_anterior = (
            float(historico["Close"].iloc[-2])
            if len(historico) > 1
            else preco_atual
        )

        variacao_pct = 0.0
        if preco_anterior:
            variacao_pct = (
                (preco_atual - preco_anterior) / preco_anterior
            ) * 100

        dados[ticker] = {
            "nome": nome,
            "preco_atual": round(preco_atual, 2),
            "variacao_pct": round(variacao_pct, 2),
        }

    return dados


def gerar_analise_ia(dados):
    print("Gerando relatório com Inteligência Artificial...")

    dolar = dados.get("BRL=X", {})
    ibovespa = dados.get("^BVSP", {})
    bitcoin = dados.get("BTC-USD", {})

    prompt = f"""
    Você é um analista financeiro sênior.
    Analise os seguintes dados do mercado financeiro coletados hoje:
    - Dólar em BRL: R$ {dolar.get('preco_atual', 'N/A')}
    - Variação diária do dólar: {dolar.get('variacao_pct', 'N/A')}%
    - Ibovespa: {ibovespa.get('preco_atual', 'N/A')} pontos
    - Variação diária do Ibovespa: {ibovespa.get('variacao_pct', 'N/A')}%
    - Bitcoin em USD: $ {bitcoin.get('preco_atual', 'N/A')}
    - Variação diária do Bitcoin: {bitcoin.get('variacao_pct', 'N/A')}%

    IMPORTANTE: responda em português do Brasil, de forma clara e direta.
    Escreva um relatório executivo curto contendo:
    1. Resumo do cenário atual.
    2. Destaques de cada um desses três ativos, incluindo a variação do dia.
    3. Um conselho prático sobre cautela ou oportunidade para o mercado geral.
    4. Evite dizer que é recomendação profissional ou garantia de lucro.
    5. Não use termos em inglês. Escreva tudo em português.
    """

    modelo = "gemini-1.5-flash"

    for tentativa in range(3):
        try:
            response = client.models.generate_content(
                model=modelo,
                contents=prompt,
            )
            return response.text
        except Exception as e:
            print(
                f"[Aviso] Servidor ocupado. Tentativa {tentativa + 1} de 3... Aguardando 5 segundos."
            )
            time.sleep(5)

    raise RuntimeError("O servidor do Google ainda está congestionado. Aguarde mais alguns minutos.")


if __name__ == "__main__":
    # 1. Garante que o Banco de Dados e a tabela existem
    inicializar_banco()

    # 2. Coleta os dados financeiros
    dados_mercado = obter_dados_mercado()

    # 3. Salva a cotação atual no Banco de Dados SQLite
    salvar_no_banco(dados_mercado)

    # 4. Gera a análise com a IA
    relatorio = gerar_analise_ia(dados_mercado)

    print("\n" + "=" * 40)
    print(" BOLETIM DE MERCADO AUTOMÁTICO ")
    print("=" * 40 + "\n")
    print(relatorio)

    with open("relatorio_mercado.txt", "w", encoding="utf-8") as f:
        f.write(relatorio)

    print("\n[Sucesso] Relatório salvo em 'relatorio_mercado.txt'!")