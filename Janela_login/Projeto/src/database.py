# database.py

import sqlite3

# Função para criar a tabela de login
def criar_tabela_login():
    try:
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY,
                        nome TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        senha TEXT NOT NULL)''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("Erro ao criar a tabela de usuários:", e)


# Função para inserir um novo usuário no banco de dados
def inserir_usuario(nome, email, senha):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                   (nome, email, senha))
    conn.commit()
    conn.close()

# Função para verificar se um usuário existe no banco de dados
def verificar_usuario(email, senha):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email=? AND senha=?", (email, senha))
    usuario = cursor.fetchone()
    conn.close()
    return usuario