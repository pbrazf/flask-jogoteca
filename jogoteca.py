from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Cria uma instância do flask
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Instânciando o banco de dados para ORM
db = SQLAlchemy(app)

from views import *

if __name__ == '__main__':
    app.run(debug=True)
