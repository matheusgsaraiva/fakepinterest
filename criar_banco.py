# Aula 9 de 23: Criando um banco de dados
from fakepinterest import database, app
from fakepinterest.models import Usuario, Foto

with app.app_context():
    database.create_all()

# Assim vamos ter criado o banco de dados database contendo duas tabelas (Usuario e Foto) e com as colunas que a gente criou no models.py