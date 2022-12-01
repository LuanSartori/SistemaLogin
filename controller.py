from model import Usuario, Login, RedefinirSenha
from dao import UsuarioDao, RedefinirSenhaDao
from utils import *
from hashlib import sha256
from datetime import datetime


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
        session = UsuarioDao.retorna_session()

        usuario = UsuarioDao.ler_dados(session, email=email)
        if len(usuario) == 0:
            raise ValueError('RAISE', 'Não existe um usuário com este email cadastrado!')
        usuario = usuario[0]
        
        # Gera um token para redefinir a senha e o salva no banco de dados
        token = sha256(f'{usuario.nome}{usuario.email}{datetime.now()}'.encode()).hexdigest()
        RedefinirSenhaDao.cadastrar_token(session, RedefinirSenha(token=token, user=usuario.id, ativado=False))

        assunto = 'Redefinição de Senha'

        corpo = f'''<p>Olá {usuario.nome},</p>
        <br>
        </p>Para redefinir a sua senha use este token: <b>{token}</b></p>'''

        remetente = 'sistema_login@gmail.com'
        senha = 'xxxxxxxxxxxxxxxx' # * Está senha é gerada nas configurações de segurança do email do remetente

        return enviar_email(senha, remetente, email, assunto, corpo)


    @staticmethod
    def redefinir_senha(token: str, email_usuario: str, nova_senha: str):
        session = UsuarioDao.retorna_session()

        redefinir_senha = RedefinirSenhaDao.ler_dados(session, token=token)[0]
        if redefinir_senha.ativado == True:
            raise ValueError('RAISE', 'Este token já foi usado!')
        usuario = UsuarioDao.ler_dados(session, id=redefinir_senha.user)[0]

        verifica_senha = senha_valida(nova_senha)
        if verifica_senha != True:
            raise ValueError('RAISE', verifica_senha)
        nova_senha = hash_senha(nova_senha, decode=True)

        UsuarioDao.redefinir_senha(session, email_usuario, nova_senha)
        RedefinirSenhaDao.marcar_ativado(session, token, usuario, True)
        return True
