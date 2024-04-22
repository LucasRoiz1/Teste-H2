import requests
import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    user='banco_mocado',
    password='senha_mocada',
    host='localhost',
    database='banco_mocado'
)
cursor = conn.cursor()

consulta = "SELECT * FROM raw_data"
cursor.execute(consulta)
resultados = cursor.fetchall()

colunas = [i[0] for i in cursor.description]
df = pd.DataFrame(resultados, columns=colunas)

df['datahora_acesso'] = pd.to_datetime(df['datahora_acesso'])

df['Mes'] = df['datahora_acesso'].dt.month

df_consolidado = df.groupby(['Mes']).agg({
    'rake': 'sum',
    'cliente_id': pd.Series.nunique,
    'modalidade': pd.Series.nunique
}).rename(columns={
    'rake': 'rake_total',
    'cliente_id': 'jogadores',
    'modalidade': 'modalidades'
})

df_consolidado['rake_cash_game'] = df[df['modalidade'] == 'Cash Game'].groupby(['Mes'])['rake'].sum()
df_consolidado['rake_torneio'] = df[df['modalidade'] == 'Torneio'].groupby(['Mes'])['rake'].sum()
df_consolidado['jogadores_cash_game'] = df[df['modalidade'] == 'Cash Game'].groupby(['Mes'])['cliente_id'].nunique()
df_consolidado['jogadores_torneio'] = df[df['modalidade'] == 'Torneio'].groupby(['Mes'])['cliente_id'].nunique()

df_consolidado.reset_index(inplace=True)

try:
    cursor = conn.cursor()
    for indice, linha in df_consolidado.iterrows():
        # ano = linha['Ano']
        mes = linha['Mes']
        rake_total = linha['rake_total']
        jogadores = linha['jogadores']
        modalidades = linha['modalidades']
        rake_cash_game = linha['rake_cash_game']
        rake_torneio = linha['rake_torneio']
        jogadores_cash_game = linha['jogadores_cash_game']
        jogadores_torneio = linha['jogadores_torneio']
        consulta = """INSERT INTO estatistica_jogos_anomes 
                        (mes, rake_total, jogadores, modalidades, rake_cash_game, rake_torneio, jogadores_cash_game, jogadores_torneio) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        dados_insercao = (mes, rake_total, jogadores, modalidades, rake_cash_game, rake_torneio, jogadores_cash_game, jogadores_torneio)
        cursor.execute(consulta, dados_insercao)
    conn.commit()
    print("Dados inseridos com sucesso no banco de dados")
except Exception as e:
    print(f"Erro ao inserir dados no banco de dados: {e.args}")

cursor.close()
conn.close()