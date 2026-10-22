"""Estilo compartilhado entre o login e o painel."""

import flet as ft

# Paleta do app (para trocar a identidade visual, mude só estes valores e o marca.py)
PRIMARIA = '#7C3AED'          # botões, links e destaques no tema claro
PRIMARIA_ESCURO = '#A78BFA'   # primária no tema escuro (mais clara, para ter contraste)
DEGRADE = ['#7C3AED', '#4C1D95']   # cartão lateral do login
TEXTO_CARTAO = '#E9DDFF'      # texto secundário sobre o cartão
ACENTO_1 = '#06B6D4'          # card de pedidos
ACENTO_2 = '#F59E0B'          # card de ticket médio e linha da meta
ACENTO_3 = '#10B981'          # card de clientes ativos
CORES_GRAFICO = [PRIMARIA, ACENTO_1, ACENTO_2, ACENTO_3]
FUNDO_DICA = '#1F1B2E'        # fundo das dicas dos gráficos

# Fundo das telas no tema claro: um pouco mais escuro que o quase-branco padrão,
# para os cartões (mais claros) se destacarem de leve
FUNDO = '#EFEAF6'

RAIO_CAMPO = 16    # cantos de campos e botões
RAIO_CARTAO = 24   # cantos de cartões e diálogos
ANIMACAO_MS = 160  # duração das transições entre telas e páginas


def tema(primaria, fundo=None):
    """Tema do app: aplica a todas as telas os padrões da tela de login."""
    forma_botao = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=RAIO_CAMPO))
    return ft.Theme(
        color_scheme_seed=PRIMARIA,
        # A semente gera a paleta; o primary fixo mantém a cor exata da marca
        color_scheme=ft.ColorScheme(primary=primaria),
        # Fundo da página; mudar o "surface" do esquema bagunça as cores derivadas
        scaffold_bgcolor=fundo,
        filled_button_theme=ft.FilledButtonTheme(style=forma_botao),
        outlined_button_theme=ft.OutlinedButtonTheme(style=forma_botao),
        text_button_theme=ft.TextButtonTheme(style=forma_botao),
        dialog_theme=ft.DialogTheme(
            shape=ft.RoundedRectangleBorder(radius=RAIO_CARTAO),
            # Cor explícita: sem ela o título herda branco e some no fundo claro
            title_text_style=ft.TextStyle(size=22, weight=ft.FontWeight.BOLD,
                                          color=ft.Colors.ON_SURFACE)),
    )


def borda_campo(preenchido=True):
    """Borda arredondada dos campos de texto.

    Preenchido: sem contorno no estado normal (só o fundo), contorno da cor primária ao focar.
    """
    def contorno(lado=None):
        return ft.OutlineInputBorder(border_radius=RAIO_CAMPO, side=lado)

    if not preenchido:
        return contorno()
    return {
        ft.ControlState.DEFAULT: contorno(ft.BorderSide(0, ft.Colors.TRANSPARENT)),
        ft.ControlState.FOCUSED: contorno(ft.BorderSide(2, ft.Colors.PRIMARY)),
        ft.ControlState.ERROR: contorno(ft.BorderSide(1, ft.Colors.ERROR)),
    }


def campo(rotulo, icone, senha=False, **kwargs):
    """Campo de texto no padrão da tela de login: preenchido, com ícone à esquerda.

    O preenchimento usa o tom claro dos cartões, um pouco mais claro que o FUNDO,
    para o campo se destacar de leve sem contorno.
    """
    return ft.TextField(
        label=rotulo, prefix_icon=icone, password=senha, can_reveal_password=senha,
        filled=True, fill_color=ft.Colors.SURFACE_CONTAINER_LOW, border=borda_campo(),
        **kwargs)
