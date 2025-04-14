import csv
import tkinter as tk 
from tkinter import messagebox

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

# Funções para o front-end
def cadastrar_usuario():
    nome = entry_nome.get()
    valor = entry_valor.get().replace(',', '.')
    if nome and valor:
        try:
            valor = float(valor)
            usuarios[nome] = valor
            salvar_dados()
            messagebox.showinfo("Sucesso", f"Usuário {nome} cadastrado com entrada de R$ {valor:.2f}.")
            entry_nome.delete(0, tk.END)
            entry_valor.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")
    else:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

def registrar_saida():
    descricao = entry_descricao.get()
    valor = entry_saida_valor.get().replace(',', '.')
    if descricao and valor:
        try:
            valor = float(valor)
            saidas[descricao] = valor
            salvar_dados()
            messagebox.showinfo("Sucesso", f"Saída {descricao} registrada com valor de R$ {valor:.2f}.")
            entry_descricao.delete(0, tk.END)
            entry_saida_valor.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")
    else:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

def calcular_saldo():
    total_entradas = sum(usuarios.values())
    total_saidas = sum(saidas.values())
    saldo_final = total_entradas - total_saidas
    messagebox.showinfo("Saldo Final", f"Total de Entradas: R$ {total_entradas:.2f}\n"
                                       f"Total de Saídas: R$ {total_saidas:.2f}\n"
                                       f"Saldo Final: R$ {saldo_final:.2f}")

def listar_dados():
    dados = "--- Entradas ---\n"
    for usuario, valor in usuarios.items():
        dados += f"{usuario}: R$ {valor:.2f}\n"
    dados += "\n--- Saídas ---\n"
    for descricao, valor in saidas.items():
        dados += f"{descricao}: R$ {valor:.2f}\n"
    messagebox.showinfo("Dados Registrados", dados)

# Interface gráfica com Tkinter
carregar_dados()

root = tk.Tk()
root.title("Controle Financeiro")

# Seção de Cadastro de Usuários
frame_cadastro = tk.Frame(root)
frame_cadastro.pack(pady=10)

tk.Label(frame_cadastro, text="Nome do Usuário:").grid(row=0, column=0, padx=5, pady=5)
entry_nome = tk.Entry(frame_cadastro)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_cadastro, text="Valor de Entrada:").grid(row=1, column=0, padx=5, pady=5)
entry_valor = tk.Entry(frame_cadastro)
entry_valor.grid(row=1, column=1, padx=5, pady=5)

btn_cadastrar = tk.Button(frame_cadastro, text="Cadastrar Usuário", command=cadastrar_usuario)
btn_cadastrar.grid(row=2, column=0, columnspan=2, pady=10)

# Seção de Registro de Saídas
frame_saidas = tk.Frame(root)
frame_saidas.pack(pady=10)

tk.Label(frame_saidas, text="Descrição da Saída:").grid(row=0, column=0, padx=5, pady=5)
entry_descricao = tk.Entry(frame_saidas)
entry_descricao.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_saidas, text="Valor da Saída:").grid(row=1, column=0, padx=5, pady=5)
entry_saida_valor = tk.Entry(frame_saidas)
entry_saida_valor.grid(row=1, column=1, padx=5, pady=5)

btn_registrar_saida = tk.Button(frame_saidas, text="Registrar Saída", command=registrar_saida)
btn_registrar_saida.grid(row=2, column=0, columnspan=2, pady=10)

# Botões de Ações Gerais
frame_acoes = tk.Frame(root)
frame_acoes.pack(pady=10)

btn_calcular_saldo = tk.Button(frame_acoes, text="Calcular Saldo", command=calcular_saldo)
btn_calcular_saldo.pack(side=tk.LEFT, padx=10)

btn_listar_dados = tk.Button(frame_acoes, text="Listar Dados", command=listar_dados)
btn_listar_dados.pack(side=tk.LEFT, padx=10)

# Iniciar o loop da interface gráfica
root.mainloop()