from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'secretK'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    senha = db.Column(db.String(80), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        nome = request.form.get('nome')
        senha = request.form.get('senha')

        novo_usuario = User(email=email, nome=nome, senha=generate_password_hash(senha))

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            return render_template('cadastro.html', error_message="Erro ao cadastrar usuário. Tente novamente.")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        usuario = User.query.filter_by(email=email).first()

        if usuario:
            print(f"Senha no banco de dados: {usuario.senha}")  # Adicione esta linha
            print(f"Senha informada no formulário: {senha}")  # Adicione esta linha

            if check_password_hash(usuario.senha, senha):
                login_user(usuario)
                print("Login bem-sucedido")
                return redirect(url_for('pagina_protegida'))
            else:
                print("Senha incorreta")
        else:
            print("Usuário não encontrado")

        print("Login falhou")
        return make_response('não', 401)

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/pagina_protegida')
@login_required
def pagina_protegida():
    return render_template('pagina_protegida.html', user=current_user.email)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        usuarios = User.query.all()
    app.run(debug=True)

    



