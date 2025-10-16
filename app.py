#app.py
from decimal import Decimal
from models import create_session, Cliente, Produto, ItemPedido

DB_URL = "sqlite:///loja_jogos.db"
session = create_session(DB_URL)

def cadastrar_cliente():
    nome = input("Nome do cliente: ").strip()
    email = input("Email do cliente: ").strip()
    telefone = input("Telefone do cliente: ").strip() or None
    
    cliente = Cliente(nome=nome, email=email, telefone=telefone)
    session.add(cliente)
    session.commit()
    print(f"Cliente cadastrado: {cliente}")

def cadastrar_produto():
    nome_produto = input("Nome do produto: ").strip()
    preco = Decimal(input("Preço do produto (ex: 199.99): ")).replace(",", ".")
    estoque = int(input("Estoque: "))

    produto = Produto(nome_produto=nome_produto, preco=preco, estoque=estoque)
    session.add(produto)
    session.commit()
    print(f"Produto cadastrado: {nome_produto}")

def criar_pedido():
    cliente_id = int(input("Digite o ID do cliente: "))
    pedido = pedido(cliente_id=cliente_id)
    session.add(pedido)
    session.flush() #GARANTE O ID DO PEDIDO ANTES DE INSERIR ITENS

    print("Adicione itens (Enter em produto_id para finalizar).")
    while True:
        val = input("Produto ID (Enter para sair): ").strip()
        if not val:
            break 
        produto_id = int(val)
        quantidade = int(input("Quantidade: "))

        # BUSCAR PRODUTO PARA PEGAR PREÇO E VALIDAR O ESTOQUE
        produto = session.get(Produto, produto_id)
        if produto is None :
            print("Produto não encontrado.")
            continue 

        if produto.estoque < quantidade:
            print(f"Estoque insuficiente. Quantidade disponível: {produto.estoque}")

        #DEBITA DO ESTOQUE
        produto.estoque -= quantidade

        item = ItemPedido(
            pedido_id = pedido.id,
            produto_id = produto_id,
            quantidade = quantidade,
            preco_unit = produto.preco
        )
    session.add(item)

    session.commit()