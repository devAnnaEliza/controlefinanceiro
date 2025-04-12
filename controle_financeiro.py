import csv

# Dicionários para armazenar dados
usuarios = {}
saidas = {}

# Funções para salvar e carregar dados
def salvar_dados():
    with open('entradas.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Usuário', 'Valor'])
        for usuario, valor in usuarios.items():
            writer.writerow([usuario, valor])

    with open('saidas.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Descrição', 'Valor'])
        for descricao, valor in saidas.items():
            writer.writerow([descricao, valor])

def carregar_dados():
    try:
        with open('entradas.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Pular cabeçalho
            for row in reader:
                usuarios[row[0]] = float(row[1])

        with open('saidas.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Pular cabeçalho
            for row in reader:
                saidas[row[0]] = float(row[1])
    except FileNotFoundError:
        print("Arquivos de dados não encontrados. Iniciando com dados vazios.")

# Funções existentes
def cadastrar_usuario():
    nome = input("Digite o nome do usuário: ")
    valor = input(f"Digite o valor de entrada para {nome}: ").replace(',', '.')
    valor = float(valor)
    usuarios[nome] = valor
    salvar_dados()
    print(f"Usuário {nome} cadastrado com entrada de R$ {valor:.2f}.\n")

def registrar_saida():
    descricao = input("Digite a descrição da saída (ex: Água, Luz): ")
    valor = input(f"Digite o valor da saída para {descricao}: ").replace(',', '.')
    valor = float(valor)
    saidas[descricao] = valor
    salvar_dados()
    print(f"Saída {descricao} registrada com valor de R$ {valor:.2f}.\n")

def calcular_saldo():
    total_entradas = sum(usuarios.values())
    total_saidas = sum(saidas.values())
    saldo_final = total_entradas - total_saidas

    print("\n--- Resumo Financeiro ---")
    print(f"Total de Entradas: R$ {total_entradas:.2f}")
    print(f"Total de Saídas: R$ {total_saidas:.2f}")
    print(f"Saldo Final: R$ {saldo_final:.2f}\n")

def listar_dados():
    print("\n--- Entradas ---")
    for usuario, valor in usuarios.items():
        print(f"{usuario}: R$ {valor:.2f}")

    print("\n--- Saídas ---")
    for descricao, valor in saidas.items():
        print(f"{descricao}: R$ {valor:.2f}")
    print()

def menu():
    carregar_dados()  # Carregar dados ao iniciar o programa
    while True:
        print("1. Cadastrar Usuário e Entrada")
        print("2. Registrar Saída")
        print("3. Calcular Saldo Final")
        print("4. Listar Dados")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            registrar_saida()
        elif opcao == "3":
            calcular_saldo()
        elif opcao == "4":
            listar_dados()
        elif opcao == "5":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.\n")

# Iniciar o programa
if __name__ == "__main__":
    menu()