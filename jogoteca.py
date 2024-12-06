from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

# Cria uma instância do flask
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Instânciando o banco de dados para ORM
db = SQLAlchemy(app)
# Instância de proteção para formulários
csrf = CSRFProtect(app)
# Intância para gerar hash de senhas
bcrypt = Bcrypt(app)

from views_game import *
from views_user import *

if __name__ == '__main__':
    app.run(debug=True)
