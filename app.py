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

DATA_PATH = 'data/auditorias.xlsx'

# Verifica se o arquivo Excel existe, caso contrário, cria um
if not os.path.exists(DATA_PATH):
    df = pd.DataFrame(columns=['name', 'date'])
    df.to_excel(DATA_PATH, index=False, engine='openpyxl')

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
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    group_by = request.args.get('group_by', 'cia_pm')

    print("Data de início:", start_date)
    print("Data de fim:", end_date)
    print("Agrupar por:", group_by)

    df = pd.read_excel('data/auditorias.xlsx', engine='openpyxl')
    df['data_fato'] = pd.to_datetime(df['data_fato'])
    df['numero_ocorrencia'] = 1

    if start_date and end_date:
        df = df[(df['data_fato'] >= pd.to_datetime(start_date)) & (df['data_fato'] <= pd.to_datetime(end_date))]
    elif start_date:
        df = df[df['data_fato'] >= pd.to_datetime(start_date)]
    elif end_date:
        df = df[df['data_fato'] <= pd.to_datetime(end_date)]

    #plot = create_plot(df, group_by_field=group_by)
    #return render_template('dashboard.html', plot=plot, start_date=start_date, end_date=end_date, group_by=group_by)

    plot1_html, plot2_html = create_plots()
    return render_template('dashboard.html', plot1=plot1_html, plot2=plot2_html)

@app.route('/cadastro_auditoria', methods=['GET', 'POST'])
@login_required
def cadastro_auditoria():
    if request.method == 'POST':
        data = request.form.to_dict()
        df = pd.read_excel(DATA_PATH, engine='openpyxl')
        df = df.append(data, ignore_index=True)
        df.to_excel(DATA_PATH, index=False, engine='openpyxl')
        return redirect(url_for('dashboard'))
    return render_template('cadastro_auditoria.html')

def create_plot(df, group_by_field):
    counts = df.groupby(group_by_field).size().reset_index(name='counts')
    fig = px.bar(counts, x=group_by_field, y='counts', title='Número de Ocorrências por Cia PM',
                 labels={'counts': 'Quantidade de Ocorrências', group_by_field: 'Cia PM'})
    return fig.to_html()

def create_plots():
    # Primeiro gráfico (já existente)
    df = pd.read_csv('data/auditorias.csv', encoding='latin1')  # Ajuste para a sua fonte de dados atual
    counts = df.groupby('cia_pm').size().reset_index(name='counts')
    fig1 = px.bar(counts, x='cia_pm', y='counts', title='Número de Ocorrências por Cia PM')

    # Segundo gráfico (novo)
    wide_df = px.data.medals_wide()
    fig2 = px.bar(wide_df, x="nation", y=["gold", "silver", "bronze"], title="Wide-Form Input")

    return fig1.to_html(), fig2.to_html()
if __name__ == '__main__':
    app.run(debug=True)
