import PySimpleGUI as sg 
import sqlite3

# MASTER_PASSWORD= '123456'

sg.theme('Dark Amber')  # please make your windows colorful

# layout = [
#         [sg.InputText('', key='-SENHA-', background_color='white', text_color='black',font=(14))],
#         [sg.Text('                         ',key='worng', text_color='red', font=(12))],
#         [sg.Button('Ok'),sg.Button('Cancele')]
#     ]

# window = sg.Window('PassWords!!', layout)

# while True:
#     event, values = window.read()
#     if  event=='Cancele' or event == sg.WIN_CLOSED:
#         print(event, "exiting")
#         exit()
#     if event =='Ok':
#         pw = str(values['-SENHA-'])
#         if pw ==MASTER_PASSWORD:
#             break
#         else:
#             window['-SENHA-'].update(background_color='red')
#             window['worng'].update('Senha errada')
#             window['-SENHA-'].update(text_color='white')

windowLay = [
        [sg.Text("*****************************************", font=(14))],
        [sg.Text("i : inserir nova senha", font=(16))],
        [sg.Text("l : listar serviços salvos", font=(16))],
        [sg.Text("r : recuperar uma senha", font=(16))],
        [sg.Text("s : sair", font=(14))],
        [sg.Text("*****************************************", font=(16))],
        [sg.InputText('',font=(12),key='-INF-', background_color='white',text_color='black'),sg.Button('Ok')]
        ]

# window.close()

conn=sqlite3.connect('passwords.db')

cursor= conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    service TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
''')

def get_pd():
    sg.theme('Dark Amber')
    lay2=[
        [sg.Text('Obter Senhas',font=(14))],
        [sg.Text('Nome do Serviço')],
        [sg.InputText('',key='-ser-',background_color='white',font=(14),text_color='black'),sg.Button('Ok')]
    ]
    win2 = sg.Window('Recuperar Senha', lay2)
    while True:
        event, values = win2.read()
        if event == sg.WIN_CLOSED:
            print('Close regiter window')
            break
        if event =='Ok':
            ser=values['-ser-']
            get_password(ser)
            break
    win2.close()

def get_password(service):
    cursor.execute(f'''
        SELECT username, password FROM users
        WHERE service = '{service}'    
    ''')
    arr=[]
    if cursor.rowcount ==0:
        print('*Serviço não cadastrado, use "l" para verificar os seus serviços')
    else:
        for user in cursor.fetchall():
            arr.append(user)
        get_show(arr,service)

def get_show(arr,ser):
    ar=arr
    lis=[]
    for tex in ar:
        lis.append([sg.Text('Usuário : '+tex[0]+'\nSenha : '+tex[1]+'\n',font=(14))])
    win3 = sg.Window('Senhas e Users de '+ser, lis).read()

def inserPassW():
    sg.theme('Dark Amber') 
    lay1=[
        [sg.Text('Inserir novo Password',font=(14))],
        [sg.Text('Nome do serviço')],
        [sg.InputText('',font=(14),key='-Serv-',background_color='white',text_color='black')],
        [sg.Text('Nome do usuário')],
        [sg.InputText('',font=(14),key='-User-',background_color='white',text_color='black')],
        [sg.Text('Senha')],
        [sg.InputText('',font=(14),key='-PW-',background_color='white',text_color='black')],
        [sg.Button('Registrar'),sg.Button('Cancelar')]
    ]
    win = sg.Window('Novo Serviço', lay1)

    while True:
        event, values = win.read()
        if event=='Cancelar' or event == sg.WIN_CLOSED:
            print('Close regiter window')
            break
        if event=='Registrar':
            serv=str(values['-Serv-'])
            use=str(values['-User-'])
            passW=str(values['-PW-'])
            insert_password(serv,use,passW)
            break
    win.close()

def insert_password(service, username,password):
    cursor.execute(f'''
        INSERT INTO users (service, username, password)
        VALUES ('{service}','{username}','{password}')
    ''')
    conn.commit()
    print('Registrou')

def show_services():
    cursor.execute('''SELECT service from users;''')
    arr=[]
    sg.theme('Dark Amber')

    for service in cursor.fetchall():
        arr.append(service[0])
    showS(arr)

def showS(arr):
    ar=arr
    lis=[]
    try:
        for tex in ar:
            lis.append([sg.Text(tex,font=(14))])
        win3 = sg.Window('PassWords!!', lis).read()
    except:
        sg.popup('ERRO!', 'Por favor, check se você faz algum registro! ', text)
        
window = sg.Window('PassWords!!', windowLay)

while True:
    event, values = window.read()
    if values['-INF-']=='s' or values['-INF-']=='S' or event == sg.WIN_CLOSED:
        print('Fecha App')
        exit()

    if values['-INF-']=='i' or values['-INF-']=='I':
        inserPassW()
        window['-INF-'].update('')
    if values['-INF-']=='r' or values['-INF-']=='R':
        get_pd()
        window['-INF-'].update('')
    if values['-INF-']=='l' or values['-INF-']=='L':
        show_services()
        window['-INF-'].update('')
        
conn.close()
        
