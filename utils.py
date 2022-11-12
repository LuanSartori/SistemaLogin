import re
import bcrypt


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
