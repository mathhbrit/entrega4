
from flask import Flask
from flask import Flask, render_template, request, redirect, url_for
from models import db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Atualize com a URI do seu banco de dados
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET'])
def cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')  # Crie o template 'cadastro.html' com o formulário

    
if __name__ == '__main__':
    app.run(debug=True)

    
