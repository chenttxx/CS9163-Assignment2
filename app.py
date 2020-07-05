from flask import Flask, request, session, render_template, redirect, url_for
import os
import subprocess
##from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
db = {}
dict = "wordlist.txt"
##csrf = CSRFProtect(app)
app.secret_key = os.urandom(24)


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
            if uname not in db:
                db[uname] = {}
                db[uname]['pword'] = pword
                db[uname]['twofactor'] = twofactor
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
                user = db.get(uname, None)
                if pword != user['pword']:
                    result = "Incorrect username or password."
                    return render_template("login.html", id=result)
                elif twofactor != user['twofactor']:
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
            f = open("textout.txt", "w"):
            f.write(textout)
            f.close()
  
            misspelled = subprocess.check_output(["./a.out", "textout.txt", "wordlist.txt"])
            misspelled = misspelled.decode('utf-8').strip()
            misspelled = misspelled.replace("\n", ", ")

            os.remove('textout.txt')
        return render_template('spell_check.html', misspelled=misspelled, textout=textout)
    else:
        return redirect(url_for("home"))
@app.route('/logout')
def logout():
    session.clear()
    loggedout = None
    loggedout = "The user has logged out."
    return render_template('home.html', id=loggedout)

if __name__ == '__main__':
    app.create_app()
