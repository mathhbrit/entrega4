from flask import Flask
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask.cli import FlaskGroup

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Atualize com a URI do seu banco de dados
db.init_app(app)


with app.app_context():
    db.create_all()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    senha = db.Column(db.String(80), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET','POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')  # Crie o template 'cadastro.html' com o formulário
    elif request.method == 'POST':
        email = request.form.get('email')
        nome = request.form.get('nome')
        senha = request.form.get('senha')

        novo_usuario = User(email=email, nome=nome, senha=senha)

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            return redirect(url_for('index'))  # Redirecione para a página inicial após o cadastro
        except Exception as e:
            db.session.rollback()
            return render_template('cadastro.html', error_message="Erro ao cadastrar usuário. Tente novamente.")

@app.route('/login')
def login():
    return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)
   
    
