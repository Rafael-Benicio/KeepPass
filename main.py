import PySimpleGUI as sg 
import sqlite3

MASTER_PASSWORD= '123456'

sg.theme('Dark Black')  # please make your windows colorful

layout = [
        [sg.InputText('', key='-SENHA-', background_color='white', text_color='black')],
        [sg.Text('                         ',key='worng', text_color='red', font=(12))],
        [sg.Button('Ok'),sg.Button('Cancele')]
    ]

window = sg.Window('PassWords!!', layout)

while True:
    event, values = window.read()
    if  event=='Cancele' or event == sg.WIN_CLOSED:
        print(event, "exiting")
        exit()
    if event =='Ok':
        pw = str(values['-SENHA-'])
        if pw ==MASTER_PASSWORD:
            break
        else:
            window['-SENHA-'].update(background_color='red')
            window['worng'].update('Senha errada')
            window['-SENHA-'].update(text_color='white')

windowLay = [
        [sg.Text("*****************************************", font=(14))],
        [sg.Text("i : inserir nova senha", font=(14))],
        [sg.Text("l : listar serviços salvos", font=(14))],
        [sg.Text("r : recuperar uma senha", font=(14))],
        [sg.Text("s : sair", font=(14))],
        [sg.Text("*****************************************", font=(14))],
        [sg.InputText('',font=(12),key='-INF-'),sg.Button('Ok')]
        ]

conn=sqlite3.connect('passwords.db')

cursor= conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    service TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
''')

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

def inserPassW():
    print('che')

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

window = sg.Window('PassWords!!', windowLay)

while True:
    event, values = window.read()
    if values['-INF-']=='s' or event == sg.WIN_CLOSED:
        print('Fecha App')
        exit()

    if values['-INF-']=='i':
        inserPassW()


conn.close()
        