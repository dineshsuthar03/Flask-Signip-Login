from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

client = MongoClient("mongodb://localhost:27017/")
db = client["your_database_name"]
users = db["users"]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        print(fullname,email,password,confirm_password)
        print(type(password))
        if str(password) == str(confirm_password):        
            
            password = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            users.insert_one({'fullname': fullname,'email':email, 'password': hashed_password})
            print(email,password)
            return redirect(url_for('login'))
        elif str(password) != str(confirm_password):
            print("Password not same")
            render_template('register.html')
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        user = users.find_one({'username': username})
        if user and bcrypt.checkpw(password, user['password']):
            session['username'] = username
            return redirect(url_for('protected'))
    return render_template('login.html')

@app.route('/protected')
def protected():
    if 'username' in session:
        return render_template('protected.html')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
