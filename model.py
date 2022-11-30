from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Usuario(Base):
    __tablename__ = "Usuario"
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    email = Column(String(40), unique=True)
    senha = Column(String(80))


class Login():
    def __init__(self, nome: str, email: str):
        self.nome = nome
        self.email = email
    
    
    def __str__(self) -> str:
        return self.nome


class RedefinirSenha(Base):
    __tablename__ = "RedefinirSenha"
    id = Column(Integer, primary_key=True)
    token = Column(String(64))
    user = Column(Integer, ForeignKey('Usuario.id'))
    ativado = Column(Boolean())
