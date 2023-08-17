from fakepinterest import app

if __name__ == '__main__':
    # debug = True significa que todas as alterações feitas aqui serão passadas ao site.
    # Senão tem que pausar o site e rodar de novo
    app.run(debug = True)


# Aula 9 de 23: Criando um banco de dados
# instalar o pip install flask-sqlalchemy