""" Módulos para uso de SQLAlchemy """

from sqlalchemy.orm import sessionmaker
from models import engine, Cliente, Conta

Session = sessionmaker(bind=engine)
session = Session()

# Defirnir informações do cliente
NOME = "Jordan"
CPF = "56354986"
EMAIL = "jordan@gmail.com"


# Adicionar um novo cliente
cliente = session.query(Cliente).filter_by(nome=NOME, cpf=CPF, email=EMAIL).first()
if cliente:
    print("Um cliente com estas informações {nome. cpf, email} já existe.")
else:
    novo_cliente = Cliente(nome=NOME, cpf=CPF, email=EMAIL)
    session.add(novo_cliente)
    try:
        session.commit()
        print("Cliente adicionado com sucesso.")

        # Adicionando uma conta para o cliente recém-adicionado
        nova_conta = Conta(
            cliente_id=novo_cliente.cliente_id, saldo=1000.0, tipo="corrente"
        )
        session.add(nova_conta)
        session.commit()

    except ImportError as e:
        session.rollback()
        print(f"Erro ao adicionar cliente: {e}")


# Consultando clientes
clientes = session.query(Cliente).all()
for cliente in clientes:
    print(cliente.nome, cliente.cpf, cliente.email)
