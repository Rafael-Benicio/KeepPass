import sqlite3

MASTER_PASSWORD= '123456'

senha= str(input('Insira sua senha master'))

if senha!=MASTER_PASSWORD:
    print('Senha invalida!')
    exit()

conn=sqlite3.connect('passwords.db')

cursor= conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    service TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
''')

def menu():
    print("*****************************************")
    print("i : inserir nova senha")
    print("l : listar serviços salvos")
    print("r : recuperar uma senha")
    print("s : sair")
    print("*****************************************")

def get_password(service):
    cursor.execute(f'''
        SELECT username, password FROM users
        WHERE service = '{service}'    
    ''')

    if cursor.rowcount ==0:
        print('*Serviço não cadastrado, use "l" para verificar os seus serviços')
    else:
        for user in cursor.fetchall():
            print(user)

def insert_password(service, username,password):
    cursor.execute(f'''
        INSERT INTO users (service, username, password)
        VALUES ('{service}','{username}','{password}')
    ''')
    conn.commit()

def show_services():
    cursor.execute('''SELECT service from users;''')
    for service in cursor.fetchall():
        print(service)    

def funcLiner(op):
    if op =='l':show_services()

    if op =='i':
        service=str(input('*Qual o nome do serviço? '))
        username=str(input('*Qual o nome do usuário? '))
        password=str(input('*Qual a senha?'))
        insert_password(service,username,password)

    if op =='r':
        service=str(input('*Qual o nome do serviço?'))
        get_password(service)

while True:
    menu()
    op=str(input('O que deseja fazer?'))
    if op not in ['l','i','r','s']:
        print('Opção não valida')
        continue
    if op =='s':
        break

    funcLiner(op)

conn.close()
        