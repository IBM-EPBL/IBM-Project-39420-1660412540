from app import app
import ibm_db
from flask import session, flash, redirect, render_template, request, url_for
from .request import (businessArticles, entArticles, get_news_source,
                      healthArticles, publishedArticles, randomArticles,
                      scienceArticles, sportArticles, techArticles,
                      topHeadlines)

conn = ibm_db.connect(
    'DATABASE=bludb;'
    'HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;'
    'PORT=30875;'
    'SECURITY=SSL;'
    'SSLServerCertificate=DigiCertGlobalRootCA.crt;'
    'UID=rzf07928;'
    'PWD=Gsmx9dW4PeOQMqze;', '', ''
)

global account

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # getting user data
        email = request.form.get('email')
        password = request.form.get('password')
        sql_check_query = "SELECT * FROM user WHERE email = ?"
        stmt = ibm_db.prepare(conn, sql_check_query)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            # email id exists 
            # checking if the password is correct
            if not account['PASSWORD'] == password:
                flash('Invalid password', category='error')

            else:
                # user entered the correct password
                # redirecting the user to the dashboard
                session['user_id'] = account['EMAIL']
                return redirect(url_for('home'))

        else:
            # email id does not exist in the database
            flash('Email invalid... Try Again', category='error')
            
        return render_template('auth/login.html')
    
    return render_template('auth/login.html')
    # return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # getting user data
        email = request.form.get('email')
        password = request.form.get('password')
        # checking: user already exists or not
        sql_check_query = "SELECT * FROM user WHERE email = ?"
        stmt = ibm_db.prepare(conn, sql_check_query)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt) 

        account = ibm_db.fetch_assoc(stmt)
        # email id does not exist in the database
        if not account:
            # inserting the data into the database
            sql_insert_query = "INSERT INTO user VALUES (?, ?)"
            stmt = ibm_db.prepare(conn, sql_insert_query)
            ibm_db.bind_param(stmt, 1, email)
            ibm_db.bind_param(stmt, 2, password)
            ibm_db.execute(stmt)

            # user data inserted into the database
            # redirecting to login page
            flash('User created successfully! Please Login', category='success')
            return redirect('/')

        else:
            flash('Email id already exists! Try another one', category='error')

        return render_template('auth/register.html')

    return render_template('auth/register.html')
    # return render_template('register.html')