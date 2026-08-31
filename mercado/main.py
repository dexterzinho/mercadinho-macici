import json
import os
produtos = []
def controle_estoque():
    print('bem vindo ao sistema de controle de estoque.')
    escolher = int(input('''Digite a funcao que deseja usar:
                         [1]: Adicionar
                         [2]: Retirar
                         [3]: Ver estoque
                         [4]: Consultar '''))

def adicionar():
    while True:
        if os.path.exists('estoque.json'):
            try: