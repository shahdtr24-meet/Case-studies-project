from flask import Flask, render_template, request, redirect, url_for, session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['SECRET_KEY'] = 'super-secret-key'

Config = {
    "apiKey": "AIzaSyBpc13ioYehbcERu97K_hunUAUGrmFnucw",
    "authDomain": "ecopeaceb5.firebaseapp.com",
    "databaseURL": "https://ecopeaceb5-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "ecopeaceb5",
    "storageBucket": "ecopeaceb5.appspot.com",
    "messagingSenderId": "1008058043324",
    "appId": "1:1008058043324:web:beb2da532082f2d4c739b9"
}

firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db = firebase.database()

@app.route('/' , methods = ["GET" , "POST"])
def main():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            session['user'] = user
            UID = session['user']['localId']
            info = {"email": email, "password": password}
            db.child('users').child(UID).set(info)
            return redirect(url_for('main'))
        except:
            return 'Error creating account'
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user
            return redirect(url_for('main'))
        except:
            return 'Error signing in'
    return render_template('signin.html')

@app.route('/signout')
def signout():
    session.pop('user', None)
    return redirect(url_for('signin'))

@app.route('/profile')
def profile():
    if 'user' in session:
        UID = session['user']['localId']
        user_data = db.child('users').child(UID).get().val()
        email = user_data['email']
        password = user_data['password']
        return render_template('profile.html', email=email , password= password )
    return redirect(url_for('signin'))



@app.route('/feedback' , methods = ["GET" , "POST"])
def feedback():
    if request.method == 'POST':
        print('meow')
        feedback = request.form['feedback']
        fb = { "feedback" : feedback}
        UID = session['user']['localId']
        db.child('feedback').child(UID).set(fb)
        info = db.child("feedback").get().val()

        print('send help')
        print(info)
        return redirect(url_for('main'))
    return render_template('about.html')



if __name__ == '__main__':
    app.run(debug=True)
