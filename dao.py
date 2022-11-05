from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Usuario


class BancoDados():
    @staticmethod
    def retorna_session():
        USUARIO = 'root'
        SENHA = ''
        HOST = 'localhost'
        BANCO = 'sistema_login'
        PORT = 3306
        CONN = f'mysql+pymysql://{USUARIO}:{SENHA}@{HOST}:{PORT}/{BANCO}'

        Session = sessionmaker(bind=create_engine(CONN, echo=False))
        return Session()


class UsuarioDao(BancoDados):
    @staticmethod
    def ler_dados(session, **kwargs) -> list:
        """
        Args:
            **kwargs: filtro para os dados
        Returns:
            list: Uma lista com instâncias de `Usuario` filtrada do banco de dados
        """
        return session.query(Usuario).filter_by(**kwargs).all()


    @staticmethod
    def fazer_cadastro(session, *usuarios: Usuario):
        session.add_all(usuarios)
        session.commit()


    @staticmethod
    def redefinir_senha(session, id_usuario: int, nova_senha: str):
        x = UsuarioDao.ler_dados(session, id=id_usuario)[0]
        x.senha = nova_senha
        session.commit()


if __name__ == '__main__':
    print(UsuarioDao.ler_dados(UsuarioDao.retorna_session(), id=0))
