from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'alura'

app.config['SQLALCHEMY_DATABASE_URI'] = \
        '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
            SGBD = 'mysql+mysqlconnector',
            usuario = 'pbrazf',
            senha = 'qwe123po',
            servidor = 'localhost',
            database = 'jogoteca'
            )

# Instânciando o banco de dados para ORM
db = SQLAlchemy(app)

# MODELOS QUE VÃO FAZER A PONTE COM O BANCO DE DADOS ----------------
class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return '<Name %r>' % self.name
# -------------------------------------------------------------------

@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
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
    
    # Query para verificar se o jogo já existe no banco
    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash('Jogo já existente!')
        return redirect(url_for('index'))
    
    # Se não tem ainda, inclui no banco de dados
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    return redirect(url_for('index')) 

@app.route('/login')
def login():
    proxima = request.args.get('proxima', url_for('index'))  # Define 'index' como valor padrão
    return render_template('login.html', proxima=proxima)

# Rota de intermediação
@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first() # Procura pelo usuário no banco
    if usuario:
        if request.form['senha'] == usuario.senha:
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