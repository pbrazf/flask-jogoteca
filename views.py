from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Jogos, Usuarios
from helpers import recupera_imagem, deleta_arquivo, FormualarioJogo, FormularioUsuario
import time

@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Jogos', jogos=lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormualarioJogo()
    return render_template('novo.html', titulo='Novo Jogo', form=form)


# Rota de intermediação 
@app.route('/criar', methods=['POST',])
def criar():
    form = FormualarioJogo(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data
    
    # Query para verificar se o jogo já existe no banco
    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash('Jogo já existente!')
        return redirect(url_for('index'))
    
    # Se não tem ainda, inclui no banco de dados
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()
 
    # Pegando o arquivo de imagem do jogo
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(fr'{upload_path}/capa{jogo.id}-{timestamp}.jpg') # Salva as informações no caminho
    return redirect(url_for('index')) 


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    
    # Consulta com base no id do jogo clicado suas informações no BD
    jogo = Jogos.query.filter_by(id=id).first()
    form = FormualarioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console
    capa_jogo = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Jogo', id=id, capa_jogo=capa_jogo, form=form)


# Rota de intermediação 
@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormualarioJogo(request.form)
    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data
        
        # Altera o banco com as novas informações
        db.session.add(jogo)
        db.session.commit()

        # Pegando o arquivo de imagem do jogo
        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(jogo.id) # Função para apagar duplicados
        arquivo.save(fr'{upload_path}/capa{jogo.id}-{timestamp}.jpg') # Salva as informações no caminho
    
    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    
    # Apaga do banco de dados o id X
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo deletado com sucesso!')
    
    return redirect(url_for('index'))
        

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
    if usuario:
        if form.senha.data == usuario.senha:
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


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)
