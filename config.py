SECRET_KEY = 'alura'

SQLALCHEMY_DATABASE_URI = \
        '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
            SGBD = 'mysql+mysqlconnector',
            usuario = 'pbrazf',
            senha = 'qwe123po',
            servidor = 'localhost',
            database = 'jogoteca'
            )
