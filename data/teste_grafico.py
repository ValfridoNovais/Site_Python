import pandas as pd
import plotly.express as px

# Carregando os dados
df = pd.read_csv('auditorias.csv', encoding='ISO-8859-1')  # Certifique-se de que a codificação está correta
print(df.head())  # Isso mostrará as primeiras linhas do DataFrame e ajudará a verificar os nomes das colunas

# Converter colunas de data para tipo data
df['Ano_Mes_Dia'] = pd.to_datetime(df['ano'].astype(str) + '-' + df['mes'].astype(str) + '-' + df['dia'].astype(str))

# 1. Distribuição Mensal de Ocorrências
def plot_monthly_distribution(company, platoon):
    filtered_data = df[(df['cia_pm'] == company) & (df['pelotao'] == platoon)]
    monthly_counts = filtered_data.groupby(filtered_data['Ano_Mes_Dia'].dt.to_period("M")).size().reset_index(name='counts')
    fig = px.bar(monthly_counts, x='Ano_Mes_Dia', y='counts', title='Distribuição Mensal de Ocorrências')
    fig.show()

# 2. Tipos de Crime por Localização
def plot_crime_types(company, platoon):
    filtered_data = df[(df['cia_pm'] == company) & (df['pelotao'] == platoon)]
    crime_types = filtered_data.groupby('nome_municipio')[['furto', 'roubo', 'extorsao']].sum().reset_index()
    fig = px.bar(crime_types, x='nome_municipio', y=['furto', 'roubo', 'extorsao'], title='Tipos de Crime por Localização', barmode='group')
    fig.show()

# 3. Natureza das Ocorrências
def plot_occurrence_nature(company, platoon):
    filtered_data = df[(df['cia_pm'] == company) & (df['pelotao'] == platoon)]
    nature_counts = filtered_data['natureza_ocorrencia_descricao_longa'].value_counts().reset_index(name='counts')
    fig = px.pie(nature_counts, values='counts', names='index', title='Natureza das Ocorrências')
    fig.show()

# Exemplo de como chamar as funções
plot_monthly_distribution('1ª Cia', '1º Pelotão')
plot_crime_types('1ª Cia', '1º Pelotão')
plot_occurrence_nature('1ª Cia', '1º Pelotão')
