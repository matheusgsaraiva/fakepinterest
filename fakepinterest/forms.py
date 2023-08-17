# criar os formulários do nosso site
# aqui vai conter as classes de login e contas
# precisa instalar pip install flask-wtf e pip install email_validator
from flask_wtf import FlaskForm # precisa disso para criar os formulários de login
from wtforms import StringField, PasswordField, SubmitField, FileField # são os campos possíveis, de texto (login), de senha (password) e botão (submit)
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError # validadores para os campos de login, senha e email
from fakepinterest.models import Usuario


# Aula 11 de 23: Criar formulários de login e de criar conta
# cada atributo será o que vai aparecer na página
# então vai ter um espaço para por o email, outro espaço para por a senha e um botão para acessar a conta
# DataRequired significa que precisa ser preenchido para ser validado
class FormLogin(FlaskForm):
    # no html email.label será E-mail
    email = StringField("E-mail", validators = [DataRequired(), Email()]) # E-mail é o que vai aparecer do lado da caixa de login
    # no html senha.label será Senha
    senha = PasswordField("Senha", validators = [DataRequired()]) # Senha é o que vai aparecer do lado da caixa de senha
    botao_confirmacao = SubmitField("Fazer Login") # Fazer Login  é o que vai aparecer no botão

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email = email.data).first() # procurando na tabela Usuario do banco de dados se já existe o email inserido
        if not usuario: # se não encontrar usuario manda uma mensagem de erro
            raise ValidationError("Usuário não existente, crie uma conta")

# aqui vai ter mais espaços (email, usuário, senha e confirmação de senha e o botão para criar a conta)
class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators = [DataRequired(), Email()])
    username = StringField("Nome do usuário", validators = [DataRequired()])
    senha = PasswordField("Senha", validators = [DataRequired(), Length(6, 20)]) # colocamos que a senha deve ter entre 6 e 20 caracteres
    confirmacao_senha = PasswordField("Confirmação de Senha", validators = [DataRequired(), EqualTo("senha")]) # aqui tem o validador EqualTo para garantir que as duas senhas são iguais
    botao_confirmacao = SubmitField("Criar Conta") # o nome do botão vai ser Criar Conta (isso que vai aparecer no site

    # não permitir que tenha duas contas com o mesmo email
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email = email.data).first() # procurando na tabela Usuario do banco de dados se já existe o email inserido
        if usuario:
            raise ValidationError("Email já cadastrado, faça login para continuar")

class FormFoto(FlaskForm):
    foto = FileField("Foto", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Enviar")