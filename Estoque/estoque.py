import json
import os

# Nome do arquivo JSON que servirá como banco de dados
ARQUIVO_ESTOQUE = 'estoque.json'

def carregar_produtos():
    """Verifica se o arquivo existe e carrega os dados. Se não existir, cria um arquivo vazio."""
    if os.path.exists(ARQUIVO_ESTOQUE):
        with open(ARQUIVO_ESTOQUE, 'r', encoding='utf-8') as arquivo:
            try:
                return json.load(arquivo)
            except json.JSONDecodeError:
                return [] # Retorna lista vazia se o arquivo estiver corrompido ou em branco
    else:
        # Cria o arquivo inicial com uma lista vazia se ele não existir
        with open(ARQUIVO_ESTOQUE, 'w', encoding='utf-8') as arquivo:
            json.dump([], arquivo)
        return []

def cadastrar():
    print('--- Bem-vindo ao sistema de estoque ---')
    
    # 1. Carrega a lista atual de produtos do arquivo
    produtos = carregar_produtos()
    
    # 2. Coleta os dados do novo produto
    nome = input('Digite o nome do produto que você deseja cadastrar: ')
    try:
        quantidade = int(input('Digite a quantidade do produto: '))
    except ValueError:
        print("Erro: A quantidade deve ser um número válido.")
        return

    # 3. Adiciona o novo produto à lista existente
    produtos.append({'nome': nome, 'quantidade': quantidade})
    
    
    with open(ARQUIVO_ESTOQUE, 'w', encoding='utf-8') as arquivo:
        json.dump(produtos, arquivo, ensure_ascii=False, indent=4)
    
    print(f'Produto "{nome}" cadastrado com sucesso!')

cadastrar()
