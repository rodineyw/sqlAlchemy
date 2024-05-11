""" Módulos para uso de SQLAlchemy """

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Cliente(Base):
    """Classe para o cliente"""

    __tablename__ = "clientes"

    cliente_id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String, unique=True)
    email = Column(String)

    # Relação com a tabela Conta
    contas = relationship("Conta", back_populates="cliente")


class Conta(Base):
    """Classe para as contas"""

    __tablename__ = "contas"

    conta_id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("clientes.cliente_id"))
    saldo = Column(Float)
    tipo = Column(String)

    # Relação com a tabela Cliente
    cliente = relationship("Cliente", back_populates="contas")


# Configuração do banco de dados
engine = create_engine("sqlite:///banco_de_dados.db")
Base.metadata.create_all(engine)
