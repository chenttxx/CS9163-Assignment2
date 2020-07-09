############CS9163 Application Security############
###################################################
################Tianxiang Chen#####################
###################################################
#################Assignment 2######################

from flask import Flask, request, session, render_template, redirect
import os
import subprocess
from flask_wtf.csrf import CSRFProtect
import bcrypt

def create_app():
    app = Flask(__name__)
    db = {}
    dict = "wordlist.txt"
    csrf = CSRFProtect(app)
    app.secret_key = os.urandom(24)
    salt = bcrypt.gensalt()

    @app.route("/")
    def home():
        loggedInUser = False
        if 'username' in session:
            loggedInUser = True
        return render_template('home.html', loggedInUser=loggedInUser)


    @app.route("/register", methods=['GET', 'POST'])
    def register():
        message = None
        if 'username' not in session:
            if request.method == 'POST':
                uname = request.form['uname']
                pword = request.form['pword']
                twofactor = request.form['2fa']
                
                if not uname or not pword:
                    message = "Registration failure."
                    return render_template("register.html", id=message)
                if len(uname) > 20 or len(pword) > 20:
                    message = "The username or password length is invalid."
                    return render_template("register.html", id=message)
                for c in uname:
                    if not(46<=ord(c)<=57 or 64<=ord(c)<=90 or 97<=ord(c)<=122):
                        message = "The username is invalid."
                        return render_template("register.html", id=message)
                for p in pword:
                    if not 0<=ord(p)<=127:
                        message = "The password is invalid."
                        return render_template("register.html", id=message)
                for t in twofactor:
                    if not 0<=ord(t)<=127:
                        message = "The two-factor authentication is invalid."
                        return render_template("register.html", id=message)
                if uname not in db:
                    hashedPword = bcrypt.hashpw(pword.encode('utf-8'), salt)
                    hashedtwofac = bcrypt.hashpw(twofactor.encode('utf-8'), salt)
                    db[uname] = {}
                    db[uname]['pword'] = hashedPword
                    db[uname]['twofactor'] = hashedtwofac
                    message = "Registration success!"
                    return render_template("register.html", id=message)
                else:
                    message = "Registration failure."
            return render_template("register.html", id=message)
        elif 'username' in session:
            message = "The account is logged in."
            return render_template("register.html", id=message)


    @app.route("/login", methods=['GET', 'POST'])
    def login():
        result = ""
        if 'username' not in session:
            if request.method == 'POST':
                uname = request.form['uname']
                pword = request.form['pword']
                twofactor = request.form['2fa']

                if (uname is None) or (pword is None):
                    result = "Incorrect username or password."
                    return render_template("login.html", id=result)
                

                if uname not in db:
                    result = "Incorrect username or password."
                else:
                    hashedPword = bcrypt.hashpw(pword.encode('utf-8'), salt)
                    hashedtwofac = bcrypt.hashpw(twofactor.encode('utf-8'),salt)
                    user = db.get(uname, None)
                    if hashedPword != user['pword']:
                        result = "Incorrect username or password."
                        return render_template("login.html", id=result)
                    elif hashedtwofac != user['twofactor']:
                        result = "Two-factor authentication failure."
                        return render_template("login.html", id=result)
                    session.clear()
                    session["username"] = uname
                    result = "Success."
            return render_template("login.html", id=result)

        else:
            result = "The account is logged in."
            return render_template("login.html", id=result)


    @app.route("/spell_check", methods=['GET', 'POST'])
    def spell_check():
        loggedInUser = False
        if 'username' in session:
            loggedInUser = True
            misspelled = None
            textout = None
            if request.method == 'POST':
                textout = request.form["inputtext"]
                f = open("textout.txt", "w")
                f.write(textout)
                f.close()

                misspelled = subprocess.check_output(["./a.out", "textout.txt", "wordlist.txt"])
                misspelled = misspelled.decode('utf-8').strip()
                misspelled = misspelled.replace("\n", ", ")

                os.remove('textout.txt')
            return render_template('spell_check.html', misspelled=misspelled, textout=textout)
        else:
            return render_template("home.html")
        
    @app.route('/logout')
    def logout():
        session.clear()
        loggedout = None
        loggedout = "The user has logged out."
        return render_template('home.html', id=loggedout)
    return app
    
if __name__ == '__main__':
    app.create_app()
    app.run()
