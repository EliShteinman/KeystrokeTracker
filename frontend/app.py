from flask import Flask, render_template

app = Flask(__name__)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/')
def index():
    return render_template('index.html')

# נתיב לדף ניהול המשתמשים
@app.route('/user_management')
def user_management():
    return render_template('user_management.html')

if __name__ == '__main__':
    app.run(port=8001, debug=True)
