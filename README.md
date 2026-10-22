# Login-teste-
simple code, with a login and registration screen, with a simple database, just to see how the project works

Aplicativo desktop em Python com tela de login e um painel (dashboard), feito com [Flet](https://flet.dev).

## Como abrir (Windows)

1. Baixe o projeto: botão verde **Code** → **Download ZIP**, e extraia a pasta
   (ou `git clone https://github.com/nikolasniks/Login-teste-.git`).
2. Dê dois cliques em **`Abrir app.bat`**.

Na primeira vez ele prepara o ambiente sozinho (1 ou 2 minutos, precisa de internet);
depois abre direto. Precisa do [Python 3.13](https://www.python.org/downloads/) ou do
[uv](https://docs.astral.sh/uv/) instalado.

Para entrar, use uma das contas de teste (ou crie uma em "Cadastre-se"):

| E-mail | Senha |
|---|---|
| `teste.meupainel@gmail.com` | `teste123` |
| `demo@exemplo.com` | `123456` |

## Funcionalidades

**Login**
- Login, cadastro e recuperação de senha em uma única janela, com "Voltar ao login"
- Validação dos campos (e-mail válido, senha mínima, confirmação de senha, e-mail já cadastrado)
- Mostrar/ocultar senha e envio com a tecla Enter
- Tela de carregamento entre o login e o painel

**Painel**
- Menu lateral com Início, Clientes, Relatórios e Configurações
- Início: indicadores, gráfico de vendas por mês, vendas por categoria e últimos pedidos
- Clientes: busca, cadastro e remoção de clientes
- Relatórios: receita x meta ao longo do ano
- Configurações: perfil, modo claro/escuro e sair

**Janela**
- Cantos arredondados, barra de título própria e troca de telas com fade
- Abre no tamanho mínimo (860×560) e se adapta quando aumentada

## Rodar pelo terminal

```bash
cd Janela_login/Projeto
pip install -r requirements.txt
python src/main.py
```

Para abrir no navegador em vez de janela: `python src/main.py --web 8550`.

Sem banco de dados por enquanto: usuários e clientes ficam em memória (`src/dados.py`) e somem ao fechar o app.
Usuários de teste pessoais podem ir em `src/usuarios_teste.py` (ignorado pelo Git), no formato
`USUARIOS = {'email': {'nome': 'Nome', 'senha': 'senha'}}`.

## Estrutura

```
Abrir app.bat            # abre o app com dois cliques
Janela_login/Projeto/
├── assets/
│   ├── icone.ico        # ícone da janela e da barra de tarefas
│   └── perfil.png       # imagem do cartão lateral do login
└── src/
    ├── main.py          # ponto de entrada: janela, tema e troca de telas
    ├── autenticacao.py  # telas de login, cadastro e recuperação de senha
    ├── carregamento.py  # tela de carregamento entre o login e o painel
    ├── painel.py        # painel com menu lateral e páginas
    ├── estilo.py        # paleta, tema, raio dos cantos e campo de texto padrão
    ├── marca.py         # nome do app, cartão do login, ícone e destaque do carregamento
    └── dados.py         # dados em memória (troque aqui quando houver banco)
```

## Personalizar a identidade visual

Para usar o app com outra marca, só dois arquivos mudam:

- `src/estilo.py`: as cores (primária, fundo, degradê do cartão, acentos e gráficos)
- `src/marca.py`: nome do app, conteúdo do cartão do login, ícone do menu e o destaque
  da tela de carregamento (pode ser uma animação própria)

Botões, campos e diálogos seguem o tema definido em `estilo.tema()`, então todas as telas mantêm o mesmo padrão.

## Layout responsivo

A janela tem largura mínima de 860px, para o cartão lateral do login nunca sumir.

| Largura da janela | Painel |
|---|---|
| 1100px ou mais | menu lateral aberto, layout completo |
| 900–1100px | menu só com ícones |
| 860–900px | menu só com ícones, layout compacto |

No layout compacto, a lista de clientes esconde Cidade e Total, os resumos dos relatórios
mostram o ícone acima do texto e o gráfico mostra os meses de dois em dois.
