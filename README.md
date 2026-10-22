# Login-teste-
simple code, with a login and registration screen, with a simple database, just to see how the project works

## Funcionalidades

- Login, cadastro e recuperação de senha em uma única janela
- Validação dos campos (e-mail válido, senha mínima, confirmação de senha, e-mail já cadastrado)
- Botão para mostrar/ocultar a senha e envio com a tecla Enter
- Modo claro e escuro (segue o tema do Windows ao abrir)
- Tela de boas-vindas após o login, com opção de sair

## Como rodar

```bash
cd Janela_login/Projeto
pip install -r requirements.txt
python src/Login.py
```

Sem banco de dados por enquanto: os usuários ficam em memória. Para testar, entre com `demo@exemplo.com` / `123456`.
