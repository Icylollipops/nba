import urllib.request as request
from bs4 import BeautifulSoup
import re
from pprint import pprint
import sqlite3

# player STats

base_url = 'http://espn.go.com'

teams_url = 'http://espn.go.com/nba/teams'
html_teams = request.urlopen(teams_url)

soup_teams = BeautifulSoup(html_teams, 'lxml')

urls = soup_teams.find_all(href=re.compile('/nba/teams/stats'))

team_urls = [base_url + url['href'] for url in urls]

team_name_dict = {'bos': 'Boston Celtics',
                  'bkn': 'Brooklyn Nets',
                  'nyk': 'New York Knicks',
                  'phi': 'Philadelphia 76ers',
                  'tor': 'Toronto Raptors',
                  'gsw': 'Golden State Warriors',
                  'lac': 'Los Angeles Clippers',
                  'lal': 'Los Angeles Lakers',
                  'pho': 'Phoenix Suns',
                  'sac': 'Sacramento Kings',
                  'chi': 'Chicago Bulls',
                  'cle': 'Cleveland Cavaliers',
                  'det': 'Detroit Pistons',
                  'ind': 'Indiana Pacers',
                  'mil': 'Milwaukee Bucks',
                  'dal': 'Dallas Mavericks',
                  'hou': 'Houston Rockets',
                  'mem': 'Memphis Grizzlies',
                  'nor': 'New Orleans Pelicans',
                  'sas': 'San Antonio Spurs',
                  'atl': 'Atlanta Hawks',
                  'cha': 'Charlotte Hornets',
                  'mia': 'Miami Heat',
                  'orl': 'Orlando Magic',
                  'was': 'Washington Wizards',
                  'den': 'Denver Nuggets',
                  'min': 'Minnesota Timberwolves',
                  'okc': 'Oklahoma City Thunder',
                  'por': 'Portland Trail Blazers',
                  'uth': 'Utah Jazz'
                  }


# http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]


for team in team_urls:
    team_code = team[-3:]
    html_team = request.urlopen(team)

    soup_team = BeautifulSoup(html_team, 'lxml')

    roster = soup_team.find_all('tr', class_=re.compile('player'))
    # roster_game_stats = roster[:int(len(roster)/2)]
    roster_shooting_stats = roster[-int(len(roster) / 2):]

    players = []
    for row in roster_shooting_stats:
        for data in row:
            players.append(data.get_text())

    player_ids = [player.a['href'].split('/')[7] for player in roster_shooting_stats]

    index = 0
    increment = 0
    for id in player_ids:
        players.insert(index + increment, id)
        index = index + 15
        increment = increment + 1

    index = 2
    increment = 0
    for id in player_ids:
        players.insert(index + increment, team_name_dict[team_code])
        index = index + 16
        increment = increment + 1
    #sqlfile = "C:\\Users\\Justin\\Desktop\\sqllite\\SQLiteStudio\\nba.db"
    conn = sqlite3.connect("C:\\Users\\Justin\\Desktop\\sqllite\\SQLiteStudio\\nba.db")
    c = conn.cursor()

    for row in chunks(players, 17):
        try:
            c.execute('INSERT INTO player_shooting_stats VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', row)
        except:
            pass
        conn.commit()
    conn.close()
