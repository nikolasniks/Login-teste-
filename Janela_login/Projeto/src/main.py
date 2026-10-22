import sys
from pathlib import Path

import flet as ft

import marca
from autenticacao import LARGURA_MINIMA, TelaAutenticacao
from estilo import PRIMARIA, PRIMARIA_ESCURO, tema
from painel import Painel

# Caminho baseado na localização do arquivo, para rodar de qualquer pasta
PASTA_ASSETS = Path(__file__).resolve().parent.parent / 'assets'
RAIO_JANELA = 20
ALTURA_MINIMA = 560


def barra_titulo(page: ft.Page):
    """Barra de título própria (sem a logo do Flet): arrastar, minimizar, maximizar e fechar."""

    def botao(icone, dica, ao_clicar, cor_hover=None):
        # size_constraints zerado: sem isso o Flet força botões de 40px de altura
        return ft.IconButton(icone, icon_size=15, tooltip=dica, on_click=ao_clicar,
                             hover_color=cor_hover, width=38, height=24, padding=0,
                             size_constraints=ft.BoxConstraints(min_width=0, min_height=0),
                             style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)))

    def minimizar(_):
        page.window.minimized = True
        page.update()

    def maximizar(_):
        page.window.maximized = not page.window.maximized
        page.update()

    async def fechar(_):
        await page.window.close()

    return ft.Row(spacing=0, controls=[
        # A área vazia arrasta a janela; dois cliques maximizam
        ft.WindowDragArea(ft.Container(height=30), expand=True),
        ft.Container(padding=ft.Padding.only(right=8), content=ft.Row(spacing=2, controls=[
            botao(ft.Icons.REMOVE, 'Minimizar', minimizar),
            botao(ft.Icons.CROP_SQUARE, 'Maximizar', maximizar),
            botao(ft.Icons.CLOSE, 'Fechar', fechar, cor_hover=ft.Colors.with_opacity(0.85, ft.Colors.RED)),
        ])),
    ])


def alcas_redimensionar(page: ft.Page):
    """Bordas invisíveis que redimensionam a janela sem moldura nativa."""
    B, C = 6, 14   # espessura das bordas e tamanho dos cantos
    E, M = ft.WindowResizeEdge, ft.MouseCursor

    def alca(borda, cursor, **posicao):
        async def redimensionar(_):
            await page.window.start_resizing(borda)
        return ft.GestureDetector(mouse_cursor=cursor, on_pan_start=redimensionar,
                                  content=ft.Container(bgcolor=ft.Colors.TRANSPARENT), **posicao)

    return [
        alca(E.TOP, M.RESIZE_UP_DOWN, top=0, left=C, right=C, height=B),
        alca(E.BOTTOM, M.RESIZE_UP_DOWN, bottom=0, left=C, right=C, height=B),
        alca(E.LEFT, M.RESIZE_LEFT_RIGHT, left=0, top=C, bottom=C, width=B),
        alca(E.RIGHT, M.RESIZE_LEFT_RIGHT, right=0, top=C, bottom=C, width=B),
        alca(E.TOP_LEFT, M.RESIZE_UP_LEFT_DOWN_RIGHT, top=0, left=0, width=C, height=C),
        alca(E.BOTTOM_RIGHT, M.RESIZE_UP_LEFT_DOWN_RIGHT, bottom=0, right=0, width=C, height=C),
        alca(E.TOP_RIGHT, M.RESIZE_UP_RIGHT_DOWN_LEFT, top=0, right=0, width=C, height=C),
        alca(E.BOTTOM_LEFT, M.RESIZE_UP_RIGHT_DOWN_LEFT, bottom=0, left=0, width=C, height=C),
    ]


def main(page: ft.Page):
    page.title = marca.NOME_APP
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = tema(PRIMARIA)
    page.dark_theme = tema(PRIMARIA_ESCURO)

    area = ft.Container(expand=True)
    if page.web:
        page.add(ft.Container(height=12), area)
    else:
        page.window.icon = str(PASTA_ASSETS / 'icone.ico')
        page.window.title_bar_hidden = True
        # Abre no tamanho mínimo; o usuário aumenta ou maximiza se quiser
        page.window.min_width, page.window.min_height = LARGURA_MINIMA, ALTURA_MINIMA
        page.window.width, page.window.height = LARGURA_MINIMA, ALTURA_MINIMA

        # Janela transparente + moldura arredondada = cantos mais redondos
        # que os do Windows (que são fixos em ~8px)
        page.window.bgcolor = ft.Colors.TRANSPARENT
        page.bgcolor = ft.Colors.TRANSPARENT
        page.window.frameless = True   # tira o contorno fino que o Windows desenha
        moldura = ft.Container(
            left=0, top=0, right=0, bottom=0,
            bgcolor=ft.Colors.SURFACE, border_radius=RAIO_JANELA,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=ft.Column([barra_titulo(page), area], spacing=0, expand=True))

        def ao_evento_janela(e: ft.WindowEvent):
            # Maximizada, a janela ocupa a tela toda: cantos retos
            if e.type in (ft.WindowEventType.MAXIMIZE, ft.WindowEventType.UNMAXIMIZE):
                moldura.border_radius = 0 if e.type == ft.WindowEventType.MAXIMIZE else RAIO_JANELA
                moldura.update()

        page.window.on_event = ao_evento_janela
        page.add(ft.Stack([moldura, *alcas_redimensionar(page)], expand=True))
        page.run_task(page.window.center)

    def largura():
        return page.width or 1280

    def mostrar(tela):
        area.content = tela
        page.update()

    def definir_tema(escuro):
        page.theme_mode = ft.ThemeMode.DARK if escuro else ft.ThemeMode.LIGHT

    def entrar(usuario):
        mostrar(Painel(page, usuario, ao_sair=sair, definir_tema=definir_tema, largura=largura()))

    def sair():
        mostrar(TelaAutenticacao(ao_entrar=entrar))

    def ao_redimensionar(e: ft.PageResizeEvent):
        # Só o painel se adapta; o login tem largura mínima fixa
        if isinstance(area.content, Painel):
            area.content.ajustar(e.width)

    page.on_resize = ao_redimensionar
    sair()


if __name__ == '__main__':
    # python main.py --web 8550  -> abre no navegador em vez de janela
    if '--web' in sys.argv:
        porta = int(sys.argv[sys.argv.index('--web') + 1])
        ft.run(main, assets_dir=str(PASTA_ASSETS), view=ft.AppView.WEB_BROWSER, port=porta)
    else:
        ft.run(main, assets_dir=str(PASTA_ASSETS))
