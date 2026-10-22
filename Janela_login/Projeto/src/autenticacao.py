import flet as ft

import dados
import marca
from estilo import ANIMACAO_MS, DEGRADE, campo

# Menor largura em que o cartão lateral e o formulário cabem lado a lado;
# a janela não diminui além disso, então o cartão nunca some
LARGURA_MINIMA = 860


def link(texto, ao_clicar):
    return ft.TextButton(texto, on_click=ao_clicar)


def botao_principal(texto, ao_clicar):
    return ft.FilledButton(texto, on_click=ao_clicar, height=50, width=float('inf'))


class TelaAutenticacao(ft.Row):
    """Cartão lateral + formulário que alterna entre login, cadastro e recuperação."""

    def __init__(self, ao_entrar):
        super().__init__(expand=True, spacing=0)
        self.ao_entrar = ao_entrar
        self.formulario = ft.AnimatedSwitcher(
            content=self.form_login(), duration=ANIMACAO_MS, reverse_duration=ANIMACAO_MS,
            switch_in_curve=ft.AnimationCurve.EASE_OUT, switch_out_curve=ft.AnimationCurve.EASE_IN,
            transition=ft.AnimatedSwitcherTransition.FADE)
        # Cartão lateral flutuante de cantos arredondados
        self.lateral = ft.Container(
            expand=5, padding=40, alignment=ft.Alignment.CENTER,
            margin=ft.Margin.only(left=12, bottom=12), border_radius=28,
            gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT,
                colors=DEGRADE),
            content=ft.Column(
                tight=True, spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=marca.conteudo_cartao()))
        # Coluna com rolagem para o cadastro caber em janelas baixas
        self.area_formulario = ft.Container(
            expand=6, padding=24,
            content=ft.Column(
                expand=True, scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[ft.Container(width=380, content=self.formulario)]))
        self.controls = [self.lateral, self.area_formulario]

    def trocar(self, formulario):
        self.formulario.content = formulario
        self.formulario.update()

    def mensagem(self, texto, sucesso=False):
        return ft.Text(texto, size=13, visible=bool(texto),
                       color=ft.Colors.GREEN if sucesso else ft.Colors.ERROR)

    def botao_voltar(self):
        """Volta ao login; fica no topo do cadastro e da recuperação de senha."""
        return ft.Row([ft.TextButton('Voltar ao login', icon=ft.Icons.ARROW_BACK,
                                     on_click=lambda _: self.trocar(self.form_login()))])

    @staticmethod
    def cabecalho(titulo, subtitulo):
        return [
            ft.Text(titulo, size=28, weight=ft.FontWeight.BOLD),
            ft.Text(subtitulo, size=14, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Container(height=8),
        ]

    @staticmethod
    def limpar_erros(*campos):
        for c in campos:
            c.error = None

    # ---------- Login ----------
    def form_login(self, email='', aviso=''):
        email_campo = campo('E-mail', ft.Icons.MAIL_OUTLINE, value=email,
                            autofocus=not email, keyboard_type=ft.KeyboardType.EMAIL)
        senha_campo = campo('Senha', ft.Icons.LOCK_OUTLINE, senha=True, autofocus=bool(email))
        status = self.mensagem(aviso, sucesso=True)

        def entrar(_):
            self.limpar_erros(email_campo, senha_campo)
            status.visible = False
            email_v, senha_v = (email_campo.value or '').strip(), senha_campo.value or ''
            if not email_v:
                email_campo.error = 'Informe seu e-mail.'
            elif not senha_v:
                senha_campo.error = 'Informe sua senha.'
            else:
                usuario = dados.autenticar(email_v, senha_v)
                if usuario:
                    return self.ao_entrar(usuario)
                senha_campo.value = ''
                senha_campo.error = 'E-mail ou senha incorretos.'
            self.formulario.update()

        email_campo.on_submit = senha_campo.on_submit = entrar
        return ft.Column(
            key='login', tight=True, spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                *([ft.Container(ft.Image(src=marca.FOTO_NO_FORMULARIO, width=64, height=64),
                                alignment=ft.Alignment.CENTER_LEFT)]
                  if marca.FOTO_NO_FORMULARIO else []),
                *self.cabecalho('Bem-vindo de volta', 'Entre com seu e-mail e senha para continuar.'),
                email_campo, senha_campo,
                ft.Row([link('Esqueci a senha', lambda _: self.trocar(self.form_recuperar()))],
                       alignment=ft.MainAxisAlignment.END),
                status,
                botao_principal('Entrar', entrar),
                ft.Row([ft.Text('Não tem uma conta?', color=ft.Colors.ON_SURFACE_VARIANT),
                        link('Cadastre-se', lambda _: self.trocar(self.form_cadastro()))],
                       alignment=ft.MainAxisAlignment.CENTER, spacing=0),
                ft.Text('Demo: demo@exemplo.com / 123456', size=12,
                        color=ft.Colors.ON_SURFACE_VARIANT, text_align=ft.TextAlign.CENTER,
                        width=float('inf')),
            ])

    # ---------- Cadastro ----------
    def form_cadastro(self):
        nome = campo('Nome', ft.Icons.PERSON_OUTLINE, autofocus=True,
                     capitalization=ft.TextCapitalization.WORDS)
        email = campo('E-mail', ft.Icons.MAIL_OUTLINE, keyboard_type=ft.KeyboardType.EMAIL)
        senha = campo('Senha', ft.Icons.LOCK_OUTLINE, senha=True,
                      hint_text=f'Mínimo de {dados.SENHA_MINIMA} caracteres')
        confirmar = campo('Confirmar senha', ft.Icons.LOCK_OUTLINE, senha=True)

        def concluir(_):
            self.limpar_erros(nome, email, senha, confirmar)
            nome_v = (nome.value or '').strip()
            email_v = (email.value or '').strip()
            senha_v, confirmar_v = senha.value or '', confirmar.value or ''
            if len(nome_v) < 2:
                nome.error = 'Informe seu nome.'
            elif not dados.EMAIL_VALIDO.match(email_v):
                email.error = 'Informe um e-mail válido.'
            elif len(senha_v) < dados.SENHA_MINIMA:
                senha.error = f'A senha precisa ter pelo menos {dados.SENHA_MINIMA} caracteres.'
            elif senha_v != confirmar_v:
                confirmar.error = 'As senhas não coincidem.'
            elif not dados.cadastrar_usuario(nome_v, email_v, senha_v):
                email.error = 'Já existe uma conta com este e-mail.'
            else:
                return self.trocar(self.form_login(
                    email=email_v, aviso='Cadastro concluído! Agora é só entrar.'))
            self.formulario.update()

        for c in (nome, email, senha, confirmar):
            c.on_submit = concluir
        return ft.Column(
            # Espaçamento menor para o cadastro caber inteiro na janela mínima
            key='cadastro', tight=True, spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                self.botao_voltar(),
                *self.cabecalho('Criar conta', 'Leva menos de um minuto.'),
                nome, email, senha, confirmar,
                ft.Container(height=4),
                botao_principal('Concluir cadastro', concluir),
            ])

    # ---------- Recuperar senha ----------
    def form_recuperar(self):
        email = campo('E-mail', ft.Icons.MAIL_OUTLINE, autofocus=True,
                      keyboard_type=ft.KeyboardType.EMAIL)
        status = self.mensagem('', sucesso=True)

        def enviar(_):
            email.error = None
            email_v = (email.value or '').strip()
            if not dados.EMAIL_VALIDO.match(email_v):
                email.error = 'Informe um e-mail válido.'
                status.visible = False
            else:
                # O envio real de e-mail ainda não existe; a mensagem é a mesma
                # exista ou não a conta, para não revelar quem está cadastrado.
                email.value = ''
                status.value = (f'Se {email_v} estiver cadastrado, você receberá '
                                'um e-mail com as instruções.')
                status.visible = True
            self.formulario.update()

        email.on_submit = enviar
        return ft.Column(
            key='recuperar', tight=True, spacing=14,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                self.botao_voltar(),
                *self.cabecalho('Recuperar senha',
                                'Digite o e-mail da sua conta e enviaremos as instruções.'),
                email, status,
                botao_principal('Enviar instruções', enviar),
            ])
