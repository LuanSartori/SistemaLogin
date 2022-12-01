from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from dao import CONN

Base = declarative_base()


class Usuario(Base):
    __tablename__ = "Usuario"
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    email = Column(String(40), unique=True)
    senha = Column(String(80))


class RedefinirSenha(Base):
    __tablename__ = "RedefinirSenha"
    id = Column(Integer, primary_key=True)
    token = Column(String(64))
    user = Column(Integer, ForeignKey('Usuario.id'))
    ativado = Column(Boolean())


class Login():
    def __init__(self, nome: str, email: str):
        self.nome = nome
        self.email = email
    
    
    def __str__(self) -> str:
        return self.nome


if __name__ == '__main__':
    engine = create_engine(CONN, echo=False)
    Base.metadata.create_all(engine)
