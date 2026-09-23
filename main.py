import sys
import subprocess

def exibir_menu():
    print("\n" + "="*50)
    print("       CENTRAL DE AGENTES AUTOMATIZADOS")
    print("="*50)
    print(" 1. Executar Agente #1 (Robô Financeiro)")
    print(" 2. Executar Agente #2 (Triagem de Mensagens)")
    print(" 3. Executar Agente #3 (Leitor de Faturas)")
    print(" 4. Abrir Painel Central (Consolidado)")
    print(" 0. Sair")
    print("="*50)

def main():
    while True:
        exibir_menu()
        opcao = input(" Escolha uma opção: ").strip()
        
        if opcao == "1":
            print("\n Iniciando Agente #1...\n")
            subprocess.run([sys.executable, "app.py"])
        elif opcao == "2":
            print("\n Iniciando Agente #2...\n")
            subprocess.run([sys.executable, "agente_triagem.py"])
        elif opcao == "3":
            print("\n Iniciando Agente #3...\n")
            subprocess.run([sys.executable, "agente_leitor.py"])
        elif opcao == "4":
            print("\n Carregando Painel Central...\n")
            subprocess.run([sys.executable, "painel_central.py"])
        elif opcao == "0":
            print("\n Encerrando a Central de Agentes. Até logo!\n")
            break
        else:
            print("\n Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()