from flask import Flask, render_template, redirect, url_for, request
import csv
app = Flask(__name__)
USERS={}

# @app.route('/')
# def homePage():
#     return render_template('register.html')
@app.route('/', methods=['GET', 'POST'])
def homePage():
    error = None
    is_registered = False
    name = request.form['username']
    password = request.form['password']
    with open('users.csv', 'r') as myFile:
        myReader = csv.reader(myFile)
        for user in myReader:
            if user == name:
                is_registered = True
        if name =
    # if request.method == "POST":
    #     name = request.form['username']
    #     password = request.form['password']
    #     return f"your name is {name} and your pass is {password}"
            #return render_template("login.html")
    # if request.form['username'] != 'admin' or request.form['password'] != 'admin':
    #     error = 'Invalid Credentials. Please try again.'
    # else:
    #     return redirect(url_for('homePage'))
    return render_template('register.html', error=error)

def main():
     myList = []
with open('users.csv', 'r') as myFile:
    myReader = csv.reader(myFile)
    myList = list(myReader)
    
print(myList)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port='5000', debug='True')



