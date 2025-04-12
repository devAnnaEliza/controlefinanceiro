# Dicionários para armazenar dados
usuarios = {}
saidas = {}

def cadastrar_usuario():
    nome = input("Digite o nome do usuário: ")
    valor = float(input(f"Digite o valor de entrada para {nome}: "))
    usuarios[nome] = valor
    print(f"Usuário {nome} cadastrado com entrada de R$ {valor:.2f}.\n")

def registrar_saida():
    descricao = input("Digite a descrição da saída (ex: Água, Luz): ")
    valor = float(input(f"Digite o valor da saída para {descricao}: "))
    saidas[descricao] = valor
    print(f"Saída {descricao} registrada com valor de R$ {valor:.2f}.\n")

def calcular_saldo():
    total_entradas = sum(usuarios.values())
    total_saidas = sum(saidas.values())
    saldo_final = total_entradas - total_saidas

    print("\n--- Resumo Financeiro ---")
    print(f"Total de Entradas: R$ {total_entradas:.2f}")
    print(f"Total de Saídas: R$ {total_saidas:.2f}")
    print(f"Saldo Final: R$ {saldo_final:.2f}\n")

def menu():
    while True:
        print("1. Cadastrar Usuário e Entrada")
        print("2. Registrar Saída")
        print("3. Calcular Saldo Final")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            registrar_saida()
        elif opcao == "3":
            calcular_saldo()
        elif opcao == "4":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.\n")

# Iniciar o programa
if __name__ == "__main__":
    menu()