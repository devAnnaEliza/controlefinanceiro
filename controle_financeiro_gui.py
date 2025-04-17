import tkinter as tk
from tkinter import ttk, messagebox
from dados import salvar_dados, carregar_dados, usuarios, saidas


# Funções para o front-end
def cadastrar_usuario():
    nome = entry_nome.get().strip()
    valor = entry_valor.get().replace(',', '.').strip()
    data = entry_data.get().strip()  # Captura o mês e ano fornecido pelo usuário
    if not data or len(data) != 7 or not data[:4].isdigit() or not data[5:].isdigit() or data[4] != '-':
        messagebox.showerror("Erro", "Por favor, insira a data no formato YYYY-MM.")
        return

    if nome and valor:
        try:
            valor = float(valor)
            usuarios[nome] = (valor, data)
            salvar_dados()
            entry_nome.delete(0, tk.END)
            entry_valor.delete(0, tk.END)
            entry_data.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")
    else:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")


def registrar_saida():
    descricao = entry_descricao.get().strip()
    valor = entry_saida_valor.get().replace(',', '.').strip()
    data = entry_saida_data.get().strip()  # Captura o mês e ano fornecido pelo usuário
    if not data or len(data) != 7 or not data[:4].isdigit() or not data[5:].isdigit() or data[4] != '-':
        messagebox.showerror("Erro", "Por favor, insira a data no formato YYYY-MM.")
        return

    if descricao and valor:
        try:
            valor = float(valor)
            saidas[descricao] = (valor, data)
            salvar_dados()
            entry_descricao.delete(0, tk.END)
            entry_saida_valor.delete(0, tk.END)
            entry_saida_data.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")
    else:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")


def exibir_entradas_por_mes():
    mes = entry_mes.get().strip()
    if not mes:
        messagebox.showerror("Erro", "Por favor, insira o mês no formato YYYY-MM.")
        return

    entradas_window = tk.Toplevel(root)
    entradas_window.title(f"Entradas - {mes}")

    tree = ttk.Treeview(entradas_window, columns=("Usuário", "Valor", "Data"), show="headings")
    tree.heading("Usuário", text="Usuário")
    tree.heading("Valor", text="Valor (R$)")
    tree.heading("Data", text="Data")
    tree.pack(fill=tk.BOTH, expand=True)

    total_entradas = 0
    for usuario, (valor, data) in usuarios.items():
        if data.startswith(mes):
            tree.insert("", tk.END, values=(usuario, f"{valor:.2f}", data))
            total_entradas += valor

    tk.Label(entradas_window, text=f"Total de Entradas: R$ {total_entradas:.2f}", font=("Arial", 12, "bold")).pack(pady=10)


def exibir_saidas_por_mes():
    mes = entry_mes.get().strip()
    if not mes:
        messagebox.showerror("Erro", "Por favor, insira o mês no formato YYYY-MM.")
        return

    saidas_window = tk.Toplevel(root)
    saidas_window.title(f"Saídas - {mes}")

    tree = ttk.Treeview(saidas_window, columns=("Descrição", "Valor", "Data"), show="headings")
    tree.heading("Descrição", text="Descrição")
    tree.heading("Valor", text="Valor (R$)")
    tree.heading("Data", text="Data")
    tree.pack(fill=tk.BOTH, expand=True)

    total_saidas = 0
    for descricao, (valor, data) in saidas.items():
        if data.startswith(mes):
            tree.insert("", tk.END, values=(descricao, f"{valor:.2f}", data))
            total_saidas += valor

    tk.Label(saidas_window, text=f"Total de Saídas: R$ {total_saidas:.2f}", font=("Arial", 12, "bold")).pack(pady=10)


def exibir_saldo_por_mes():
    mes = entry_mes.get().strip()
    if not mes or len(mes) != 7 or not mes[:4].isdigit() or not mes[5:].isdigit() or mes[4] != '-':
        messagebox.showerror("Erro", "Por favor, insira o mês no formato YYYY-MM.")
        return

    saldo_window = tk.Toplevel(root)
    saldo_window.title(f"Saldo - {mes}")

    total_entradas = sum(valor for usuario, (valor, data) in usuarios.items() if data.startswith(mes))
    total_saidas = sum(valor for descricao, (valor, data) in saidas.items() if data.startswith(mes))
    saldo_final = total_entradas - total_saidas

    tk.Label(saldo_window, text=f"Total de Entradas: R$ {total_entradas:.2f}\n"
                                f"Total de Saídas: R$ {total_saidas:.2f}\n"
                                f"Saldo Final: R$ {saldo_final:.2f}",
             font=("Arial", 12, "bold")).pack(pady=20)


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

tk.Label(frame_cadastro, text="Data (YYYY-MM):").grid(row=2, column=0, padx=5, pady=5)
entry_data = tk.Entry(frame_cadastro)
entry_data.grid(row=2, column=1, padx=5, pady=5)

tk.Button(frame_cadastro, text="Cadastrar Usuário", command=cadastrar_usuario).grid(row=3, column=0, columnspan=2, pady=10)

# Seção de Registro de Saídas
frame_saidas = tk.Frame(root)
frame_saidas.pack(pady=10)

tk.Label(frame_saidas, text="Descrição da Saída:").grid(row=0, column=0, padx=5, pady=5)
entry_descricao = tk.Entry(frame_saidas)
entry_descricao.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_saidas, text="Valor da Saída:").grid(row=1, column=0, padx=5, pady=5)
entry_saida_valor = tk.Entry(frame_saidas)
entry_saida_valor.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_saidas, text="Data (YYYY-MM):").grid(row=2, column=0, padx=5, pady=5)
entry_saida_data = tk.Entry(frame_saidas)
entry_saida_data.grid(row=2, column=1, padx=5, pady=5)

tk.Button(frame_saidas, text="Registrar Saída", command=registrar_saida).grid(row=3, column=0, columnspan=2, pady=10)

# Campo para selecionar o mês
frame_mes = tk.Frame(root)
frame_mes.pack(pady=10)

tk.Label(frame_mes, text="Mês (YYYY-MM):").grid(row=0, column=0, padx=5, pady=5)
entry_mes = tk.Entry(frame_mes)
entry_mes.grid(row=0, column=1, padx=5, pady=5)

tk.Button(frame_mes, text="Exibir Entradas", command=exibir_entradas_por_mes).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_mes, text="Exibir Saídas", command=exibir_saidas_por_mes).grid(row=1, column=1, padx=5, pady=5)
tk.Button(frame_mes, text="Exibir Saldo", command=exibir_saldo_por_mes).grid(row=1, column=2, padx=5, pady=5)

# Iniciar o loop da interface gráfica
root.mainloop()