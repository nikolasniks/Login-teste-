import re
from pathlib import Path

import customtkinter as ctk
from PIL import Image

# Caminho baseado na localização do arquivo, para rodar de qualquer pasta
PASTA_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_PERFIL = PASTA_PROJETO / 'assets' / 'perfil.png'

# Usuários em memória (sem banco de dados por enquanto): somem ao fechar o app
USUARIOS = {
    'demo@exemplo.com': {'nome': 'Usuário Demo', 'senha': '123456'},
}

EMAIL_VALIDO = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
SENHA_MINIMA = 6

# Paleta (cor no tema claro, cor no tema escuro)
ROXO = ('#7C3AED', '#8B5CF6')
ROXO_HOVER = ('#6D28D9', '#7C3AED')
FUNDO = ('#F4F2FA', '#0F0D17')
CARTAO = ('#FFFFFF', '#1A1726')
BORDA = ('#E4E0F0', '#2D2840')
TEXTO = ('#1F1B2E', '#F3F0FF')
TEXTO_SUAVE = ('#6B6584', '#A59FBF')
ERRO = ('#DC2626', '#F87171')
SUCESSO = ('#059669', '#34D399')


class CampoTexto(ctk.CTkFrame):
    """Rótulo + campo de entrada, com botão de mostrar/ocultar para senhas."""

    def __init__(self, master, rotulo, placeholder='', senha=False):
        super().__init__(master, fg_color='transparent')
        self._senha = senha

        ctk.CTkLabel(self, text=rotulo, text_color=TEXTO_SUAVE,
                     font=ctk.CTkFont(size=12, weight='bold'),
                     anchor='w').pack(fill='x', pady=(0, 4))

        linha = ctk.CTkFrame(self, fg_color='transparent')
        linha.pack(fill='x')

        self.entrada = ctk.CTkEntry(
            linha, placeholder_text=placeholder, height=42, corner_radius=10,
            border_width=1, border_color=BORDA, fg_color=FUNDO,
            text_color=TEXTO, show='•' if senha else '')
        self.entrada.pack(side='left', fill='x', expand=True)

        if senha:
            self.botao_olho = ctk.CTkButton(
                linha, text='Mostrar', width=72, height=42, corner_radius=10,
                fg_color='transparent', hover_color=BORDA,
                text_color=TEXTO_SUAVE, command=self._alternar_visibilidade)
            self.botao_olho.pack(side='left', padx=(6, 0))

    def _alternar_visibilidade(self):
        oculto = self.entrada.cget('show') != ''
        self.entrada.configure(show='' if oculto else '•')
        self.botao_olho.configure(text='Ocultar' if oculto else 'Mostrar')

    def valor(self):
        return self.entrada.get() if self._senha else self.entrada.get().strip()

    def limpar(self):
        self.entrada.delete(0, 'end')
        if self._senha:
            self.entrada.configure(show='•')
            self.botao_olho.configure(text='Mostrar')

    def marcar_erro(self, erro=True):
        self.entrada.configure(border_color=ERRO if erro else BORDA)


class Tela(ctk.CTkFrame):
    """Base das telas do formulário: título, mensagem de status e utilidades."""

    def __init__(self, app, titulo, subtitulo):
        super().__init__(app.area_formulario, fg_color='transparent')
        self.app = app
        self.campos = []

        # Espaçador que fixa a largura do formulário
        ctk.CTkFrame(self, width=360, height=1, fg_color='transparent').pack()
        self.titulo = ctk.CTkLabel(self, text=titulo, text_color=TEXTO, anchor='w',
                                   font=ctk.CTkFont(size=26, weight='bold'))
        self.titulo.pack(fill='x')
        ctk.CTkLabel(self, text=subtitulo, text_color=TEXTO_SUAVE, anchor='w',
                     justify='left', wraplength=340,
                     font=ctk.CTkFont(size=13)).pack(fill='x', pady=(4, 18))

        self.mensagem = ctk.CTkLabel(self, text='', anchor='w', justify='left',
                                     wraplength=340, font=ctk.CTkFont(size=12))

    def adicionar_campo(self, *args, **kwargs):
        campo = CampoTexto(self, *args, **kwargs)
        campo.pack(fill='x', pady=(0, 10))
        campo.entrada.bind('<Return>', lambda _: self.enviar())
        campo.entrada.bind('<Key>', lambda _: campo.marcar_erro(False), add='+')
        self.campos.append(campo)
        return campo

    def botao_principal(self, texto):
        self.mensagem.pack(fill='x', pady=(0, 8))
        ctk.CTkButton(self, text=texto, height=44, corner_radius=10,
                      fg_color=ROXO, hover_color=ROXO_HOVER,
                      font=ctk.CTkFont(size=14, weight='bold'),
                      command=self.enviar).pack(fill='x', pady=(4, 0))

    def link(self, master, texto, comando):
        return ctk.CTkButton(master, text=texto, fg_color='transparent',
                             hover=False, text_color=ROXO, width=0, height=24,
                             font=ctk.CTkFont(size=12, weight='bold'),
                             command=comando)

    def rodape(self, pergunta, texto_link, comando):
        linha = ctk.CTkFrame(self, fg_color='transparent')
        linha.pack(pady=(18, 0))
        if pergunta:
            ctk.CTkLabel(linha, text=pergunta, text_color=TEXTO_SUAVE,
                         font=ctk.CTkFont(size=12)).pack(side='left', padx=(0, 4))
        self.link(linha, texto_link, comando).pack(side='left')

    def mostrar_mensagem(self, texto, sucesso=False):
        self.mensagem.configure(text=texto, text_color=SUCESSO if sucesso else ERRO)

    def erro(self, campo, texto):
        campo.marcar_erro()
        campo.entrada.focus_set()
        self.mostrar_mensagem(texto)

    def ao_exibir(self):
        self.mensagem.configure(text='')
        for campo in self.campos:
            campo.limpar()
            campo.marcar_erro(False)
        if self.campos:
            self.after(50, self.campos[0].entrada.focus_set)

    def enviar(self):
        pass


class TelaLogin(Tela):
    def __init__(self, app):
        super().__init__(app, 'Bem-vindo de volta',
                         'Entre com seu e-mail e senha para continuar.')
        self.email = self.adicionar_campo('E-MAIL', 'voce@gmail.com')
        self.senha = self.adicionar_campo('SENHA', 'Sua senha', senha=True)

        esqueci = ctk.CTkFrame(self, fg_color='transparent')
        esqueci.pack(fill='x', pady=(0, 6))
        self.link(esqueci, 'Esqueci a senha',
                  lambda: app.mostrar('recuperar')).pack(side='right')

        self.botao_principal('Entrar')
        self.rodape('Não tem uma conta?', 'Cadastre-se',
                    lambda: app.mostrar('cadastro'))

    def enviar(self):
        email, senha = self.email.valor(), self.senha.valor()
        if not email:
            return self.erro(self.email, 'Informe seu e-mail.')
        if not senha:
            return self.erro(self.senha, 'Informe sua senha.')

        usuario = USUARIOS.get(email)
        if not usuario or usuario['senha'] != senha:
            self.senha.limpar()
            return self.erro(self.senha, 'E-mail ou senha incorretos.')
        self.app.entrar(nome=usuario['nome'], email=email)

    def preencher_apos_cadastro(self, email):
        self.email.entrada.insert(0, email)
        self.after(60, self.senha.entrada.focus_set)
        self.mostrar_mensagem('Cadastro concluído! Agora é só entrar.', sucesso=True)


class TelaCadastro(Tela):
    def __init__(self, app):
        super().__init__(app, 'Criar conta', 'Leva menos de um minuto.')
        self.nome = self.adicionar_campo('NOME', 'Seu nome completo')
        self.email = self.adicionar_campo('E-MAIL', 'voce@gmail.com')
        self.senha = self.adicionar_campo(
            'SENHA', f'Mínimo de {SENHA_MINIMA} caracteres', senha=True)
        self.confirmar = self.adicionar_campo(
            'CONFIRMAR SENHA', 'Repita a senha', senha=True)

        self.botao_principal('Concluir cadastro')
        self.rodape('Já tem uma conta?', 'Entrar', lambda: app.mostrar('login'))

    def enviar(self):
        nome, email = self.nome.valor(), self.email.valor()
        senha, confirmar = self.senha.valor(), self.confirmar.valor()

        if len(nome) < 2:
            return self.erro(self.nome, 'Informe seu nome.')
        if not EMAIL_VALIDO.match(email):
            return self.erro(self.email, 'Informe um e-mail válido.')
        if len(senha) < SENHA_MINIMA:
            return self.erro(
                self.senha, f'A senha precisa ter pelo menos {SENHA_MINIMA} caracteres.')
        if senha != confirmar:
            return self.erro(self.confirmar, 'As senhas não coincidem.')

        if email in USUARIOS:
            return self.erro(self.email, 'Já existe uma conta com este e-mail.')
        USUARIOS[email] = {'nome': nome, 'senha': senha}

        self.app.mostrar('login')
        self.app.telas['login'].preencher_apos_cadastro(email)


class TelaRecuperar(Tela):
    def __init__(self, app):
        super().__init__(app, 'Recuperar senha',
                         'Digite o e-mail da sua conta e enviaremos as instruções.')
        self.email = self.adicionar_campo('E-MAIL', 'voce@gmail.com')
        self.botao_principal('Enviar instruções')
        self.rodape('', '← Voltar para o login', lambda: app.mostrar('login'))

    def enviar(self):
        email = self.email.valor()
        if not EMAIL_VALIDO.match(email):
            return self.erro(self.email, 'Informe um e-mail válido.')
        # O envio real de e-mail ainda não existe; a mensagem é a mesma
        # exista ou não a conta, para não revelar quem está cadastrado.
        self.email.limpar()
        self.mostrar_mensagem(
            f'Se {email} estiver cadastrado, você receberá um e-mail com as instruções.',
            sucesso=True)


class TelaInicio(Tela):
    def __init__(self, app):
        super().__init__(app, 'Olá!', 'Login realizado com sucesso.')

        cartao = ctk.CTkFrame(self, fg_color=FUNDO, corner_radius=12,
                              border_width=1, border_color=BORDA)
        cartao.pack(fill='x', pady=(0, 20))
        ctk.CTkLabel(cartao, text='CONECTADO COMO', text_color=TEXTO_SUAVE,
                     font=ctk.CTkFont(size=11, weight='bold'),
                     anchor='w').pack(fill='x', padx=16, pady=(14, 0))
        self.email = ctk.CTkLabel(cartao, text='', text_color=TEXTO, anchor='w',
                                  font=ctk.CTkFont(size=14))
        self.email.pack(fill='x', padx=16, pady=(2, 14))

        ctk.CTkButton(self, text='Sair', height=44, corner_radius=10,
                      fg_color='transparent', border_width=1,
                      border_color=BORDA, hover_color=BORDA, text_color=TEXTO,
                      font=ctk.CTkFont(size=14, weight='bold'),
                      command=lambda: app.mostrar('login')).pack(fill='x')

    def definir_usuario(self, nome, email):
        partes = nome.split()
        self.titulo.configure(text=f'Olá, {partes[0] if partes else nome}!')
        self.email.configure(text=email)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Login')
        self.geometry('920x620')
        self.minsize(800, 600)
        self.configure(fg_color=FUNDO)

        self.grid_columnconfigure(0, weight=5, uniform='col')
        self.grid_columnconfigure(1, weight=6, uniform='col')
        self.grid_rowconfigure(0, weight=1)

        self._montar_painel_lateral()

        cartao = ctk.CTkFrame(self, fg_color=CARTAO, corner_radius=0)
        cartao.grid(row=0, column=1, sticky='nsew')

        topo = ctk.CTkFrame(cartao, fg_color='transparent')
        topo.pack(fill='x', padx=24, pady=(18, 0))
        self.tema = ctk.CTkSwitch(topo, text='Modo escuro', text_color=TEXTO_SUAVE,
                                  progress_color=ROXO, command=self._alternar_tema)
        self.tema.pack(side='right')
        if ctk.get_appearance_mode() == 'Dark':
            self.tema.select()

        # pack com expand centraliza o formulário no espaço abaixo do topo
        self.area_formulario = ctk.CTkFrame(cartao, fg_color='transparent')
        self.area_formulario.pack(expand=True, pady=(0, 30))

        self.telas = {
            'login': TelaLogin(self),
            'cadastro': TelaCadastro(self),
            'recuperar': TelaRecuperar(self),
            'inicio': TelaInicio(self),
        }
        self.tela_atual = None
        self.mostrar('login')

    def _montar_painel_lateral(self):
        painel = ctk.CTkFrame(self, fg_color=ROXO, corner_radius=0)
        painel.grid(row=0, column=0, sticky='nsew')

        conteudo = ctk.CTkFrame(painel, fg_color='transparent')
        conteudo.place(relx=0.5, rely=0.5, anchor='center')

        if CAMINHO_PERFIL.exists():
            imagem = Image.open(CAMINHO_PERFIL)
            self._imagem_perfil = ctk.CTkImage(imagem, imagem, size=(140, 140))
            ctk.CTkLabel(conteudo, text='', image=self._imagem_perfil).pack(pady=(0, 24))

        ctk.CTkLabel(conteudo, text='Sua conta,\nem um só lugar.',
                     text_color='#FFFFFF', justify='center',
                     font=ctk.CTkFont(size=26, weight='bold')).pack()
        ctk.CTkLabel(conteudo, text='Entre ou crie seu cadastro para começar.',
                     text_color='#E9DDFF', font=ctk.CTkFont(size=13)).pack(pady=(10, 0))

    def _alternar_tema(self):
        ctk.set_appearance_mode('dark' if self.tema.get() else 'light')

    def mostrar(self, nome):
        if self.tela_atual:
            self.tela_atual.pack_forget()
        self.tela_atual = self.telas[nome]
        self.tela_atual.ao_exibir()
        self.tela_atual.pack(fill='both', expand=True)

    def entrar(self, nome, email):
        self.telas['inicio'].definir_usuario(nome, email)
        self.mostrar('inicio')


def main():
    ctk.set_appearance_mode('system')
    App().mainloop()


if __name__ == '__main__':
    main()
