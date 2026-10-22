import flet as ft

import marca


class TelaCarregamento(ft.Container):
    """Tela exibida entre o login e o painel: destaque da marca, progresso e saudação.

    O destaque e o tempo na tela vêm do marca.py (animacao_carregamento e
    TEMPO_CARREGAMENTO).
    """

    def __init__(self, usuario):
        partes = usuario['nome'].split()
        primeiro_nome = partes[0] if partes else usuario['nome']
        super().__init__(
            expand=True, alignment=ft.Alignment.CENTER,
            content=ft.Column(
                tight=True, spacing=14, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    marca.animacao_carregamento(),
                    ft.Text(marca.NOME_APP, size=24, weight=ft.FontWeight.BOLD),
                    ft.Container(height=6),
                    # Sem value: barra indeterminada (animação contínua)
                    ft.ProgressBar(width=220, bar_height=6, border_radius=3,
                                   bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
                    ft.Text(f'Preparando o painel de {primeiro_nome}…',
                            size=14, color=ft.Colors.ON_SURFACE_VARIANT),
                ]))
