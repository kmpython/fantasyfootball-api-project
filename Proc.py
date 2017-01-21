import urllib.request as ur
import urllib.parse
import json
import sqlite3
import msvcrt


def fetch_json_data(url_func):
    url = url_func

    values = {'name': 'Michael Foord',
              'location': 'Northampton',
              'anguage': 'Python'}
    headers = {'User-Agent': 'Mozilla/5.0'}

    data = urllib.parse.urlencode(values)
    data = data.encode('ascii')
    req = urllib.request.Request(url, data, headers)
    response = urllib.request.urlopen(req)
    the_page = response.read().decode('utf-8')

    return the_page


def exitRoutine():
    loop = input("Press Y to continue to main menu Or press any other key to exit : ")
    return loop


def dec_tab_team(cur):
    cur.executescript('''
    DROP TABLE IF EXISTS team;

    CREATE TABLE team (
    id     TEXT NOT NULL PRIMARY KEY,
    name   TEXT UNIQUE,
    city   TEXT
    );

    ''')


def dec_tab_schedule(cur):
    cur.executescript('''
    DROP TABLE IF EXISTS schedule;

    CREATE TABLE schedule (
    game_week TEXT NOT NULL,
    hteam   TEXT,
    ateam   TEXT,
    gdate   TEXT,
    gtime   TEXT,
    gtvstn  TEXT
    );

    ''')


def dec_tab_player(cur):
    cur.executescript('''
    DROP TABLE IF EXISTS player;

    CREATE TABLE player (
    fname TEXT NOT NULL,
    team   TEXT,
    pos   TEXT,
    jersey TEXT,
    height TEXT,
    weight TEXT,
    college TEXT
    );

    ''')

def main():
    loopM = "y"
    while loopM == "y" or loopM == "Y":
        print("please select your choices:")
        print(" 1 for list of NFL teams")
        print(" 2 for NFL schedule")
        print(" 3 for NFL players")

        enter = input('enter your choice here:')
        option = int(enter)
        url = None

        conn = sqlite3.connect('ffn.sqlite')
        cur = conn.cursor()

        if option == 1:
            url_func = 'http://www.fantasyfootballnerd.com/service/nfl-teams/json/test/'
            dec_tab_team(cur)
            the_page1 = fetch_json_data(url_func)
            team_data = json.loads(the_page1)
            for item in team_data['NFLTeams']:
                print("Team code :  {}   Team name :  {}  Team city :  {}".format(item["code"], item['fullName'],
                                                                                  item['shortName']))
                cur.execute('''INSERT OR REPLACE INTO team
                (id, name, city) VALUES ( ?, ?, ? )''',
                            (item["code"], item['fullName'], item['shortName']))

            loopM = exitRoutine()

        elif option == 2:
            url_func = 'http://www.fantasyfootballnerd.com/service/schedule/json/test/'
            dec_tab_schedule(cur)
            the_page1 = fetch_json_data(url_func)
            team_schedule = json.loads(the_page1)
            for item in team_schedule['Schedule']:
                print("gameweek :  {}   hometeam :  {}  awayteam :  {}".format(item["gameWeek"], item['homeTeam'],
                                                                               item['awayTeam'], item['gameDate'],
                                                                               item['gameTimeET'], item['tvStation']))
                cur.execute('''INSERT OR REPLACE INTO schedule
                (game_week, hteam, ateam, gdate, gtime, gtvstn) VALUES ( ?, ?, ?, ?, ?, ? )''',
                            (item["gameWeek"], item['homeTeam'], item['awayTeam'], item['gameDate'], item['gameTimeET'],
                             item['tvStation']))

            print("do you want to view additional detials ? (game time, date and channel?)")
            print("press Y for yes or N for NO")
            byteChoice = msvcrt.getch()
            choice = byteChoice.decode("utf-8")

            while (choice == "Y" or choice == 'y'):
                print("please enter game week home and away team")
                gme_week = input("enter game week: ")
                hm_team = input("enter home team: ")
                hm_team = hm_team.upper()
                aw_team = input("enter away team: ")
                aw_team = aw_team.upper()

                cur.execute('''SELECT * FROM schedule WHERE game_week = ? and hteam = ? and ateam = ?''',
                            (gme_week, hm_team, aw_team))
                try:
                    row = cur.fetchone()
                    print("game week : " + row[0])
                    print("home team : " + row[1])
                    print("away team : " + row[2])
                    print("date is : " + row[3])
                    print("time is : " + row[4])
                    print("channel is: " + row[5])
                    choice = "N"
                except:
                    print("row not found! check values once and try again!")
                    print("Press Y to try again")
                    byteChoice = msvcrt.getch()
                    choice = byteChoice.decode("utf-8")

            if (choice != "Y" or choice != 'y'):
                loopM = exitRoutine()
            else:
                print(" wrong choice!!")

        elif option == 3:

            pos_list = ["QB", " RB", "WR", "TE", "K", "DEF"]
            position = input("enter choice of position : QB RB, WR, TE, K, DEF or press enter for entire list : ")
            url_temp = 'http://www.fantasyfootballnerd.com/service/players/json/test/'

            if position.upper() in pos_list:
                url_func = url_temp + position.upper() + "/"
            else:
                url_func = url_temp

            dec_tab_player(cur)
            the_page1 = fetch_json_data(url_func)
            team_player = json.loads(the_page1)
            for item in team_player['Players']:
                print("First Name :  {}   Team :  {}  Position :  {}".format(item["fname"], item['team'],
                                                                             item['position']))
                cur.execute('''INSERT OR REPLACE INTO player
                (fname, team, pos, jersey, height, weight, college) VALUES ( ?, ?, ?, ?, ?, ?, ? )''',
                            (item["fname"], item['team'], item['position'], item['jersey'], item['height'],
                             item['weight'], item['college']))

            loopM = exitRoutine()

        else:
            print("Enter valid Choice !!")
            loopM = exitRoutine()

        conn.commit()


if __name__ == "__main__": main()