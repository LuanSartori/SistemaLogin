from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Usuario, RedefinirSenha
from utils import ServerError
from sqlalchemy.exc import OperationalError, IntegrityError


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
        except OperationalError:
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
        except OperationalError:
            raise ServerError('Não foi possível acessar o servidor!')


    @staticmethod
    def fazer_cadastro(session, *usuarios: Usuario):
        try:
            session.add_all(usuarios)
            session.commit()
        except OperationalError:
            raise ServerError('Não foi possível acessar o servidor!')
        except IntegrityError:
            raise ValueError('RAISE', 'Já existe um usuário cadastrado com este email')


    @staticmethod
    def redefinir_senha(session, email_usuario: int, nova_senha: str):
        try:
            x = UsuarioDao.ler_dados(session, email=email_usuario)[0]
            x.senha = nova_senha
            session.commit()
        except OperationalError:
            raise ServerError('Não foi possível acessar o servidor!')
        except IndexError:
            raise ValueError('RAISE', 'Não há nenhum usuário cadastrado com este email!')


class RedefinirSenhaDao(BancoDados):
    @staticmethod
    def ler_dados(session, **kwargs) -> list:
        """
        Args:
            **kwargs: filtro para os dados
        Returns:
            list: Uma lista com instâncias de `Usuario` filtrada do banco de dados
        """
        try:
            return session.query(RedefinirSenha).filter_by(**kwargs).all()
        except OperationalError:
            raise ServerError('Não foi possível acessar o servidor!')
    

    @staticmethod
    def cadastrar_token(session, redefinir_senha: RedefinirSenha):
        """
        Cadastro no banco um token para o usuário redefinir sua senha. Múltiplos tokens podem ser usados
        """
        try:
            session.add(redefinir_senha)
            session.commit()
        except OperationalError:
            raise ServerError('Não foi possível acessar o servidor!')
        except IntegrityError:
            raise ValueError('RAISE', 'Erro ao cadastrar o token!')
    

    @staticmethod
    def marcar_ativado(session, token: str, usuario: Usuario, ativado: bool):
        """
        Depois de já criado o primeiro cadastro do usuário,
        altere seu estado para controlar quando o token já foi usado
        
        ---
        
        Args:
            token (str): token único usado para redefinir a senha
            usuario (Usuario): instância do usuário a qual pertence o token
            ativado (bool): True para token já usado. False para não
        """
        try:
            x = RedefinirSenhaDao.ler_dados(session, token=token, user=usuario.id)[0]
            x.ativado = ativado
            session.commit()
        except OperationalError:
            raise ServerError('Não foi possível acessar o servidor!')
        except IndexError:
            raise ValueError('RAISE', 'Não há nenhum usuário cadastrado com este email!')


if __name__ == '__main__':
    print(UsuarioDao.ler_dados(UsuarioDao.retorna_session(), id=0))
