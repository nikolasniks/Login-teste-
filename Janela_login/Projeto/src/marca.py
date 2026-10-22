"""Identidade do app: nome, cartão lateral do login e marca do menu.

Junto com as cores do estilo.py, é tudo o que muda para personalizar o app.
"""

import flet as ft

from estilo import PRIMARIA, TEXTO_CARTAO

NOME_APP = 'Meu Painel'
FOTO_NO_FORMULARIO = None   # imagem acima de "Bem-vindo de volta"; None para não mostrar
TEMPO_CARREGAMENTO = 1.0    # segundos na tela de carregamento entre o login e o painel


def conteudo_cartao():
    """Conteúdo do cartão lateral do login."""
    return [
        ft.Image(src='perfil.png', width=150, height=150),
        ft.Container(height=12),
        ft.Text('Sua conta,\nem um só lugar.', size=30, weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER),
        ft.Text('Entre ou crie seu cadastro para acessar o painel.',
                size=14, color=TEXTO_CARTAO, text_align=ft.TextAlign.CENTER),
    ]


def icone_menu(tamanho=20):
    """Ícone da marca: topo do menu lateral e, maior, a tela de carregamento."""
    return ft.Container(ft.Icon(ft.Icons.BOLT, color=ft.Colors.WHITE, size=tamanho),
                        bgcolor=PRIMARIA, border_radius=round(tamanho * 0.6),
                        padding=round(tamanho * 0.4))


def animacao_carregamento():
    """Destaque da tela de carregamento: aqui, o ícone parado (troque por uma animação)."""
    return icone_menu(tamanho=48)


def nome_menu():
    """Nome ao lado do ícone, com o menu aberto."""
    return ft.Text(NOME_APP, size=18, weight=ft.FontWeight.BOLD)
