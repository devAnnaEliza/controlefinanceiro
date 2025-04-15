import csv
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import openpyxl

# Dicionários para armazenar dados
usuarios = {}
saidas = {}

# Funções para salvar e carregar dados
def salvar_dados():
    with open('entradas.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Usuário', 'Valor', 'Data'])
        for usuario, (valor, data) in usuarios.items():
            writer.writerow([usuario, valor, data])

    with open('saidas.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Descrição', 'Valor', 'Data'])
        for descricao, (valor, data) in saidas.items():
            writer.writerow([descricao, valor, data])

def carregar_dados():
    try:
        with open('entradas.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Pular cabeçalho
            for row in reader:
                if len(row) >= 3 and all(row):  # Verifica se a linha tem pelo menos 3 colunas
                    usuarios[row[0]] = (float(row[1]), row[2])

        with open('saidas.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Pular cabeçalho
            for row in reader:
                if len(row) >= 3 and all(row):  # Verifica se a linha tem pelo menos 3 colunas
                    saidas[row[0]] = (float(row[1]), row[2])
    except FileNotFoundError:
        print("Arquivos de dados não encontrados. Iniciando com dados vazios.")

def exportar_para_excel():
    workbook = openpyxl.Workbook()
    sheet_entradas = workbook.active
    sheet_entradas.title = "Entradas"
    sheet_saidas = workbook.create_sheet(title="Saídas")

    # Adicionar cabeçalhos
    sheet_entradas.append(["Usuário", "Valor", "Data"])
    sheet_saidas.append(["Descrição", "Valor", "Data"])

    # Adicionar dados
    for usuario, (valor, data) in usuarios.items():
        sheet_entradas.append([usuario, valor, data])

    for descricao, (valor, data) in saidas.items():
        sheet_saidas.append([descricao, valor, data])

    # Salvar arquivo
    workbook.save("controle_financeiro.xlsx")
    messagebox.showinfo("Exportação", "Dados exportados para 'controle_financeiro.xlsx'.")

# Funções para o front-end
def cadastrar_usuario():
    nome = entry_nome.get()
    valor = entry_valor.get().replace(',', '.')
    data = datetime.now().strftime('%Y-%m')  # Captura o mês e ano atual
    if nome and valor:
        try:
            valor = float(valor)
            usuarios[nome] = (valor, data)
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
    data = datetime.now().strftime('%Y-%m')  # Captura o mês e ano atual
    if descricao and valor:
        try:
            valor = float(valor)
            saidas[descricao] = (valor, data)
            salvar_dados()
            messagebox.showinfo("Sucesso", f"Saída {descricao} registrada com valor de R$ {valor:.2f}.")
            entry_descricao.delete(0, tk.END)
            entry_saida_valor.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")
    else:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

def calcular_saldo():
    total_entradas = sum(valor for valor, _ in usuarios.values())
    total_saidas = sum(valor for valor, _ in saidas.values())
    saldo_final = total_entradas - total_saidas
    messagebox.showinfo("Saldo Final", f"Total de Entradas: R$ {total_entradas:.2f}\n"
                                       f"Total de Saídas: R$ {total_saidas:.2f}\n"
                                       f"Saldo Final: R$ {saldo_final:.2f}")

def listar_dados_por_mes():
    mes = entry_mes.get()
    if not mes:
        messagebox.showerror("Erro", "Por favor, insira o mês no formato YYYY-MM.")
        return

    entradas_mes = {usuario: valor for usuario, (valor, data) in usuarios.items() if data == mes}
    saidas_mes = {descricao: valor for descricao, (valor, data) in saidas.items() if data == mes}

    total_entradas = sum(entradas_mes.values())
    total_saidas = sum(saidas_mes.values())
    saldo_mes = total_entradas - total_saidas

    dados = f"--- Dados do Mês {mes} ---\n"
    dados += "--- Entradas ---\n"
    for usuario, valor in entradas_mes.items():
        dados += f"{usuario}: R$ {valor:.2f}\n"
    dados += "--- Saídas ---\n"
    for descricao, valor in saidas_mes.items():
        dados += f"{descricao}: R$ {valor:.2f}\n"
    dados += f"\nSaldo do Mês: R$ {saldo_mes:.2f}"

    messagebox.showinfo(f"Dados do Mês {mes}", dados)

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


# Seção de Listagem por Mês
frame_mes = tk.Frame(root)
frame_mes.pack(pady=10)

tk.Label(frame_mes, text="Mês (YYYY-MM):").grid(row=0, column=0, padx=5, pady=5)
entry_mes = tk.Entry(frame_mes)
entry_mes.grid(row=0, column=1, padx=5, pady=5)

btn_listar_mes = tk.Button(frame_mes, text="Listar Dados por Mês", command=listar_dados_por_mes)
btn_listar_mes.grid(row=1, column=0, columnspan=2, pady=10)

# Botões de Ações Gerais
frame_acoes = tk.Frame(root)
frame_acoes.pack(pady=10)

btn_calcular_saldo = tk.Button(frame_acoes, text="Calcular Saldo", command=calcular_saldo)
btn_calcular_saldo.pack(side=tk.LEFT, padx=10)

btn_exportar = tk.Button(frame_acoes, text="Exportar para Excel", command=exportar_para_excel)
btn_exportar.pack(side=tk.LEFT, padx=10)

# Iniciar o loop da interface gráfica
root.mainloop()