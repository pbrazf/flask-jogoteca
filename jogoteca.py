from flask import Flask, render_template, request, redirect, session, flash, url_for


class Jogo: 
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('God of War', 'Rack n Slash', 'PS2')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'PS2')
lista = [jogo1, jogo2, jogo3]

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario('Pedro Braz', 'pbrazf', 'qwe123po')
usuario2 = Usuario('Beatriz Hiromi', 'bia', '051022')
usuario3 = Usuario('João Marcos', 'joao', '12345')
usuarios = {usuario1.nickname: usuario1, 
            usuario2.nickname: usuario2,
            usuario3.nickname: usuario3}

app = Flask(__name__)
app.secret_key = 'alura'

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

# Rota de intermediação 
@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for(index)) 

@app.route('/login')
@app.route('/login')
def login():
    proxima = request.args.get('proxima', url_for('index'))  # Define 'index' como valor padrão
    return render_template('login.html', proxima=proxima)

# Rota de intermediação
@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = usuarios.get(request.form['usuario'])  # Usa `get` para evitar KeyError
    if usuario and request.form['senha'] == usuario.senha:
        session['usuario_logado'] = usuario.nickname
        flash(f'{usuario.nickname} logado com sucesso!')
        proxima_pagina = request.form.get('proxima', url_for('index'))  # Garante que sempre tenha um destino válido
        return redirect(proxima_pagina)
    
    # Caso usuário não exista ou senha esteja incorreta
    flash('Usuário ou senha incorretos.')
    return redirect(url_for('login'))  # Redireciona para a página de login

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso.')
    return redirect(url_for('index'))

app.run(debug=True)