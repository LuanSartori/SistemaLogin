from model import Usuario, Login
from dao import UsuarioDao
from utils import *


class UsuarioController():
    @staticmethod
    def fazer_cadastro(nome: str, email: str, senha: str) -> True:
        session = UsuarioDao.retorna_session()

        if 2 >= len(nome) > 50:
            raise ValueError('RAISE', 'O nome deve ter entre 2 e 50 caracteres!')
        
        if not email_valido(email):
            raise ValueError('RAISE', 'Email inválido!')
        
        verifica_senha = senha_valida(senha)
        if verifica_senha != True:
            raise ValueError('RAISE', verifica_senha)
        senha = hash_senha(senha, decode=True)

        usuario = Usuario(nome=nome, email=email, senha=senha)
        UsuarioDao.fazer_cadastro(session, usuario)
        return True
    

    @staticmethod
    def fazer_login(email: str, senha: str) -> Login:
        session = UsuarioDao.retorna_session()

        if not email_valido(email):
            raise ValueError('RAISE', 'Email inválido!')

        usuario = UsuarioDao.ler_dados(session, email=email)
        if not usuario:
            raise ValueError('RAISE', 'Este email não está cadastrado!')
        usuario = usuario[0]
        
        if not comparar_senha(senha.encode('utf-8'), usuario.senha.encode('utf-8')):
            raise ValueError('RAISE', 'Senha incorreta!')
        
        return Login(usuario.nome, usuario.email)
    

    @staticmethod
    def esqueci_minha_senha(email: str):
        print(f'Link para redefinir sua senha enviado para o email {email}')

        # TODO: Sistema para enviar um email


    @staticmethod
    def redefinir_senha(email_usuario: str, nova_senha: str):
        session = UsuarioDao.retorna_session()

        verifica_senha = senha_valida(nova_senha)
        if verifica_senha != True:
            raise ValueError('RAISE', verifica_senha)
        nova_senha = hash_senha(nova_senha, decode=True)

        UsuarioDao.redefinir_senha(session, email_usuario, nova_senha)
        return True
