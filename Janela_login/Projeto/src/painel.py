import flet as ft
import flet_charts as fch

import dados
import marca
from estilo import (ACENTO_1, ACENTO_2, ACENTO_3, CORES_GRAFICO, FUNDO_DICA, PRIMARIA,
                    RAIO_CAMPO, RAIO_CARTAO as RAIO, campo)

LARGURA_MENU_ABERTO = 1100   # abaixo disso o menu lateral mostra só ícones
LARGURA_COMPACTA = 900       # abaixo disso as páginas usam o layout compacto
ESTILO_DICA = ft.TextStyle(color=ft.Colors.WHITE, weight=ft.FontWeight.W_600, size=12)
STATUS_PEDIDO = {
    'Pago': ft.Colors.GREEN,
    'Enviado': ft.Colors.BLUE,
    'Em produção': ft.Colors.AMBER,
    'Pendente': ft.Colors.RED,
}


def cartao(content, padding=24, expand=False, col=None):
    return ft.Container(
        content=content, padding=padding, expand=expand, col=col,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW, border_radius=RAIO,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT))


def titulo_secao(texto, extra=None):
    return ft.Row([ft.Text(texto, size=16, weight=ft.FontWeight.W_600), *([extra] if extra else [])],
                  alignment=ft.MainAxisAlignment.SPACE_BETWEEN)


def etiqueta(texto, cor):
    return ft.Container(
        content=ft.Text(texto, size=12, weight=ft.FontWeight.W_600, color=cor),
        bgcolor=ft.Colors.with_opacity(0.12, cor), border_radius=20,
        padding=ft.Padding.symmetric(horizontal=10, vertical=4))


def cartao_indicador(titulo, valor, variacao, icone, cor):
    positivo = not variacao.startswith('-')
    return cartao(col={'xs': 12, 'sm': 6, 'xl': 3}, content=ft.Column(spacing=10, controls=[
        ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
            ft.Text(titulo, size=13, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Container(ft.Icon(icone, color=cor, size=20), padding=8, border_radius=12,
                         bgcolor=ft.Colors.with_opacity(0.12, cor)),
        ]),
        ft.Text(valor, size=26, weight=ft.FontWeight.BOLD),
        ft.Row(spacing=4, controls=[
            ft.Icon(ft.Icons.TRENDING_UP if positivo else ft.Icons.TRENDING_DOWN, size=16,
                    color=ft.Colors.GREEN if positivo else ft.Colors.RED),
            ft.Text(variacao, size=12, weight=ft.FontWeight.W_600,
                    color=ft.Colors.GREEN if positivo else ft.Colors.RED),
            ft.Text('vs. mês anterior', size=12, color=ft.Colors.ON_SURFACE_VARIANT),
        ]),
    ]))


def eixo_meses(passo=1):
    return fch.ChartAxis(label_size=28, labels=[
        fch.ChartAxisLabel(value=i, label=ft.Text(m, size=11, color=ft.Colors.ON_SURFACE_VARIANT))
        for i, m in enumerate(dados.MESES) if i % passo == 0])


def eixo_milhares():
    return fch.ChartAxis(label_size=44, labels=[
        fch.ChartAxisLabel(value=v, label=ft.Text(f'{v // 1000}k', size=11,
                                                  color=ft.Colors.ON_SURFACE_VARIANT))
        for v in range(0, 60001, 10000)])


def grade():
    return fch.ChartGridLines(interval=10000, color=ft.Colors.OUTLINE_VARIANT, dash_pattern=[4, 4])


# ---------------------------------------------------------------- Páginas

def pagina_inicio(painel):
    vendas = [v for v in dados.VENDAS_MENSAIS if v]
    atual, anterior = vendas[-1], vendas[-2]
    variacao = (atual - anterior) / anterior * 100
    ativos = sum(c['status'] == 'Ativo' for c in dados.CLIENTES)

    grafico_barras = fch.BarChart(
        expand=True, max_y=60000, interactive=True,
        tooltip=fch.BarChartTooltip(bgcolor=FUNDO_DICA, border_radius=8),
        left_axis=eixo_milhares(), bottom_axis=eixo_meses(2 if painel.compacto else 1),
        horizontal_grid_lines=grade(),
        groups=[fch.BarChartGroup(x=i, rods=[fch.BarChartRod(
            from_y=0, to_y=v, width=10 if painel.compacto else 18,
            color=ft.Colors.PRIMARY if i == len(vendas) - 1 else
            ft.Colors.with_opacity(0.45, ft.Colors.PRIMARY), border_radius=6,
            tooltip=fch.BarChartRodTooltip(dados.moeda(v), text_style=ESTILO_DICA))])
            for i, v in enumerate(dados.VENDAS_MENSAIS)])

    total_cat = sum(p for _, p in dados.CATEGORIAS)
    grafico_pizza = fch.PieChart(
        sections_space=3, center_space_radius=48, expand=True,
        sections=[fch.PieChartSection(
            value=p, radius=34, color=CORES_GRAFICO[i], title='')
            for i, (_, p) in enumerate(dados.CATEGORIAS)])
    legenda = ft.Column(spacing=8, controls=[
        ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
            ft.Row(spacing=8, controls=[
                ft.Container(width=10, height=10, border_radius=5, bgcolor=CORES_GRAFICO[i]),
                ft.Text(nome, size=13)]),
            ft.Text(f'{p / total_cat:.0%}', size=13, weight=ft.FontWeight.W_600)])
        for i, (nome, p) in enumerate(dados.CATEGORIAS)])

    def valor_e_status(valor, status):
        valor_txt = ft.Text(dados.moeda(valor), weight=ft.FontWeight.W_600)
        if painel.compacto:  # empilha para caber em telas estreitas
            return [ft.Column([valor_txt, etiqueta(status, STATUS_PEDIDO[status])], spacing=4,
                              horizontal_alignment=ft.CrossAxisAlignment.END)]
        return [valor_txt, ft.Container(etiqueta(status, STATUS_PEDIDO[status]), width=110,
                                        alignment=ft.Alignment.CENTER_RIGHT)]

    pedidos = ft.Column(spacing=0, controls=[
        ft.Container(
            padding=ft.Padding.symmetric(vertical=10),
            border=ft.Border.only(bottom=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT)),
            content=ft.Row(controls=[
                ft.CircleAvatar(content=ft.Text(cliente[0], weight=ft.FontWeight.BOLD),
                                radius=18, bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.PRIMARY), color=ft.Colors.PRIMARY),
                ft.Column(spacing=0, expand=True, controls=[
                    ft.Text(cliente, weight=ft.FontWeight.W_500, no_wrap=True,
                            overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Text(f'{numero} · {quando}', size=12, color=ft.Colors.ON_SURFACE_VARIANT)]),
                *valor_e_status(valor, status),
            ]))
        for numero, cliente, quando, valor, status in dados.PEDIDOS_RECENTES])

    return ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=20, controls=[
        ft.ResponsiveRow(spacing=20, run_spacing=20, controls=[
            cartao_indicador('Receita do mês', dados.moeda(atual), f'{variacao:+.1f}%'.replace('.', ','),
                             ft.Icons.PAYMENTS_OUTLINED, ft.Colors.PRIMARY),
            cartao_indicador('Pedidos', '312', '+8,2%', ft.Icons.SHOPPING_BAG_OUTLINED, ACENTO_1),
            cartao_indicador('Clientes ativos', str(ativos), '+2', ft.Icons.PEOPLE_OUTLINE, ACENTO_3),
            cartao_indicador('Ticket médio', dados.moeda(atual / 312), '-1,4%',
                             ft.Icons.RECEIPT_LONG_OUTLINED, ACENTO_2),
        ]),
        ft.ResponsiveRow(spacing=20, run_spacing=20, controls=[
            cartao(col={'xs': 12, 'lg': 8}, content=ft.Column(spacing=16, controls=[
                titulo_secao('Vendas por mês', etiqueta(str(2026), ft.Colors.PRIMARY)),
                ft.Container(grafico_barras, height=260)])),
            cartao(col={'xs': 12, 'lg': 4}, content=ft.Column(spacing=16, controls=[
                titulo_secao('Vendas por categoria'),
                ft.Container(grafico_pizza, height=170), legenda])),
        ]),
        cartao(ft.Column(spacing=8, controls=[
            titulo_secao('Últimos pedidos', ft.TextButton(
                'Ver clientes', icon=ft.Icons.ARROW_FORWARD, on_click=lambda _: painel.ir_para(1))),
            pedidos])),
    ])


def pagina_clientes(painel):
    busca = campo(None, ft.Icons.SEARCH, hint_text='Buscar por nome, e-mail ou cidade',
                  expand=True)
    contador = ft.Text(size=13, color=ft.Colors.ON_SURFACE_VARIANT)
    # No layout compacto, Cidade e Total comprado saem para a tabela caber na tela
    completo = not painel.compacto
    tabela = ft.DataTable(
        expand=True, heading_row_height=44, data_row_min_height=56, data_row_max_height=56,
        column_spacing=24 if completo else 12, horizontal_margin=16 if completo else 8,
        heading_text_style=ft.TextStyle(weight=ft.FontWeight.W_600, color=ft.Colors.ON_SURFACE_VARIANT),
        columns=[ft.DataColumn(ft.Text('Cliente')),
                 *([ft.DataColumn(ft.Text('Cidade'))] if completo else []),
                 ft.DataColumn(ft.Text('Status')),
                 *([ft.DataColumn(ft.Text('Total comprado'), numeric=True)] if completo else []),
                 ft.DataColumn(ft.Text(''))])
    vazio = ft.Container(
        visible=False, padding=40, alignment=ft.Alignment.CENTER,
        content=ft.Column(tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
            ft.Icon(ft.Icons.SEARCH_OFF, size=40, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Text('Nenhum cliente encontrado.', color=ft.Colors.ON_SURFACE_VARIANT)]))

    def atualizar(_=None, redesenhar=True):
        termo = (busca.value or '').strip().lower()
        filtrados = [c for c in dados.CLIENTES
                     if termo in f"{c['nome']} {c['email']} {c['cidade']}".lower()]
        tabela.rows = [ft.DataRow(cells=[
            ft.DataCell(ft.Row(spacing=12, controls=[
                ft.CircleAvatar(content=ft.Text(c['nome'][0], weight=ft.FontWeight.BOLD),
                                radius=16, bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.PRIMARY), color=ft.Colors.PRIMARY),
                ft.Column(spacing=0, alignment=ft.MainAxisAlignment.CENTER, controls=[
                    ft.Text(c['nome'], weight=ft.FontWeight.W_500),
                    ft.Text(c['email'], size=12, color=ft.Colors.ON_SURFACE_VARIANT)])])),
            *([ft.DataCell(ft.Text(c['cidade']))] if completo else []),
            ft.DataCell(etiqueta(c['status'], ft.Colors.GREEN if c['status'] == 'Ativo' else ft.Colors.GREY)),
            *([ft.DataCell(ft.Text(dados.moeda(c['total'])))] if completo else []),
            ft.DataCell(ft.IconButton(ft.Icons.DELETE_OUTLINE, tooltip='Remover',
                                      icon_color=ft.Colors.ON_SURFACE_VARIANT,
                                      on_click=lambda _, c=c: confirmar_remocao(c))),
        ]) for c in filtrados]
        vazio.visible = not filtrados
        tabela.visible = bool(filtrados)
        contador.value = f'{len(filtrados)} de {len(dados.CLIENTES)} clientes'
        if redesenhar:
            painel.page_ref.update()

    def confirmar_remocao(cliente):
        def remover(_):
            dados.CLIENTES.remove(cliente)
            painel.page_ref.pop_dialog()
            atualizar()
            painel.avisar(f"{cliente['nome']} foi removido.")

        painel.page_ref.show_dialog(ft.AlertDialog(
            title=ft.Text('Remover cliente?'),
            content=ft.Text(f"{cliente['nome']} será removido da lista."),
            actions=[ft.TextButton('Cancelar', on_click=lambda _: painel.page_ref.pop_dialog()),
                     ft.FilledButton('Remover', on_click=remover,
                                     style=ft.ButtonStyle(bgcolor=ft.Colors.ERROR))]))

    def novo_cliente(_):
        nome = campo('Nome', ft.Icons.PERSON_OUTLINE, autofocus=True,
                     capitalization=ft.TextCapitalization.WORDS)
        email = campo('E-mail', ft.Icons.MAIL_OUTLINE, keyboard_type=ft.KeyboardType.EMAIL)
        cidade = campo('Cidade', ft.Icons.LOCATION_CITY_OUTLINED)
        ativo = ft.Switch(label='Cliente ativo', value=True)

        def salvar(_):
            for c in (nome, email, cidade):
                c.error = None
            if len((nome.value or '').strip()) < 2:
                nome.error = 'Informe o nome.'
            elif not dados.EMAIL_VALIDO.match((email.value or '').strip()):
                email.error = 'Informe um e-mail válido.'
            elif not (cidade.value or '').strip():
                cidade.error = 'Informe a cidade.'
            else:
                dados.CLIENTES.insert(0, {
                    'nome': nome.value.strip(), 'email': email.value.strip(),
                    'cidade': cidade.value.strip(),
                    'status': 'Ativo' if ativo.value else 'Inativo', 'total': 0.0})
                painel.page_ref.pop_dialog()
                busca.value = ''
                atualizar()
                return painel.avisar(f'{nome.value.strip()} foi adicionado.')
            dialogo.update()

        for c in (nome, email, cidade):
            c.on_submit = salvar
        dialogo = ft.AlertDialog(
            title=ft.Text('Novo cliente'),
            content=ft.Column([nome, email, cidade, ativo], tight=True, spacing=14, width=380,
                              horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
            actions=[ft.TextButton('Cancelar', on_click=lambda _: painel.page_ref.pop_dialog()),
                     ft.FilledButton('Salvar', on_click=salvar)])
        painel.page_ref.show_dialog(dialogo)

    busca.on_change = atualizar
    atualizar(redesenhar=False)
    return ft.Column(expand=True, spacing=20, controls=[
        ft.Row(spacing=12, controls=[
            busca,
            # Mesma altura do campo de busca ao lado
            ft.FilledButton('Novo cliente' if completo else 'Novo', icon=ft.Icons.ADD, height=56,
                            on_click=novo_cliente),
        ]),
        cartao(padding=8, expand=True, content=ft.Column(expand=True, spacing=0, controls=[
            ft.Container(contador, padding=ft.Padding.only(left=16, top=8, bottom=4)),
            ft.Column([tabela, vazio], scroll=ft.ScrollMode.AUTO, expand=True,
                      horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
        ])),
    ])


def pagina_relatorios(painel):
    meses = [i for i, v in enumerate(dados.VENDAS_MENSAIS) if v]
    total = sum(dados.VENDAS_MENSAIS)
    batidas = sum(dados.VENDAS_MENSAIS[i] >= dados.META_MENSAL[i] for i in meses)
    melhor = max(meses, key=lambda i: dados.VENDAS_MENSAIS[i])

    def resumo(rotulo, valor, icone):
        return cartao(col={'xs': 12, 'md': 4}, content=ft.Row(spacing=14, controls=[
            ft.Container(ft.Icon(icone, color=ft.Colors.PRIMARY), padding=10, border_radius=RAIO_CAMPO,
                         bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.PRIMARY)),
            ft.Column(spacing=2, controls=[
                ft.Text(rotulo, size=13, color=ft.Colors.ON_SURFACE_VARIANT),
                ft.Text(valor, size=20, weight=ft.FontWeight.BOLD)])]))

    grafico = fch.LineChart(
        expand=True, min_y=0, max_y=60000, min_x=0, max_x=11, interactive=True,
        tooltip=fch.LineChartTooltip(bgcolor=FUNDO_DICA, border_radius=8),
        left_axis=eixo_milhares(), bottom_axis=eixo_meses(2 if painel.compacto else 1),
        horizontal_grid_lines=grade(),
        data_series=[
            fch.LineChartData(
                curved=True, stroke_width=3, color=ft.Colors.PRIMARY,
                below_line_bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.PRIMARY),
                points=[fch.LineChartDataPoint(i, dados.VENDAS_MENSAIS[i],
                                               tooltip=fch.LineChartDataPointTooltip(
                                                   f'Receita: {dados.moeda(dados.VENDAS_MENSAIS[i])}',
                                                   text_style=ESTILO_DICA))
                        for i in meses]),
            fch.LineChartData(
                stroke_width=2, color=ACENTO_2, dash_pattern=[6, 4],
                points=[fch.LineChartDataPoint(i, v, tooltip=fch.LineChartDataPointTooltip(
                                                   f'Meta: {dados.moeda(v)}', text_style=ESTILO_DICA))
                        for i, v in enumerate(dados.META_MENSAL)]),
        ])

    legenda = ft.Row(spacing=16, controls=[
        ft.Row(spacing=6, controls=[ft.Container(width=14, height=3, bgcolor=cor),
                                    ft.Text(t, size=12, color=ft.Colors.ON_SURFACE_VARIANT)])
        for t, cor in (('Receita', ft.Colors.PRIMARY), ('Meta', ACENTO_2))])

    return ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=20, controls=[
        ft.ResponsiveRow(spacing=20, run_spacing=20, controls=[
            resumo('Receita no ano', dados.moeda(total), ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED),
            resumo('Metas batidas', f'{batidas} de {len(meses)} meses', ft.Icons.FLAG_OUTLINED),
            resumo('Melhor mês', dados.MESES[melhor], ft.Icons.EMOJI_EVENTS_OUTLINED),
        ]),
        cartao(ft.Column(spacing=16, controls=[
            titulo_secao('Receita x meta', legenda),
            ft.Container(grafico, height=320)])),
    ])


def pagina_configuracoes(painel):
    escuro = ft.Switch(value=painel.page_ref.theme_mode == ft.ThemeMode.DARK,
                       on_change=lambda e: painel.definir_tema(e.control.value))

    def linha(icone, titulo, descricao, controle):
        return ft.Container(
            padding=ft.Padding.symmetric(vertical=12),
            content=ft.Row(spacing=16, controls=[
                ft.Icon(icone, color=ft.Colors.ON_SURFACE_VARIANT),
                ft.Column(spacing=0, expand=True, controls=[
                    ft.Text(titulo, weight=ft.FontWeight.W_500),
                    ft.Text(descricao, size=12, color=ft.Colors.ON_SURFACE_VARIANT)]),
                controle]))

    return ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=20, controls=[
        cartao(ft.Row(spacing=20, controls=[
            ft.CircleAvatar(content=ft.Text(painel.usuario['nome'][0], size=28,
                                            weight=ft.FontWeight.BOLD),
                            radius=36, bgcolor=PRIMARIA, color=ft.Colors.WHITE),
            ft.Column(spacing=2, expand=True, controls=[
                ft.Text(painel.usuario['nome'], size=20, weight=ft.FontWeight.BOLD),
                ft.Text(painel.usuario['email'], color=ft.Colors.ON_SURFACE_VARIANT)]),
        ])),
        cartao(ft.Column(spacing=0, controls=[
            titulo_secao('Preferências'),
            linha(ft.Icons.DARK_MODE_OUTLINED, 'Modo escuro',
                  'Alterna entre o tema claro e o escuro.', escuro),
            ft.Divider(height=1, color=ft.Colors.OUTLINE_VARIANT),
            linha(ft.Icons.LOGOUT, 'Sair da conta', 'Volta para a tela de login.',
                  ft.OutlinedButton('Sair', on_click=lambda _: painel.ao_sair())),
        ])),
    ])


# (nome, ícone, ícone selecionado, subtítulo, função que monta a página)
PAGINAS = [
    ('Início', ft.Icons.DASHBOARD_OUTLINED, ft.Icons.DASHBOARD,
     'Olá, {nome}! Aqui está o resumo do seu negócio.', pagina_inicio),
    ('Clientes', ft.Icons.PEOPLE_OUTLINE, ft.Icons.PEOPLE,
     'Busque, cadastre e gerencie seus clientes.', pagina_clientes),
    ('Relatórios', ft.Icons.INSERT_CHART_OUTLINED, ft.Icons.INSERT_CHART,
     'Acompanhe a receita do ano em relação à meta.', pagina_relatorios),
    ('Configurações', ft.Icons.SETTINGS_OUTLINED, ft.Icons.SETTINGS,
     'Seu perfil e as preferências do painel.', pagina_configuracoes),
]


# ---------------------------------------------------------------- Estrutura

class Painel(ft.Row):
    """Menu lateral + barra superior + área da página atual."""

    def __init__(self, page, usuario, ao_sair, definir_tema, largura):
        super().__init__(expand=True, spacing=0)
        self.page_ref = page
        self.usuario = usuario
        self.ao_sair = ao_sair
        self._definir_tema = definir_tema
        self.compacto = False

        self.topo_menu = ft.Container(padding=ft.Padding.only(top=8, bottom=24))
        self.botao_sair = ft.Container(padding=ft.Padding.only(top=24))
        self.menu = ft.NavigationRail(
            selected_index=0, min_extended_width=220, bgcolor=ft.Colors.TRANSPARENT,
            indicator_color=ft.Colors.with_opacity(0.15, ft.Colors.PRIMARY),
            indicator_shape=ft.RoundedRectangleBorder(radius=RAIO_CAMPO),
            leading=self.topo_menu, trailing=self.botao_sair,
            destinations=[ft.NavigationRailDestination(icon=i, selected_icon=s, label=n)
                          for n, i, s, _, _ in PAGINAS],
            on_change=lambda e: self.ir_para(e.control.selected_index))

        self.titulo = ft.Text(size=24, weight=ft.FontWeight.BOLD)
        self.subtitulo = ft.Text(color=ft.Colors.ON_SURFACE_VARIANT)
        self.botao_tema = ft.IconButton(on_click=lambda _: self.definir_tema(
            self.page_ref.theme_mode != ft.ThemeMode.DARK))
        self.area = ft.AnimatedSwitcher(
            content=ft.Container(), duration=200, expand=True,
            transition=ft.AnimatedSwitcherTransition.FADE)

        primeiro_nome = usuario['nome'].split()[0]
        # Menu lateral como cartão flutuante de cantos arredondados
        self.conteudo = ft.Container(
            expand=True, content=ft.Column(expand=True, spacing=24, controls=[
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                       vertical_alignment=ft.CrossAxisAlignment.START, controls=[
                           ft.Column(spacing=2, expand=True, controls=[self.titulo, self.subtitulo]),
                           ft.Row(spacing=8, controls=[
                               self.botao_tema,
                               ft.CircleAvatar(content=ft.Text(primeiro_nome[0],
                                                               weight=ft.FontWeight.BOLD),
                                               bgcolor=PRIMARIA, color=ft.Colors.WHITE,
                                               tooltip=usuario['email'])]),
                       ]),
                self.area,
            ]))
        self.controls = [
            ft.Container(self.menu, margin=ft.Margin.only(left=12, bottom=12),
                         padding=ft.Padding.symmetric(vertical=8, horizontal=4),
                         bgcolor=ft.Colors.SURFACE_CONTAINER_LOW, border_radius=RAIO,
                         border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT)),
            self.conteudo,
        ]
        self._atualizar_icone_tema()
        self.ajustar(largura, atualizar=False)
        self.ir_para(0, atualizar=False)

    def ajustar(self, largura, atualizar=True):
        """Adapta o layout à largura da janela; só redesenha ao cruzar um limite."""
        aberto = largura >= LARGURA_MENU_ABERTO
        compacto = largura < LARGURA_COMPACTA
        mudou_pagina = compacto != self.compacto
        self.compacto = compacto

        self.menu.extended = aberto
        icone = marca.icone_menu()
        # Com o menu fechado não há largura limite: uma Row aqui trava o desenho
        self.topo_menu.content = (ft.Row(tight=True, spacing=10, controls=[
            icone, marca.nome_menu()]) if aberto else icone)
        self.botao_sair.content = (
            ft.TextButton('Sair', icon=ft.Icons.LOGOUT, on_click=lambda _: self.ao_sair()) if aberto
            else ft.IconButton(ft.Icons.LOGOUT, tooltip='Sair', on_click=lambda _: self.ao_sair()))
        self.conteudo.padding = (ft.Padding.only(left=16, right=16, top=8, bottom=16) if compacto
                                 else ft.Padding.only(left=28, right=28, top=8, bottom=24))
        self.titulo.size = 20 if compacto else 24

        if mudou_pagina and self.menu.selected_index is not None and self.area.content.key:
            self.ir_para(self.menu.selected_index, atualizar=False)
        if atualizar:
            self.page_ref.update()

    def ir_para(self, indice, atualizar=True):
        nome, _, _, subtitulo, construir = PAGINAS[indice]
        self.menu.selected_index = indice
        self.titulo.value = nome
        self.subtitulo.value = subtitulo.format(nome=self.usuario['nome'].split()[0])
        self.area.content = ft.Container(construir(self), expand=True, key=nome)
        if atualizar:
            self.page_ref.update()

    def definir_tema(self, escuro):
        self._definir_tema(escuro)
        self._atualizar_icone_tema()
        self.page_ref.update()

    def _atualizar_icone_tema(self):
        escuro = self.page_ref.theme_mode == ft.ThemeMode.DARK
        self.botao_tema.icon = ft.Icons.LIGHT_MODE_OUTLINED if escuro else ft.Icons.DARK_MODE_OUTLINED
        self.botao_tema.tooltip = 'Tema claro' if escuro else 'Tema escuro'

    def avisar(self, texto):
        self.page_ref.show_dialog(ft.SnackBar(ft.Text(texto), behavior=ft.SnackBarBehavior.FLOATING,
                                          width=360))
