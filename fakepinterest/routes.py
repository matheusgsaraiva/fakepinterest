# criar as rotas do nosso site (os link)
from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from fakepinterest.models import Usuario, Foto # vamos usar as informações dessas tabelas aqui
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto # importando os formulários de login e criar conta
import os
from werkzeug.utils import secure_filename # essa biblioteca já vem isntalada


@app.route("/", methods = ["GET", "POST"]) # com o url_for podemos mudar o nome da rota. Exemplo de "/" para "/homepage" que não vai ter problema, pois o url_for vai na função homepage
# para cada rota que criarmos temos que definir uma função pra ela
# método post no html vai enviar informações para cá
# sempre que for importar uma variável o html coloca entre {{}}, Exemplo: arquivo homepage.html {{ form.csrf_token }}
# o csrft_token é uma trava de segurança contra hackers
#
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit(): # verificando se os validators definido em forms estão sendo respeitados
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        # form_login.senha.data é o valor da senha preenchida
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data): # se existe usuario e a senha está correta
            login_user(usuario) # fazer login do usuario
            # redirecionar para a página do usuário
            return redirect(url_for("perfil", id_usuario=usuario.id))

    return render_template("homepage.html", form=form_login)

# Aula 12 de 23: Implementar o formulário de login na homepage e de criar conta
# vamos ter uma página diferente para criar contas
@app.route("/criarconta", methods = ["GET", "POST"]) # liberamos o get e post para a página criarconta
def criarconta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit(): # só vai passar se tudo estiver validado com os validators definidos em forms
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data) # bcrypt para criptografar a senha. Até na tabela do banco de dados a senha estará criptografada
        # transferindo as informações do formulario de criar conta para a tabela. ".data" é para pegar o valor do
        # username ou email inserido
        usuario = Usuario(username = form_criarconta.username.data,
                          senha=senha,
                          email=form_criarconta.email.data)
        database.session.add(usuario) # adicionando os valores
        database.session.commit() # fazendo o commit das informações adicionadas

        # após criar a conta será automaticamente logado na conta criada tem que fazer o login pois para acessar a
        # página de perfil é requerido o login. Remember = True é para lembrar que o usuário está logado
        login_user(usuario, remember = True)

        # redirecionando para a página do perfil do usuário criado, passando o id do usuário criado que é o que a
        # route perfil requer como parâmetro
        return redirect(url_for("perfil", id_usuario=usuario.id))

    return render_template("criarconta.html", form=form_criarconta)

# perfil tem uma restrição que é só somente usuarios logados que podem acessar por isso tem o @login_required
@app.route("/perfil/<id_usuario>", methods=["GET","POST"]) # Aula 14 de 23: Logout do Usuário e Atualizando o Perfil do Usuário
@login_required
def perfil(id_usuario):
    # verificar que o usuário enviado é o usuário atual. Queremos limitar o acesso a somente ao usuário que foi logado
    if int(id_usuario) == int(current_user.id):
        # o usuario ta vendo o perfil dele
        # passando o formulário de fotos
        form_foto = FormFoto()

        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            # salvar o arquivo na pasta fotos_post
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), # os.path.abspath(os.path.dirname(__file__)) é o caminho original do routes.py
                              app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
            # registrar esse arquivo no banco de dados
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None) # podemos passar o usuario no render_template

# vamos colocar um for no html para mostrar as fotos de cada perfil usando a seguinte estrutura
# {% for foto in usuario.fotos %} e {% endfor %}

# para pegar as imagens vamos usar o url_for e mostrar o caminho de onde está fotos usando a estrutura
# <img src="{{ url_for('static', filename = 'fotos_posts/default.png') }}">
# primeiro argumento do url_for é a pasta static (padrão é colocar static) e depois é o nome do arquivo

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage")) # redirecionar para a homepage após o logout

@app.route("/feed")
@login_required
def feed():
    # pegando as fotos de todos os usuários. Poderia limitar a 100 se quisesse, basta fazer .all()[:100]
    fotos= Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template("feed.html", fotos=fotos)