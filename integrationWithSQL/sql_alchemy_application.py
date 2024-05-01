""" Módulo para uso de SQLAlchemy """

import sqlalchemy as sql
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from sqlalchemy import select

Base = declarative_base()


class User(Base):
    """Class representa o usuario"""

    __tablename__ = "users"
    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(20))
    fullname = sql.Column(sql.String(50))
    emails = relationship(
        "EnderecoEmail", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"User (ID: {self.id}, Nome: {self.name}, Nome Completo: {self.fullname})"
        )


class EnderecoEmail(Base):
    """Class representa o endereço de e-mail"""

    __tablename__ = "endereco_email"
    id = sql.Column(sql.Integer, primary_key=True)
    email = sql.Column(sql.String(50), nullable=False)
    user_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="emails")

    def __repr__(self):
        return f"Endereço de e-mail (ID: {self.id}, E-mail: {self.email})"


# Conexão com o banco de dados
engine = create_engine("sqlite://")

# Criando as class como tabela no banco de dados
Base.metadata.create_all(engine)

# Inspeciona o banco de dados
insp = inspect(engine)

# print(insp.get_table_names())
# print(insp.default_schema_name)

with Session(engine) as session:
    juliana = User(
        name="juliana",
        fullname="Juliana Mascarenhas",
        emails=[EnderecoEmail(email="juliana.masc@gmail.com")],
    )

    sandy = User(
        name="sandy",
        fullname="Sandy Bastos",
        emails=[
            EnderecoEmail(email="sandy.bastos@gmail.com"),
            EnderecoEmail(email="sandy.ba@yahoo.com"),
        ],
    )

    patrick = User(
        name="patrick",
        fullname="Patrick Bastos",
        emails=[
            EnderecoEmail(email="patrick.bastos@gmail.com"),
            EnderecoEmail(email="patrick.bts@yahoo.com"),
        ],
    )

    # Adicionando os objetos no banco de dados
    session.add_all([juliana, sandy, patrick])
    session.commit()

stmt = select(User).where(User.name.in_(["juliana", "sandy"]))
print("Recuprando usuários a partir de condição de filtragem!")
for user in session.scalars(stmt):
    print(user)


stmt_EnderecoEmail = select(EnderecoEmail).where(EnderecoEmail.user_id.in_([2]))
print("\nRecuperando os endereços de e-mail dos usuários!")
for email in session.scalars(stmt_EnderecoEmail):
    print(email)

order = select(User).order_by(User.fullname)
print("\nRecuperando informacoes dos usuários!")
for result in session.scalars(order):
    print(result)


stmt_join = select(User.fullname, EnderecoEmail.email).join_from(EnderecoEmail, User)
# print("\nRecuperando informações dos usuários e seus endereços de e-mail!")
for result in session.scalars(stmt_join):
    print(result)


connection = engine.connect()
print("\nRecuperando informações dos usuários e seus endereços de e-mail!")
result = connection.execute(stmt_join).fetchall()
for row in result:
    print(row)
