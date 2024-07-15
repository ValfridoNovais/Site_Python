from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

DATA_PATH = 'data/auditorias.csv'

# Verifica se o arquivo CSV existe, caso contrário, cria um
if not os.path.exists(DATA_PATH):
    df = pd.DataFrame(columns=['name', 'date'])
    df.to_csv(DATA_PATH, index=False)

@app.route('/')
def dashboard():
    df = pd.read_csv(DATA_PATH)
    return render_template('dashboard.html', auditorias=df.to_dict(orient='records'))

@app.route('/cadastro_auditoria', methods=['GET', 'POST'])
def cadastro_auditoria():
    if request.method == 'POST':
        data = request.form.to_dict()
        df = pd.read_csv(DATA_PATH)
        df = df.append(data, ignore_index=True)
        df.to_csv(DATA_PATH, index=False)
        return redirect(url_for('dashboard'))
    return render_template('cadastro_auditoria.html')

if __name__ == '__main__':
    app.run(debug=True)
