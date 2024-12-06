from jogoteca import app
from flask import render_template, request, redirect, session, flash, url_for
from models import Usuarios
from helpers import FormularioUsuario
from flask_bcrypt import check_password_hash

@app.route('/login')
def login():
    proxima = request.args.get('proxima', url_for('index'))  # Define 'index' como valor padrão
    form = FormularioUsuario()
    return render_template('login.html', proxima=proxima, form=form)

# Rota de intermediação
@app.route('/autenticar', methods=['POST'])
def autenticar():
    form = FormularioUsuario(request.form)

    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first() # Procura pelo usuário no banco
    senha = check_password_hash(usuario.senha, form.senha.data) # Devolve um Booleano indicando se a senha está correta ou não
    if usuario and senha:
        session['usuario_logado'] = usuario.nickname
        flash(f'{usuario.nickname} logado com sucesso!')
        proxima_pagina = request.form.get('proxima', url_for('index'))  # Garante que sempre tenha um destino válido
        return redirect(proxima_pagina)

    # Caso usuário não exista ou senha esteja incorreta
    flash('Usuário não logado.')
    return redirect(url_for('login'))  # Redireciona para a página de login

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso.')
    return redirect(url_for('index'))
