"""Dados em memória (sem banco de dados por enquanto): somem ao fechar o app.

Quando houver um banco, só este arquivo precisa mudar.
"""

import re

EMAIL_VALIDO = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
SENHA_MINIMA = 6

USUARIOS = {
    'demo@exemplo.com': {'nome': 'Usuário Demo', 'senha': '123456'},
    # Conta de teste pública (fictícia, só para entrar no app; nenhum e-mail é enviado)
    'teste.meupainel@gmail.com': {'nome': 'Usuário Teste', 'senha': 'teste123'},
}

# Usuários de teste pessoais ficam em usuarios_teste.py, que o Git ignora
# (nunca vão para o repositório). Formato: USUARIOS = {'email': {'nome': ..., 'senha': ...}}
try:
    from usuarios_teste import USUARIOS as _USUARIOS_TESTE
    USUARIOS.update(_USUARIOS_TESTE)
except ImportError:
    pass

MESES = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
         'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
VENDAS_MENSAIS = [28400, 31200, 29800, 35600, 38100, 36900,
                  41200, 43800, 40500, 46300, 48250, 0]
META_MENSAL = [30000, 30000, 32000, 34000, 36000, 38000,
               40000, 42000, 42000, 44000, 46000, 48000]

CATEGORIAS = [
    ('Caixas', 42),
    ('Bandejas', 23),
    ('Mini móveis', 18),
    ('Personalizados', 17),
]

CLIENTES = [
    {'nome': 'Ana Lima', 'email': 'ana.lima@gmail.com', 'cidade': 'Brasília', 'status': 'Ativo', 'total': 12480.0},
    {'nome': 'Bruno Souza', 'email': 'bruno@lojasouza.com.br', 'cidade': 'Goiânia', 'status': 'Ativo', 'total': 8930.5},
    {'nome': 'Carla Mendes', 'email': 'carla.m@hotmail.com', 'cidade': 'São Paulo', 'status': 'Inativo', 'total': 2150.0},
    {'nome': 'Diego Rocha', 'email': 'diego@rochadecor.com', 'cidade': 'Brasília', 'status': 'Ativo', 'total': 19870.9},
    {'nome': 'Elisa Prado', 'email': 'elisa.prado@gmail.com', 'cidade': 'Belo Horizonte', 'status': 'Ativo', 'total': 6420.0},
    {'nome': 'Fábio Nunes', 'email': 'fabio@artesnunes.com', 'cidade': 'Curitiba', 'status': 'Inativo', 'total': 980.0},
    {'nome': 'Gabriela Alves', 'email': 'gabi.alves@outlook.com', 'cidade': 'Rio de Janeiro', 'status': 'Ativo', 'total': 15300.0},
]

PEDIDOS_RECENTES = [
    ('#1048', 'Diego Rocha', 'Hoje, 10:42', 1890.0, 'Pago'),
    ('#1047', 'Ana Lima', 'Hoje, 09:15', 640.0, 'Em produção'),
    ('#1046', 'Gabriela Alves', 'Ontem', 2310.5, 'Pago'),
    ('#1045', 'Bruno Souza', 'Ontem', 455.0, 'Pendente'),
    ('#1044', 'Elisa Prado', '20/10', 1120.0, 'Enviado'),
]


def autenticar(email, senha):
    """Devolve o usuário se e-mail e senha conferem; senão None."""
    usuario = USUARIOS.get(email)
    if usuario and usuario['senha'] == senha:
        return {'nome': usuario['nome'], 'email': email}
    return None


def cadastrar_usuario(nome, email, senha):
    """Cadastra e devolve True; devolve False se o e-mail já existe."""
    if email in USUARIOS:
        return False
    USUARIOS[email] = {'nome': nome, 'senha': senha}
    return True


def moeda(valor):
    """Formata no padrão brasileiro: 1234.5 -> 'R$ 1.234,50'."""
    texto = f'{valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    return f'R$ {texto}'
