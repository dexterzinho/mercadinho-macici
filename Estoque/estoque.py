import json
import os

# Antes eu tava usando só 'estoque.json', mas isso faz o arquivo nascer em
# qualquer pasta que o script for executado (tipo, se alguém roda o programa
# de fora da pasta Estoque, o json aparece lá fora, solto). Pra resolver isso
# de vez, pego o caminho da própria pasta onde esse arquivo .py está e grudo
# o nome do json nela. Assim o banco de dados sempre mora dentro de Estoque,
# não importa de onde o script seja chamado.
PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_ESTOQUE = os.path.join(PASTA_ATUAL, 'estoque.json')


def carregar_produtos():
    """Lê o arquivo json e devolve a lista de produtos.
    Se o arquivo ainda não existe (primeira vez rodando), cria ele vazio.
    Se o arquivo existe mas tá corrompido/vazio, também devolve lista vazia
    em vez de quebrar o programa."""
    if os.path.exists(ARQUIVO_ESTOQUE):
        with open(ARQUIVO_ESTOQUE, 'r', encoding='utf-8') as arquivo:
            try:
                return json.load(arquivo)
            except json.JSONDecodeError:
                return []
    else:
        with open(ARQUIVO_ESTOQUE, 'w', encoding='utf-8') as arquivo:
            json.dump([], arquivo)
        return []


def salvar_produtos(produtos):
    """Escreve a lista de produtos no json. Separei isso numa função própria
    porque toda função que mexe no estoque precisa salvar depois, e não faz
    sentido repetir esse bloco em cada uma."""
    with open(ARQUIVO_ESTOQUE, 'w', encoding='utf-8') as arquivo:
        json.dump(produtos, arquivo, ensure_ascii=False, indent=4)


def gerar_novo_id(produtos):
    """Gera o próximo ID disponível. Pego o maior ID que já existe e somo 1,
    em vez de usar só o tamanho da lista - assim, mesmo removendo produtos
    no meio do caminho, nunca corre o risco de dois produtos ficarem com o
    mesmo ID."""
    if not produtos:
        return 1
    return max(produto['id'] for produto in produtos) + 1


def buscar_produto(produtos, nome):
    """Procura um produto pelo nome (ignorando maiúscula/minúscula) e
    devolve o dicionário dele. Se não achar, devolve None."""
    for produto in produtos:
        if produto['nome'].lower() == nome.lower():
            return produto
    return None


def buscar_produto_por_id(produtos, id_produto):
    """Mesma ideia da busca por nome, mas por ID. Uso isso principalmente
    na remoção, porque buscar por ID é bem mais seguro do que por nome -
    não tem erro de digitação nem ambiguidade entre produtos parecidos."""
    for produto in produtos:
        if produto['id'] == id_produto:
            return produto
    return None


def pedir_quantidade(mensagem):
    """Fica pedindo a quantidade até o usuário digitar um número inteiro
    válido e positivo. Antes o programa simplesmente cancelava a operação
    inteira se a pessoa errasse a digitação uma vez só, o que é chato -
    agora só pede de novo."""
    while True:
        entrada = input(mensagem)
        try:
            quantidade = int(entrada)
        except ValueError:
            print('Ops, isso não é um número válido. Tenta de novo.')
            continue

        if quantidade <= 0:
            print('A quantidade tem que ser maior que zero.')
            continue

        return quantidade


def pedir_preco(mensagem):
    """Mesma lógica da quantidade, só que pra preço - aceita casas decimais
    (o usuário pode digitar com ponto ou vírgula) e não deixa passar valor
    negativo ou zerado. O preço ainda não é usado em nenhum lugar do sistema,
    é só pra já deixar guardado pro caixa que vem depois."""
    while True:
        entrada = input(mensagem).replace(',', '.')
        try:
            preco = float(entrada)
        except ValueError:
            print('Ops, isso não é um valor válido. Tenta de novo (ex: 9.90).')
            continue

        if preco <= 0:
            print('O preço tem que ser maior que zero.')
            continue

        return round(preco, 2)


def pedir_id(mensagem):
    """Pede um ID e garante que seja um número inteiro antes de seguir."""
    while True:
        entrada = input(mensagem)
        try:
            return int(entrada)
        except ValueError:
            print('Isso não é um ID válido. O ID é sempre um número.')


def cadastrar():
    """Cadastra um produto novo no estoque. Se o produto já existir,
    não cria duplicado - só soma a quantidade no que já tem (mantendo
    o ID e o preço que já estavam salvos)."""
    produtos = carregar_produtos()

    nome = input('Digite o nome do produto que você deseja cadastrar: ').strip()
    if not nome:
        print('O nome do produto não pode ficar em branco.')
        return

    produto_existente = buscar_produto(produtos, nome)
    if produto_existente:
        print(f'O produto "{produto_existente["nome"]}" já existe no estoque (ID {produto_existente["id"]}).')
        quantidade = pedir_quantidade('Quantidade a somar no estoque existente: ')
        produto_existente['quantidade'] += quantidade
        salvar_produtos(produtos)
        print(f'Estoque de "{produto_existente["nome"]}" atualizado para {produto_existente["quantidade"]} unidades.')
        return

    quantidade = pedir_quantidade('Digite a quantidade do produto: ')
    preco = pedir_preco('Digite o preço do produto (R$): ')
    novo_produto = {
        'id': gerar_novo_id(produtos),
        'nome': nome,
        'quantidade': quantidade,
        'preco': preco,
    }
    produtos.append(novo_produto)
    salvar_produtos(produtos)
    print(f'Produto "{nome}" cadastrado com sucesso! (ID {novo_produto["id"]})')


def adicionar():
    """Adiciona quantidade a um produto que já existe no estoque.
    Se o produto não existir ainda, avisa e sugere usar o cadastro."""
    produtos = carregar_produtos()

    if not produtos:
        print('O estoque ainda está vazio. Cadastre um produto primeiro.')
        return

    nome = input('Nome do produto que vai receber mais unidades: ').strip()
    produto = buscar_produto(produtos, nome)

    if produto is None:
        print(f'Não encontrei "{nome}" no estoque. Use a opção de cadastro para criá-lo.')
        return

    quantidade = pedir_quantidade('Quantidade a adicionar: ')
    produto['quantidade'] += quantidade
    salvar_produtos(produtos)
    print(f'Pronto! "{produto["nome"]}" (ID {produto["id"]}) agora tem {produto["quantidade"]} unidades.')


def retirar():
    """Retira uma quantidade do estoque de um produto. Não deixa o
    estoque ficar negativo - se pedir mais do que tem, avisa e cancela."""
    produtos = carregar_produtos()

    if not produtos:
        print('O estoque ainda está vazio, não tem o que retirar.')
        return

    nome = input('Nome do produto que você quer retirar do estoque: ').strip()
    produto = buscar_produto(produtos, nome)

    if produto is None:
        print(f'Não encontrei "{nome}" no estoque.')
        return

    quantidade = pedir_quantidade(f'Quantidade a retirar (disponível: {produto["quantidade"]}): ')

    if quantidade > produto['quantidade']:
        print(f'Não dá pra retirar {quantidade} unidades, só tem {produto["quantidade"]} no estoque.')
        return

    produto['quantidade'] -= quantidade
    salvar_produtos(produtos)
    print(f'Retirado! "{produto["nome"]}" (ID {produto["id"]}) ficou com {produto["quantidade"]} unidades.')


def consultar_estoque():
    """Mostra todos os produtos cadastrados, com ID, quantidade e preço.
    O ID aparece aqui justamente pra facilitar quando for remover um
    produto depois."""
    produtos = carregar_produtos()

    if not produtos:
        print('O estoque está vazio no momento.')
        return

    print('\n--- Estoque atual ---')
    for produto in produtos:
        print(f'- ID {produto["id"]} | {produto["nome"]} | {produto["quantidade"]} unidade(s) | R$ {produto["preco"]:.2f}')
    print('---------------------\n')


def remover_produto():
    """Remove um produto inteiro do estoque. Agora a busca é por ID em vez
    de nome - fica bem mais seguro, sem risco de remover o produto errado
    por causa de nome parecido ou erro de digitação. Use a opção de
    consultar estoque pra ver o ID antes de remover."""
    produtos = carregar_produtos()

    if not produtos:
        print('O estoque está vazio, não tem produto pra remover.')
        return

    consultar_estoque()
    id_produto = pedir_id('Digite o ID do produto que você quer remover: ')
    produto = buscar_produto_por_id(produtos, id_produto)

    if produto is None:
        print(f'Não encontrei nenhum produto com o ID {id_produto}.')
        return

    confirmacao = input(f'Tem certeza que quer remover "{produto["nome"]}" (ID {produto["id"]})? (s/n): ').strip().lower()
    if confirmacao != 's':
        print('Remoção cancelada.')
        return

    produtos.remove(produto)
    salvar_produtos(produtos)
    print(f'Produto "{produto["nome"]}" removido do estoque.')


def exibir_menu():
    print('\n===== Sistema de Estoque =====')
    print('1 - Cadastrar novo produto')
    print('2 - Adicionar quantidade a um produto')
    print('3 - Retirar quantidade de um produto')
    print('4 - Consultar estoque')
    print('5 - Remover produto do cadastro')
    print('0 - Sair')


def main():
    print('--- Bem-vindo ao sistema de estoque ---')

    while True:
        exibir_menu()
        opcao = input('Escolha uma opção: ').strip()

        if opcao == '1':
            cadastrar()
        elif opcao == '2':
            adicionar()
        elif opcao == '3':
            retirar()
        elif opcao == '4':
            consultar_estoque()
        elif opcao == '5':
            remover_produto()
        elif opcao == '0':
            print('Até mais!')
            break
        else:
            print('Opção inválida, escolhe um número do menu.')


if __name__ == '__main__':
    main()
