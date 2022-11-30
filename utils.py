import re
import bcrypt
import smtplib
import email.message
from random import choice
import string


class ServerError(Exception):
    def __init__(self, *objects):
        pass


# --------------------------------------------------


def email_valido(email: str) -> bool:
    """
    Args:
        email (str): string
    Returns:
        True para um email válido. False para inválido
    """

    valida = re.compile(r'^[\w-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$')
    return False if not valida.match(email) else True


def senha_valida(senha: str) -> bool:
    """
    Recebe uma senha e verifica se:
        * A senha deve tem entre 8 e 20 caracteres;
        * A senha deve tem pelo menos uma letra maiúscula e minúscula;
        * A senha deve tem pelo menos um número;
        * A senha não tem espaços vazios
    
    ---

    Args:
        senha (str): string
    Returns:
        True: se a senha passar pelas verificações
        str: motivo do erro caso ela não passe
    """

    if len(senha) < 8 or len(senha) > 20:
        return 'A senha deve ter entre 8 e 20 caracteres!'
    elif not re.search('[a-z]', senha) or not re.search('[A-Z]', senha):
        return 'A senha deve ter pelo pelo menos uma letra maiúscula e minúscula!'
    elif not re.search('[0-9]', senha):
        return 'A senha deve ter pelo menos um número!'
    elif re.search('\s', senha):
        return 'A senha não deve ter espaços vazios!'
    else:
        return True


def hash_senha(senha: str, decode=False) -> str: 
    """
    Args:
        senha (str): string
        decode (bool): a senha deve retornar descodificada. default=False
    Returns:
        decode=False: senha codificada em `utf-8`
        decode=True: senha descodificada
    """

    pwd_bytes = senha.encode("utf-8") 
    salt = bcrypt.gensalt()
    senha = bcrypt.hashpw(pwd_bytes, salt)
    return senha.decode('utf-8') if decode else senha


def comparar_senha(senha_1: str, senha_2: str) -> bool:
    """Args:
        senha_1 (str): string codificada em `utf-8`
        senha_2 (str): senha em hash codificada em `utf-8`
    Returns:
        True se as duas senhas forem iguais, senão False
    """
    return bcrypt.checkpw(senha_1, senha_2)


def enviar_email(senha, de, para, assunto, corpo):  
    try:
        corpo_email = corpo

        msg = email.message.Message()
        msg['Subject'] = assunto # assunto
        msg['From'] = de # remetente
        msg['To'] = para # destinatário
        # print(msg)
        # print(msg['To'])
        password = senha
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email)

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        # Login Credentials for sending the mail
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        return True
    except:
        raise ValueError('RAISE', 'O email não pôde ser enviado!')


# --------------------------------------------------


def cor(**kwargs) -> str:
    formatacao = {
            None: '0', 'nenhuma': '0', 'negrito': '1',
            'sublinhado': '4', 'negativo': '7'
            }
    texto = {
        None: '', 'branco': '30', 'vermelho': '31',
        'verde': '32', 'amarelo': '33', 'azul': '34',
        'roxo': '35', 'ciano': '36', 'cinza': '37'
        }
    fundo = {
        None: '', 'branco': '40', 'vermelho': '41',
        'verde': '42', 'amarelo': '43', 'azul': '44',
        'roxo': '45', 'ciano': '46', 'cinza': '47'
        }
    if kwargs.get('limpa'):
        return '\033[m'
    return f'\033[{formatacao[kwargs.get("formatacao")]};{texto[kwargs.get("texto")]};{fundo[kwargs.get("fundo")]}m'.replace(';;m', 'm').replace(';m', 'm')


def titulo(txt: str, decorador: str='=', comprimento: int=None,
           recuo: int=4, justificar: bool=False, **kwargs):
    """
    Printa um título decorado na tela, no formato::

        ===========
            Olá
        ===========
    
    ---

    Args:
        txt (str): título a ser exibido
        decorador (str): símbolo que vai ficar em cima e abaixo do título. default= '='
        comprimento (int): comprimento do decorador. Caso não passado é o `len` do título. default=None
        recuo (int): espaço do título até o começo da linha. default=4
        justificar_recuo (bool): deixa o título no meio bem no meio do comprimento do decorador. default=False
        **kwargs: parâmetros para função `cor`
    """
    
    print(cor(**kwargs), end='')
    print(decorador * (comprimento if comprimento else len(txt) + recuo * 2))
    print((' ' * (comprimento // 2 - len(txt) // 2) + txt)) if justificar else print(' '*recuo + txt)
    print(decorador * (comprimento if comprimento else len(txt) + recuo * 2))
    print(cor(limpa=True))
