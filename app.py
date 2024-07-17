from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

DATA_PATH = 'data/auditorias.csv'

# Verifica se o arquivo CSV existe, caso contrário, cria um
if not os.path.exists(DATA_PATH):
    df = pd.DataFrame(columns=['name', 'date'])
    df.to_csv(DATA_PATH, index=False, encoding='latin1')

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            user = User(username)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login inválido. Tente novamente.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    df = pd.read_csv(DATA_PATH, encoding='latin1')
    return render_template('dashboard.html', auditorias=df.to_dict(orient='records'))

@app.route('/cadastro_auditoria', methods=['GET', 'POST'])
@login_required
def cadastro_auditoria():
    if request.method == 'POST':
        data = request.form.to_dict()
        df = pd.read_csv(DATA_PATH, encoding='latin1')
        df = df.append(data, ignore_index=True)
        df.to_csv(DATA_PATH, index=False, encoding='latin1')
        return redirect(url_for('dashboard'))
    return render_template('cadastro_auditoria.html')

if __name__ == '__main__':
    app.run(debug=True)
