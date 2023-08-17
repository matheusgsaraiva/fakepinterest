from flask import Flask # pip install flask
from flask_sqlalchemy import SQLAlchemy # pip install flask_sqlalchemy
from flask_login import LoginManager # pip install flask_login
from flask_bcrypt import Bcrypt # pip install flask_bcrypt

# pip install email_validator

app = Flask(__name__) # nome do aplicativo
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db" # parametro para definir o local do banco de dados. Documentação do flask explica isso
app.config["SECRET_KEY"] = "fde4fb3793cf2eb8d85cc32896524128" # chave de segurança
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"
database = SQLAlchemy(app)

# Aula 10 de 23: Implementar sistema de login e segurança
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'homepage' # a página que vai aparecer a janela de login

# tem que importar o routes depois de inicializar o app que é a linha de cima (app = Flask(__name__) # nome do aplicativo)
from fakepinterest import routes

# Aula 10 de 23: Implementar sistema de login e segurança
# instalar pip install flask-login flask-bcrypt