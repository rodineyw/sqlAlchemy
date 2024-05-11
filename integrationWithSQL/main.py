""" Módulos para uso de SQLAlchemy """

from sqlalchemy.orm import sessionmaker
from models import engine, Cliente, Conta

Session = sessionmaker(bind=engine)
session = Session()

# Adicionar um novo cliente
novo_cliente = Cliente(nome="Rod", cpf="123.123.123-12", email="rod@example.com")
session.add(novo_cliente)
session.commit()

# Adicionando uma conta para o cliente
nova_conta = Conta(cliente_id=novo_cliente.cliente_id, saldo=1000.0, tipo="corrente")
session.add(nova_conta)
session.commit()

# Consultando clientes
clientes = session.query(Cliente).all()
for cliente in clientes:
    print(cliente.nome, cliente.cpf)
