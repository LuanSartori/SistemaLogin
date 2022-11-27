from model import Login
from controller import *
from utils import titulo, cor
from time import sleep


def cadastro():
    titulo('Faça seu cadastro aqui!', comprimento=100, justificar=True, texto='azul')
    while True:
        try:
            nome = str(input(f'{cor(texto="amarelo")}Nome: {cor(texto="verde")}')).strip()
            email = str(input(f'{cor(texto="amarelo")}Email: {cor(texto="verde")}')).strip()
            senha = str(input(f'{cor(texto="amarelo")}Senha: {cor(texto="verde")}')).strip()
            print(cor())

            UsuarioController.fazer_cadastro(nome, email, senha)
            titulo('Cadastro realizado com sucesso!', '-', texto='verde')
            sleep(3)
            break
        except TypeError:
            titulo('Dados inválidos!', '*', texto='vermelho')
            continue
        except ValueError as arg:
            if arg.args[0] == 'RAISE':
                erro = ''
                for i, e in enumerate(arg.args):
                    if i == 0:
                        continue
                    erro += str(e) + ' | '
                titulo(erro[:len(erro)-3], '*', texto='vermelho')
            else:
                titulo('Valor Inválido!', '*', texto='vermelho')
            continue
        except ServerError as arg:
            titulo(f'Erro de conexão com o servidor: {str(arg)}', '*', texto='vermelho')
            exit()
        except Exception as arg:
            titulo(f'ERRO: {str(arg)}', '*', texto='vermelho')
            exit()


def login():
    titulo(f'Seja bem-vindo ao {cor(formatacao="sublinhado")}Sistema de Login{cor(formatacao="nenhuma", texto="azul")}', comprimento=100, justificar=True, texto='azul')
    while True:
        match str(input('{}Você já tem cadastro?{} [{}S{}/{}N{}] '.format(
            cor(texto='amarelo'), cor(), cor(texto='verde'), cor(), cor(texto='vermelho'), cor()
        ))).upper().strip():
            case 'S':
                pass
            case 'N':
                print(f'{cor(texto="amarelo")}Vamos fazer agora!{cor()}\n')
                sleep(3)
                cadastro()
            case other:
                print()
                titulo('Resposta inválida!', '*', comprimento=40, justificar=True, texto='vermelho')
                continue
        print('\n')
        break
    
    titulo('Faça o seu login', comprimento=100, justificar=True, texto='azul')
    tentativas = 0
    while True:
        try:
            if tentativas >= 2:
                match str(input('{}Esqueceu sua senha?{} [{}S{}/{}N{}] '.format(
                    cor(texto='amarelo'), cor(), cor(texto='verde'), cor(), cor(texto='vermelho'), cor()
                ))).upper().strip():
                    case 'S':

                        # TODO: Email para redefinição de senha
                        
                        pass
                    case 'N':
                        continue
                    case other:
                        print()
                        titulo('Resposta inválida!', '*', comprimento=40, justificar=True, texto='vermelho')
                        continue
            email = str(input(f'{cor(texto="amarelo")}Email: {cor(texto="verde")}')).strip()
            senha = str(input(f'{cor(texto="amarelo")}Senha: {cor(texto="verde")}')).strip()
            print(cor())

            login = UsuarioController.fazer_login(email, senha)
            titulo('Logado com sucesso!', '-', texto='verde')
            return login
        except TypeError:
            titulo('Dados inválidos!', '*', texto='vermelho')
            continue
        except ValueError as arg:
            if arg.args[0] == 'RAISE':
                if arg.args[1] == 'Senha incorreta!':
                    tentativas += 1

                erro = ''
                for i, e in enumerate(arg.args):
                    if i == 0:
                        continue
                    erro += str(e) + ' | '
                titulo(erro[:len(erro)-3], '*', texto='vermelho')
            else:
                titulo('Valor Inválido!', '*', texto='vermelho')
            continue
        except ServerError as arg:
            titulo(f'Erro de conexão com o servidor: {str(arg)}', '*', texto='vermelho')
            exit()
        except Exception as arg:
            titulo(f'ERRO: {str(arg)}', '*', texto='vermelho')
            exit()
        

if __name__ == '__main__':
    login: Login = login()
