from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = "secret_key"

# Create database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
''')

conn.commit()
conn.close()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        username = request.form['username'].strip()
        password = request.form['password']

        if len(username) < 3:
            return "Username must contain at least 3 characters"

        if len(password) < 6:
            return "Password must contain at least 6 characters"

        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        )

        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users(username,password) VALUES (?,?)",
                (username, hashed_password)
            )

            conn.commit()
            conn.close()

            return redirect('/login')

        except:
            return "Username already exists"

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password FROM users WHERE username=?",
            (username,)
        )

        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(
            password.encode('utf-8'),
            user[0]
        ):
            session['user'] = username
            return redirect('/dashboard')

        return "Invalid Username or Password"

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/login')

    return render_template(
        'dashboard.html',
        username=session['user']
    )


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
