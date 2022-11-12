from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Usuario
from utils import ServerError


class BancoDados():
    @staticmethod
    def retorna_session():
        USUARIO = 'root'
        SENHA = ''
        HOST = 'localhost'
        BANCO = 'sistema_login'
        PORT = 3306
        CONN = f'mysql+pymysql://{USUARIO}:{SENHA}@{HOST}:{PORT}/{BANCO}'

        try:
            Session = sessionmaker(bind=create_engine(CONN, echo=False))
            return Session()
        except:
            raise ServerError('Não possível acessar o servidor!')


class UsuarioDao(BancoDados):
    @staticmethod
    def ler_dados(session, **kwargs) -> list:
        """
        Args:
            **kwargs: filtro para os dados
        Returns:
            list: Uma lista com instâncias de `Usuario` filtrada do banco de dados
        """
        try:
            return session.query(Usuario).filter_by(**kwargs).all()
        except:
            raise ServerError('Não foi possível acessar o servidor!')


    @staticmethod
    def fazer_cadastro(session, *usuarios: Usuario):
        try:
            session.add_all(*usuarios)
            session.commit()
        except:
            raise ServerError('Não foi possível acessar o servidor!')


    @staticmethod
    def redefinir_senha(session, email_usuario: int, nova_senha: str):
        try:
            x = UsuarioDao.ler_dados(session, email=email_usuario)[0]
            x.senha = nova_senha
            session.commit()
        except:
            raise ServerError('Não foi possível acessar o servidor!')


if __name__ == '__main__':
    print(UsuarioDao.ler_dados(UsuarioDao.retorna_session(), id=0))
