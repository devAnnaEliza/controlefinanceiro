import csv 
import openpyxl

usuarios = {}
saidas = {}

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

