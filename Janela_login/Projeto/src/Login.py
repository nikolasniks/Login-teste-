import PySimpleGUI as sg
from database import criar_tabela_login, inserir_usuario, verificar_usuario

# Função para criar a janela de login


def janela_login():
    sg.theme('DarkPurple')
    layout_1 = [
        [sg.Image(filename='Projeto/assets/perfil.png',
                  size=(258, 258), key='-IMAGE-')]
    ]

    layout_2 = [
        [sg.Text('GMAIL: '), sg.Input(key='-EMAIL-')],
        [sg.Text('SENHA:'), sg.Input(password_char='*', key='-SENHA-')],
        [sg.Button('Login'), sg.Button('Esqueci a Senha'),
         sg.Button('Cadastrar-se')]
    ]

    layout = [
        [sg.Column(layout_1, element_justification='center')],
        [sg.HorizontalSeparator()],
        [sg.Column(layout_2, element_justification='center')],
    ]
    return sg.Window('Login', layout=layout, finalize=True, size=(400, 400), element_justification='c')


def janela_cadastro():
    sg.theme('DarkPurple')
    layout_3 = [
        [sg.Text('NOME: '), sg.Input(key='-NOME-')],
        [sg.Text('GMAIL: '), sg.Input(key='-EMAIL-')],
        [sg.Text('SENHA:'), sg.Input(
            password_char='*', key='-SENHA_CADASTRO-')],
        [sg.Button('Concluir cadastro'), sg.Button('Cancelar')]
    ]
    return sg.Window('Cadastro', layout=layout_3, finalize=True, size=(300, 150), element_justification='c')


def janela_esqueci_senha():
    sg.theme('DarkPurple')
    layout_esqueci_senha = [
        [sg.Text('Por favor, insira seu e-mail para recuperar sua senha:')],
        [sg.Text('E-mail:'), sg.Input(key='-EMAIL-')],
        [sg.Button('Enviar'), sg.Button('Cancelar')]
    ]
    return sg.Window('Esqueci a Senha', layout=layout_esqueci_senha, finalize=True, element_justification='c')


def popup_enviado():
    sg.popup('Um e-mail com instruções foi enviado para o seu endereço de e-mail.',
             title='E-mail Enviado')


def popup_concluido():
    sg.popup('Cadastro concluído com sucesso!', title='Concluído')


def main():
    criar_tabela_login()

    janela1, janela2, janela_esqueci = janela_login(), None, None

    while True:
        window, event, values = sg.read_all_windows()

        if window == janela1 and event == sg.WIN_CLOSED:
            break
        if window == janela1 and event == 'Cadastrar-se':
            janela2 = janela_cadastro()
            janela1.hide()
        if window == janela2 and event == sg.WIN_CLOSED:
            janela2.close()
            janela1.un_hide()
        if window == janela1 and event == 'Esqueci a Senha':
            janela_esqueci = janela_esqueci_senha()
            janela1.hide()
        if window == janela_esqueci and event == sg.WIN_CLOSED:
            janela_esqueci.close()
            janela1.un_hide()
        if window == janela_esqueci and event == 'Enviar':
            popup_enviado()
            janela_esqueci.close()
            janela1.un_hide()
        if window == janela2 and event == 'Concluir cadastro':
            inserir_usuario(
                values['-NOME-'], values['-EMAIL-'], values['-SENHA_CADASTRO-'])
            popup_concluido()
        if window == janela1 and event == 'Login':
            email = values.get('-EMAIL-', '')
            senha = values.get('-SENHA-', '')
            usuario = verificar_usuario(email, senha)
            if usuario:
                sg.popup('Login bem-sucedido!', title='Sucesso')
            else:
                sg.popup('E-mail ou senha incorretos!', title='Erro')


if __name__ == "__main__":
    main()