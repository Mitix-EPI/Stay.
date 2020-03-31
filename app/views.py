from app import app
# from flask import render_template
# from flask import request
from flask import Flask, render_template, request, redirect, url_for, session


from flask import jsonify
import pymysql as sql

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    print(session)
    if ('loggedin' in session):
        connect = sql.connect(host ="localhost",
                                user ='root',
                                passwd ='root@123',
                                db ='epitodo'
                                )
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    else :
        return redirect(url_for('signin'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'loggedin' in session:
        return render_template('index.html', username=session['username'])
    else:
        return redirect(url_for('signin'))

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
                                db ='epitodo'
                                )
        cursor = connect.cursor()
        print("connection établie")
        cursor.execute("""SELECT * FROM accounts WHERE username = %s AND password = %s""", (username, password))
        account = cursor.fetchone()
        if (account):
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
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
    if (request.method =='POST' and 'username' in request.form and 'password' in request.form):
        username = request.form['username']
        password = request.form['password']
        print("connection en cours ...")
        connect = sql.connect(host ="localhost",
                                user ='root',
                                passwd ='root@123',
                                db ='epitodo'
                                )
        cursor = connect.cursor()
        print("connection établie")
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username))
        account = cursor.fetchone()
        if (account):
            msg = "Account already exists"
        else :
            cursor.execute("""INSERT INTO accounts VALUES (NULL, %s, %s)""", (username, password))
            connect.commit()
            msg = "Account Created perfectly !"
            print("Envoie de la donnée à la DB")
            print("le compte %s avec le mdp %s est créé", (username, password))
    elif request.method == 'POST':
        msg = "Fill out the form"
    return render_template('register.html', msg=msg)

@app.route('/user', methods=['GET'])
def route_all_users():
    result = 'Liste de la Base de donnees \n '
    try:
        ## We ’re creating connection between our mysql server and our app
        print("connection en cours ...")
        connect = sql.connect(host ="localhost",
                                # unix_socket =' path_to_our_mysql_socket',
                                user ='root',
                                passwd ='root@123',
                                db ='epitodo'
                                )
        ## We ’re retrieving a " pointer " aka " cursor " to our database
        cursor = connect.cursor()
        print("connection établie")
        # cursor.execute(sql_create) //peut etre
        try:
            print("Envoie de la donnée à la DB")
            reference = ("georges", "what-else?")
            cursor.execute("""INSERT INTO user (name, password) VALUES(%s, %s)""", reference)
            connect.commit()
            print("Donnée envoyée à la DB")
        except :
            print("Retour en arrière")
            connect.rollback()
        ## We ’re executing a SQL command ,x
        ## assuming that all tables are already created
        print("Récupération des données")
        cursor.execute("""SELECT DISTINCT name, password FROM user""")
        rows = cursor.fetchall()
        print(rows)
        for row in rows:
            result += 'name : {0} | password : {1} \n'.format(row[0], row[1])
        print("Données récupérées")
        # cursor.execute("SELECT * from user")
        # ## We ’re retrieving all results
        # result = cursor.fetchall()
        ## We ’re closing our cursor and our connection
        cursor.close()
        connect.close()
    except Exception as e :
        print("y'a un bleme")
        print ("Caught an exception : ", e)
    ## We ’re sending the data
    return jsonify(result)
