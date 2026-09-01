import json
import os
from estoque import carregar_produtos, salvar_produtos, buscar_produto, buscar_produto_por_id, consultar_estoque

caminho = os.path.join(os.path.dirname(__file__), "estoque.json")

with open(caminho,'r',encoding='utf-8') as arquivo:
    estoque = json.load(arquivo)

'''Mostra os itens armazenados nos arrays do json'''
for produto in estoque:
    print(f" ID: {produto["id"]}\n Nome: {produto["nome"]}\n Quantidade: {produto["quantidade"]}\n Preço: {produto["preco"]}\n ------------")

'''Pede as coisas necessarias para o caixa como saldo, produto a ser comprado e quantidade(tambem verifica se quantidade é menor que 0 e apresenta erro)'''
carrinho = []
saldo = float(input("Digite seu saldo atual: R$ "))
print("--------------")

def pedir_Id_Quantidade(): 
    while True:
        try:
            id_produto = int(input("Digite o id do produto que sera comprado ->"))
            print("--------------------")
            quantidade_compra = int(input("Digite a quantidade do produto que sera comprado ->"))
            print("--------------------")

            if quantidade_compra <= 0:
                print("A quantidade deve ser maior que zero!")
                continue

            carrinho.append({
                "id": id_produto,
                "quantidade": quantidade_compra
            })

            continuar = input("Deseja adicionar outro produto? (s/n):").lower()
            print("--------------------")
            if continuar == "n":
                break
        except ValueError:
                print("ID e quantidade devem ser numeros!")
    return carrinho

'''Função para retirar quantidade comprada do estoque'''
def retirar_produtos(carrinho, estoque):

    for item in carrinho:

        id_produto = item["id"]
        quantidade_prouto = item["quantidade"]

        for produto in estoque:
            if produto["id"] == id_produto:
                if quantidade_prouto <= produto["quantidade"]:
                    produto["quantidade"] -= quantidade_prouto

                    print(
                        f"{quantidade_prouto}x {produto["nome"] }"
                        f"Retirado do estoque"
                    )

                else:
                    print(
                        f"Estoque inisuficiente para {produto["nome"]}!"
                    )

                break

        else:
            print(f"Produto com ID {id_produto} não encontrado.")

'''Calcula o valor total da compra'''

def verificar_estoque(carrinho, estoque):

    for item in carrinho:

        id_produto = item["id"]
        quantidade_compra = item["quantidade"]

        for produto in estoque:

            if produto["id"] == id_produto:

                if quantidade_compra > produto["quantidade"]:
                    print(
                        f"Estoque insuficiente para "
                        f"{produto['nome']}!"
                    )
                    return False

                break

        else:
            print(f"Produto com ID {id_produto} não encontrado!")
            return False

    return True

def calcular_total(carrinho, estoque):

    total = 0

    for item in carrinho:

        id_produto = item["id"]
        quantidade = item["quantidade"]

        for produto in estoque:

            if produto["id"] == id_produto:
                subtotal = quantidade * produto["preco"]

                total += subtotal

                print(
                    f"{produto["nome"]}; "
                    f"{quantidade}x R$ {produto["preco"]:.2f} "
                    f"= R$ {subtotal:.2f}"
                )

                break

    return total
'''finaliza a compra mostrando produtos e quantidades retiradas do estoque. Mostrando tambem seu saldo final e troco'''
carrinho = pedir_Id_Quantidade()

retirar_produtos(carrinho, estoque)

total = calcular_total(carrinho, estoque)

if saldo >= total:
    troco = saldo - total

    print("-------------------------")
    print(f"TOTAL: R${total:.2f}")
    print(f"TROCO: R${troco:.2f}")
else:
    print("Saldo insuficiente!")
    print(f"Faltam R$ {total - saldo:.2f}")


with open("Estoque/estoque.json", "w", encoding="utf-8") as arquivo:
    json.dump(estoque, arquivo,indent=4, ensure_ascii=False)