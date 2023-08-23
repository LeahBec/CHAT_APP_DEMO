from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

# @app.route('/')
# def homePage():
#     return render_template('register.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port='5000', debug='True')



@app.route('/', methods=['POST'])
def homePage():
    error = None
    name = request.form['username']
    password = request.form['password']
    # if request.form['username'] != 'admin' or request.form['password'] != 'admin':
    #     error = 'Invalid Credentials. Please try again.'
    # else:
    #     return redirect(url_for('homePage'))
    return render_template('register.html', error=error)