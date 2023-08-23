from flask import Flask, render_template, redirect, url_for, request, session
import csv
app = Flask(__name__)
app.secret_key="secret_key"

# @app.route('/')
# def homePage():
#     return render_template('register.html')
def is_registered(name):
    with open('users.csv', 'r') as myFile:
            myReader = csv.reader(myFile)
            for line in myReader:
                if line[0] == name:
                     return True
                


def register_user(name, password):
      with open('users.csv', 'a') as myFile:
            writer = csv.writer(myFile)
            writer.writerow([name, password])
@app.route('/register', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def homePage():   
    error = None
    if request.method == "POST":
     
        name = request.form['username']
        password = request.form['password']
        if is_registered(name):
            return redirect('login')
        else:
            register_user(name, password)
            return redirect('login')
    return render_template('register.html', error=error)


def is_right_pass(name, password):
         with open('users.csv', 'r') as myFile:
            myReader = csv.reader(myFile)
            for line in myReader:
                if line[0] == name and line[1] == password:
                     return True
         return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
     
        name = request.form['username']
        password = request.form['password']
        if is_right_pass(name, password):
            session['username'] = name
            return redirect('lobby')
        else:
            return "wrong pass!"
    return render_template('login.html')





if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port='5000', debug='True')



