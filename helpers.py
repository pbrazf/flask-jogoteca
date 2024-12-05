from jogoteca import app 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
import os

# Classe para representar o formulário de novo jogo
class FormualarioJogo(FlaskForm):
    nome = StringField('Nome do Jogo', [validators.data_required(), validators.Length(min=1, max=50)])
    categoria = StringField('Categoria', [validators.data_required(), validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.data_required(), validators.Length(min=1, max=20)])
    salvar = SubmitField('Salvar')
    
# Classe para representar o formulário de login 
class FormularioUsuario(FlaskForm):
    nickname = StringField('Nickname', [validators.data_required(), validators.Length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.data_required(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo
    return 'capa_padrao.jpg'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))
