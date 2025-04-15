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

def carregar_dados():
    try:
        with open('entradas.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if len(row) >= 3 and all(row):
                    usuarios[row[0]] = (float(row[1]), row[2])

        with open('saidas.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader