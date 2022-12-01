# Sistema de Login

Um sistema para cadastro/login de usuários feito com Python e SQL que roda pelo prompt de comando com um banco de dados hospedado no localhost

## Demonstração 💻

Para iniciar basta iniciar o banco de dados e executar o arquivo `views.py`:

![Cadastro](imgs/cadastro.PNG)

---

Depois de fazer um cadastro é só fazer o login:

![Login](imgs/login.PNG)

---

Caso você erre a senha por 2 ou mais vezes o sistema irá perguntar se você não esqueceu a senha, caso você responda que sim ele irá perguntar o seu email e enviar um token único, que você deve retornar para o sistema para assim redefinir sua senha:

![Redefinir Senha](imgs/redefinir_senha.PNG)
![Email Redefinir Senha](imgs/email_redefinir_senha.PNG)

---

## Técnico

- Python 3.10.2
- Interface - Prompt de comando
- Bibliotecas: 📚

    - PyMySQL 1.0.2
    - SQLAlchemy 1.4.42
    - bcrypt 4.0.1

- Banco de dados hospedado com XAMPP 🖧

![Python](https://img.shields.io/badge/Python-306a99?style=for-the-badge&logo=python&logoColor=ffff00)
![MySQL](https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white)

---

## Como usar 📝

- Instale as bibliotecas
- Crie um banco de dados pelo XAMPP ou outro software
- Dentro do arquivo `dao.py` configure a string de conexão na linha 8 a 14
- Com a string de conexão configurada e o banco de dados já ligado execute o arquivo `model.py`para carregar as tabelas no banco de dados
- Agora já está tudo pronto e só executar a views.py
