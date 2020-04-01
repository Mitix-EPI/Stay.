from app import app
# from flask import render_template
# from flask import request
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
from random import randint

from flask import jsonify
import pymysql as sql

@app.route('/', methods=['GET', 'POST'])
def index():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    print(session)
    if ('loggedin' in session):
        connect = sql.connect(host ="localhost",
                                user ='root',
                                passwd ='root@123',
                                db ='stay'
                                )
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM user WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    else :
        return redirect(url_for('signin'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'], day=session['day'])
    else:
        return redirect(url_for('signin'))

def check_date(date, value, timer): # Format date: YYYY/MM/JJ HH:MM

    # Cette fonction permet de récupérer la date de première connexion, pour ce faire on vérifie si
    # la date sans compter l'heure, la minute et plus petit est supérieure à la date précédemment entrée
    # dans la BDD de l'utilisateur. Si cette valeur est NULL c'est que l'utilisateur ne s'était pas connecté
    # dans les temps un ancien jour.

    # Dans le cas où la date est différente, on regarde alors l'heure de connexion. Si l'heure est bien entre 8h et
    # 10h30, alors on set la date actuelle, dans le cas contraire on set NULL
    # Dans tous les cas sauf lorsqu'il ne s'agit pas de la première connexion de l'utilisateur, le timer des popups est
    # également set sur NULL mais redéfini dans le fonction juste en dessous de celle-ci.

    new_possible_date = str(date.year) + "/" + str(date.month) + "/" + str(date.day) + " " + str(date.hour) + ":" + str(date.minute)

    if (value == "NULL"): # Si il avait raté un jour
        actual_hour = [int(date.hour), int(date.minute)]

        if actual_hour[0] >= 8 and actual_hour[0] <= 9:
            return new_possible_date, "NULL"
        elif actual_hour[0] == 10:
            if actual_hour[1] <= 30:
                return new_possible_date, "NULL"
            else:
                return "NULL", "NULL" # Plus tard que 10h30
        else:
            return "NULL", "NULL" # Plus tard que 10h30
    else: # Si il n'avait pas raté le jour
        tmp = value.split(" ")
        date_tmp = tmp[0].split("/")
        hour_tmp = tmp[1].split(":")

        for i in range(0, len(date_tmp)):
            date_tmp[i] = int(date_tmp[i])
        for i in range(0, len(hour_tmp)):
            hour_tmp[i] = int(hour_tmp[i])

        actual_date = [int(date.year), int(date.month), int(date.day)]
        actual_hour = [int(date.hour), int(date.minute)]

        is_diff = False
        for i in range(0, len(actual_date)):
            if actual_date[i] > date_tmp[i]:
                is_diff = True
                break
        if is_diff:
            if actual_hour[0] >= 8 and actual_hour[0] <= 9:
                return new_possible_date, "NULL"
            elif actual_hour[0] == 10:
                if actual_hour[1] <= 30:
                    return new_possible_date, "NULL"
                else:
                    return "NULL", "NULL" # Plus tard que 10h30
            else:
                return "NULL", "NULL" # Plus tard que 10h30
        else:
            return value, timer
    return "NULL", "NULL" # Si error

def set_timer(join_date, timer):

    # Dans le cas où le timer n'est pas NULL et est défini (cas si le joueur ne se connecte pas pour la première fois de la journée
    # mais qu'il s'est connecté la première fois dans les temps (entre 8h et 10h30)), on vérifie alors que le temps actuel a bien
    # dépassé l'heure indiquée dans le timer. Si c'est le cas, on fait de même que dans le premier paragraphe: à savoir un random
    # entre 30 minutes et 2h30


    # Pense-bête: Faire en sorte de set à NULL la date et timer si le refresh n'a pas eu lieu dans les 10 min
    # qui ont suivi la pop-up pour mettre le jour en fail
    # Penser donc à 18h à ajouter 1 jour à tous les users qui ont donc la date de première connexion != NULL

    if join_date == "NULL":
        return ("NULL")
    elif timer == "NULL":
        time = datetime.now()
        tmp = timedelta(hours=randint(0, 2), minutes=randint(0, 30))
        if tmp.hours == 0 and tmp.minutes < 30:
            tmp.minutes = 30
        time += tmp
        if time.hour < 8 or time.hour >= 18:
            return "NULL", join_date # 18h passé et les popups s'arrêtent à 18h
        else:
            text = str(time.hour) + ":" + str(time.minute)
            return text, join_date
    else:
        timer_split = timer.split(":")
        date_join_split = join_date.split(" ")
        date_hour = date_join_split[1].split(":")
        del date_join_split

        if int(timer_split[0]) <= int(date_hour[0]):
            if int(timer_split[1]) <= int(date_hour[1]) and int(date_hour[1]) - int(timer_split[1]) <= 10: # Temps dépassé
                time = datetime.now()
                tmp = timedelta(hours=randint(0, 2), minutes=randint(0, 30))
                if tmp.hours == 0 and tmp.minutes < 30:
                    tmp.minutes = 30
                time += tmp
                if time.hour < 8 or time.hour >= 18:
                    return ("NULL") # 18h passé et les popups s'arrêtent à 18h
                else:
                    text = str(time.hour) + ":" + str(time.minute)
                    return text, join_date
            elif int(timer_split[1]) <= int(date_hour[1]) and int(date_hour[1]) - int(timer_split[1]) > 10: # Temps dépassé mais plus de 10 min
                return "NULL", "NULL"
            else:
                return timer, join_date
        else:
            return timer, join_date
    return timer, join_date

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    msg = ''
    if (request.method =='POST' and 'username' in request.form and 'password' in request.form):
        username = request.form['username']
        password = request.form['password']

        print("connection en cours ...")
        connect = sql.connect(host ="localhost",
                                user ='root',
                                passwd ='root@123',
                                db ='stay'
                                )
        cursor = connect.cursor()
        print("connection établie")
        cursor.execute("""SELECT * FROM user WHERE (username = %s OR mail = %s) AND password = %s""", (username, username, password))
        account = cursor.fetchone()
        if (account):
            tmp, timer = check_date(datetime.now(), account[5], account[6])
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            session['mail'] = account[3]
            session['day'] = account[4]
            timer, tmp = set_timer(tmp, timer)
            session['time'] = tmp
            session['timer'] = timer
            return (redirect(url_for('home')))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)

@app.route("/signout", methods=['GET', 'POST'])
def signout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('signin'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if (request.method =='POST' and 'username' in request.form and 'password' in request.form and 'mail' in request.form):
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        tmp = ip.split(".")
        del tmp[-1]
        new_ip = ".".join(tmp)
        del tmp
        del ip
        print(new_ip)
        username = request.form['username']
        password = request.form['password']
        mail = request.form['mail']
        print("connection en cours ...")
        connect = sql.connect(host ="localhost",
                                user ='root',
                                passwd ='root@123',
                                db ='stay'
                                )
        cursor = connect.cursor()
        print("connection établie")
        cursor.execute("SELECT * FROM user WHERE username = '%s' OR ip = '%s'" %(username, new_ip))
        account = cursor.fetchone()
        print(account)
        if (account and account[4] == new_ip):
            msg = "You already have an account in your house"
        elif (account):
            msg = "Account already exists"
        else :
            day = 0
            cursor.execute("INSERT INTO %s (username, password, mail, ip, day) VALUES ('%s', '%s', '%s', '%s', '%d')" % ("user", username, password, mail, str(new_ip), int(day)))
            connect.commit()
            msg = "Account Created perfectly !"
            print("Envoie de la donnée à la DB")
            print("le compte %s avec le mdp %s est créé", (username, password))
    elif request.method == 'POST':
        msg = "Fill out the form"
    return render_template('register.html', msg=msg)


























# @app.route('/user', methods=['GET'])
# def route_all_users():
#     result = 'Liste de la Base de donnees \n '
#     try:
#         ## We ’re creating connection between our mysql server and our app
#         print("connection en cours ...")
#         connect = sql.connect(host ="localhost",
#                                 # unix_socket =' path_to_our_mysql_socket',
#                                 user ='root',
#                                 passwd ='root@123',
#                                 db ='stay'
#                                 )
#         ## We ’re retrieving a " pointer " aka " cursor " to our database
#         cursor = connect.cursor()
#         print("connection établie")
#         # cursor.execute(sql_create) //peut etre
#         try:
#             print("Envoie de la donnée à la DB")
#             reference = ("georges", "what-else?")
#             cursor.execute("""INSERT INTO user (name, password) VALUES(%s, %s)""", reference)
#             connect.commit()
#             print("Donnée envoyée à la DB")
#         except :
#             print("Retour en arrière")
#             connect.rollback()
#         ## We ’re executing a SQL command ,x
#         ## assuming that all tables are already created
#         print("Récupération des données")
#         cursor.execute("""SELECT DISTINCT name, password FROM user""")
#         rows = cursor.fetchall()
#         print(rows)
#         for row in rows:
#             result += 'name : {0} | password : {1} \n'.format(row[0], row[1])
#         print("Données récupérées")
#         # cursor.execute("SELECT * from user")
#         # ## We ’re retrieving all results
#         # result = cursor.fetchall()
#         ## We ’re closing our cursor and our connection
#         cursor.close()
#         connect.close()
#     except Exception as e :
#         print("y'a un bleme")
#         print ("Caught an exception : ", e)
#     ## We ’re sending the data
#     return jsonify(result)
