# criar a estrutura do banco de dados
from fakepinterest import database, login_manager
from datetime import datetime
from flask_login import UserMixin

# essa função é obrigatória e o padrão do nome dela é "login_" + nome da classe usuario em minúsculo
# temos que colocar o decorator do login_manager para reconhecer que isso faz parte do login_manager
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

# cada classe aqui será uma tabela do banco de dados
# e cada atributo será uma coluna da tabela
# aqui definimos o tipo da coluna e as contraints (não nulas, chave primária e chave estrangeira)
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key = True)
    username = database.Column(database.String, nullable = False)
    email = database.Column(database.String, nullable = False, unique = True)
    senha = database.Column(database.String, nullable = False)
    fotos = database.relationship("Foto", backref = "usuario", lazy = True)

class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default="default.png")
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=True)