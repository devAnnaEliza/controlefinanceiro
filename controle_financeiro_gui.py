import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd 
from dados import salvar_dados, carregar_dados, usuarios, saidas


def exportar_para_excel():
    try:
        entradas_df = pd.DataFrame([
            {"Tipo": "Entrada", "Descrição/Usuário": usuario, "Valor (R$)": valor, "Data": data}
            for usuario, (valor, data) in usuarios.items()
        ])

        saidas_df = pd.DataFrame([
            {"Tipo": "Saída", "Descrição/Usuário": descricao, "Valor (R$)": valor, "Data": data}
            for descricao, (valor, data) in saidas.items()
        ])

        dados_df = pd.concat([entradas_df, saidas_df], ignore_index=True)

        total_entradas = sum(valor for _, (valor, _) in usuarios.items())
        total_saidas = sum(valor for _, (valor, _) in saidas.items())
        saldo_final = total_entradas - total_saidas

        
        saldo_df = pd.DataFrame([{
            "Tipo": "Saldo Final",
            "Descrição/Usuário": "",
            "Valor (R$)": saldo_final,
            "Data": ""
        }])
        dados_df = pd.concat([dados_df, saldo_df], ignore_index=True)

        

        dados_df.to_excel("controle_financeiro.xlsx", index=False, engine="openpyxl")
        messagebox.showinfo("Sucesso", "Os dados foram exportados para 'controle_financeiro.xlsx'.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao exportar os dados: {e}")




def cadastrar_usuario():
    nome = entry_nome.get().strip()
    valor = entry_valor.get().replace(',', '.').strip()
    mes = combo_mes.get().zfill(2) 
    ano = combo_ano.get()
    data = f"{ano}-{mes}" 

    if nome and valor:
        try:
            valor = float(valor)
            usuarios[nome] = (valor, data)
            salvar_dados()
            entry_nome.delete(0, tk.END)
            entry_valor.delete(0, tk.END)
            combo_mes.set("")
            combo_ano.set("")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")
    else:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")


def registrar_saida():
    descricao = entry_descricao.get().strip()
    valor = entry_saida_valor.get().replace(',', '.').strip()
    mes = combo_saida_mes.get().zfill(2) 
    ano = combo_saida_ano.get()
    data = f"{ano}-{mes}" 

    if descricao and valor:
        try:
            valor = float(valor)
            saidas[descricao] = (valor, data)
            salvar_dados()
            entry_descricao.delete(0, tk.END)
            entry_saida_valor.delete(0, tk.END)
            combo_saida_mes.set("")
            combo_saida_ano.set("")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")
    else:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

def exibir_entradas_por_mes():
    mes = combo_mes.get().zfill(2) 
    ano = combo_ano.get() 
    data_filtro = f"{ano}-{mes}" 

    if not mes or not ano:
        messagebox.showerror("Erro", "Por favor, selecione o mês e o ano.")
        return

    

    entradas_window = tk.Toplevel(root)
    entradas_window.title(f"Entradas - {data_filtro}")

    
    tree = ttk.Treeview(entradas_window, columns=("Usuário", "Valor", "Data"), show="headings")
    tree.heading("Usuário", text="Usuário")
    tree.heading("Valor", text="Valor (R$)")
    tree.heading("Data", text="Data")
    tree.pack(fill=tk.BOTH, expand=True)

    total_entradas = 0
    for usuario, (valor, data) in usuarios.items():
        if data.startswith(data_filtro):  
            tree.insert("", tk.END, values=(usuario, f"{valor:.2f}", data))
            total_entradas += valor

    tk.Label(entradas_window, text=f"Total de Entradas: R$ {total_entradas:.2f}", font=("Arial", 12, "bold")).pack(pady=10)


def exibir_saidas_por_mes():
    mes = combo_saida_mes.get().zfill(2) 
    ano = combo_saida_ano.get() 
    data_filtro = f"{ano}-{mes}" 

    if not mes or not ano:
        messagebox.showerror("Erro", "Por favor, selecione o mês e o ano.")
        return

    

    saidas_window = tk.Toplevel(root)
    saidas_window.title(f"Saídas - {data_filtro}")

    

    tree = ttk.Treeview(saidas_window, columns=("Descrição", "Valor", "Data"), show="headings")
    tree.heading("Descrição", text="Descrição")
    tree.heading("Valor", text="Valor (R$)")
    tree.heading("Data", text="Data")
    tree.pack(fill=tk.BOTH, expand=True)

    total_saidas = 0
    for descricao, (valor, data) in saidas.items():
        if data.startswith(data_filtro): 
            tree.insert("", tk.END, values=(descricao, f"{valor:.2f}", data))
            total_saidas += valor

    tk.Label(saidas_window, text=f"Total de Saídas: R$ {total_saidas:.2f}", font=("Arial", 12, "bold")).pack(pady=10)



def exibir_saldo_por_mes():
    mes = combo_mes.get().zfill(2) 
    ano = combo_ano.get() 
    data_filtro = f"{ano}-{mes}" 

    if not mes or not ano:
        messagebox.showerror("Erro", "Por favor, selecione o mês e o ano.")
        return

    saldo_window = tk.Toplevel(root)
    saldo_window.title(f"Saldo - {data_filtro}")

    total_entradas = sum(valor for usuario, (valor, data) in usuarios.items() if data.startswith(data_filtro))
    total_saidas = sum(valor for descricao, (valor, data) in saidas.items() if data.startswith(data_filtro))
    saldo_final = total_entradas - total_saidas

    tk.Label(saldo_window, text=f"Total de Entradas: R$ {total_entradas:.2f}\n"
                                f"Total de Saídas: R$ {total_saidas:.2f}\n"
                                f"Saldo Final: R$ {saldo_final:.2f}",
             font=("Arial", 12, "bold")).pack(pady=20)




carregar_dados()

root = tk.Tk()
root.title("Controle Financeiro")



frame_cadastro = tk.Frame(root)
frame_cadastro.pack(pady=10)

tk.Label(frame_cadastro, text="Nome do Usuário:").grid(row=0, column=0, padx=5, pady=5)
entry_nome = tk.Entry(frame_cadastro)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_cadastro, text="Valor de Entrada:").grid(row=1, column=0, padx=5, pady=5)
entry_valor = tk.Entry(frame_cadastro)
entry_valor.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_cadastro, text="Mês:").grid(row=2, column=0, padx=5, pady=5)
combo_mes = ttk.Combobox(frame_cadastro, values=[str(i) for i in range(1, 13)], state="readonly")
combo_mes.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_cadastro, text="Ano:").grid(row=3, column=0, padx=5, pady=5)
combo_ano = ttk.Combobox(frame_cadastro, values=[str(i) for i in range(2010, 2031)], state="readonly")
combo_ano.grid(row=3, column=1, padx=5, pady=5)

tk.Button(frame_cadastro, text="Cadastrar Usuário", command=cadastrar_usuario).grid(row=4, column=0, columnspan=2, pady=10)



frame_saidas = tk.Frame(root)
frame_saidas.pack(pady=10)

tk.Label(frame_saidas, text="Descrição da Saída:").grid(row=0, column=0, padx=5, pady=5)
entry_descricao = tk.Entry(frame_saidas)
entry_descricao.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_saidas, text="Valor da Saída:").grid(row=1, column=0, padx=5, pady=5)
entry_saida_valor = tk.Entry(frame_saidas)
entry_saida_valor.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_saidas, text="Mês:").grid(row=2, column=0, padx=5, pady=5)
combo_saida_mes = ttk.Combobox(frame_saidas, values=[str(i) for i in range(1, 13)], state="readonly")
combo_saida_mes.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_saidas, text="Ano:").grid(row=3, column=0, padx=5, pady=5)
combo_saida_ano = ttk.Combobox(frame_saidas, values=[str(i) for i in range(2010, 2031)], state="readonly")
combo_saida_ano.grid(row=3, column=1, padx=5, pady=5)

tk.Button(frame_saidas, text="Registrar Saída", command=registrar_saida).grid(row=4, column=0, columnspan=2, pady=10)



frame_mes = tk.Frame(root)
frame_mes.pack(pady=10)

tk.Button(frame_mes, text="Exibir Entradas", command=exibir_entradas_por_mes).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_mes, text="Exibir Saídas", command=exibir_saidas_por_mes).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_mes, text="Exibir Saldo", command=exibir_saldo_por_mes).grid(row=0, column=2, padx=5, pady=5)
tk.Button(frame_mes, text="Exportar para Excel", command=exportar_para_excel).grid(row=1, column=0, columnspan=3, pady=10)



root.mainloop()