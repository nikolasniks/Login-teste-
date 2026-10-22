"""Identidade do app: nome, cartão lateral do login e marca do menu.

Junto com as cores do estilo.py, é tudo o que muda para personalizar o app.
"""

import flet as ft

from estilo import PRIMARIA, TEXTO_CARTAO

NOME_APP = 'Meu Painel'
FOTO_NO_FORMULARIO = None   # imagem acima de "Bem-vindo de volta"; None para não mostrar


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


def icone_menu():
    """Ícone no topo do menu lateral (aparece também com o menu fechado)."""
    return ft.Container(ft.Icon(ft.Icons.BOLT, color=ft.Colors.WHITE, size=20),
                        bgcolor=PRIMARIA, border_radius=12, padding=8)


def nome_menu():
    """Nome ao lado do ícone, com o menu aberto."""
    return ft.Text(NOME_APP, size=18, weight=ft.FontWeight.BOLD)
