import requests
import mysql.connector

def gravaBanco(json):
    
    conn = mysql.connector.connect(
        user='banco_mocado',
        password='senha_mocada',
        host='localhost',
        database='banco_mocado'
    )
    cursor = conn.cursor()
    
    values = ''
    for item in json:
        try:
            score_home = item['scores'][0]['score']
        except:
            score_home = '0'

        try:
            score_away = item['scores'][1]['score']
        except:
            score_away = '0'

        values += ",('" + item['commence_time'].replace('T', ' ').replace('Z','' ) + "', '" + item['commence_time'][:10] + "', '" + item['home_team'] + "', '" + item['away_team'] + "', " + score_home + ", " + score_away + ")"

    cursor.execute('INSERT INTO matchs_epl VALUES ' + values[1:])
    conn.commit()
    cursor.close()
    conn.close()

url = "https://odds.p.rapidapi.com/v4/sports/soccer_brazil_campeonato/scores"

querystring = {"daysFrom":"3"}

headers = {
	"X-RapidAPI-Key": "8c0123fc64mshee05b1ce79fe169p113287jsn7e27bbe36c24",
	"X-RapidAPI-Host": "odds.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
gravaBanco(response.json())

