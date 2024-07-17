from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import pandas as pd
import os
import plotly.express as px

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
    df = pd.read_csv('data/auditorias.csv', encoding='latin1')
    df['data_fato'] = pd.to_datetime(df['data_fato'])
    df['numero_ocorrencia'] = 1  # Supondo que cada linha é uma ocorrência

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    group_by = request.args.get('group_by', 'cia_pm')

    if start_date and end_date:
        df = df[(df['data_fato'] >= start_date) & (df['data_fato'] <= end_date)]

    plot = create_plot(df, group_by_field=group_by)
    return render_template('dashboard.html', plot=plot)

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

#função para criar o gráfico:
def create_plot(data_frame, group_by_field='cia_pm'):
    fig = px.bar(data_frame, x=group_by_field, y='numero_ocorrencia', title=f'Ocorrências por {group_by_field}')
    graphJSON = fig.to_json()
    return graphJSON


if __name__ == '__main__':
    app.run(debug=True)
