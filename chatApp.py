from flask import Flask, render_template, redirect, url_for, request, session
import csv
import os
# import requests
import urllib.parse
from datetime import datetime
import base64

app = Flask(__name__)
ROOMS = []
app.secret_key="secret_key"


def encode_password(user_pass):
    pass_bytes = user_pass.encode('ascii')
    base64_bytes = base64.b64encode(pass_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message


def decode_password(user_pass):
     base64_bytes = user_pass.encode('ascii')
     pass_bytes = base64.b64decode(base64_bytes)
     user_pass = pass_bytes.decode('ascii')
     return user_pass


def is_registered(name):
    with open('users.csv', 'r') as myFile:
            myReader = csv.reader(myFile)
            for line in myReader:
                if line[0] == name:
                     return True
                

def register_user(name, password):
      with open('users.csv', 'a') as myFile:
            writer = csv.writer(myFile)
            writer.writerow([name, encode_password(password)])


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
                if line[0] == name and decode_password(line[1]) == password:
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
            return redirect('login')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('register.html')


@app.route('/lobby', methods=['GET', 'POST'])
def lobby():
    if request.method == "POST":
        new_room = request.form['new_room']
        if new_room not in ROOMS:
            ROOMS.append(new_room)
            print(ROOMS)
            file_path = "os.getenv('ROOMS_DIR'){}.txt".format(new_room)
            try:
                  if not os.path.isdir("ROOMS"):
                      os.makedirs("ROOMS")
                  if not os.path.isfile(file_path):
                    with open(file_path, "w") as file:
                        file.write("Hello, you are in room: {}\n".format(new_room))
                # with open(file_path, "r+") as file:
                #     txt = fdofile.read()
                #     return txt
            except FileNotFoundError:
                return "File not found."
            else:
                return redirect('chat/{}'.format(new_room))
        else:
            print("The room name is occupied")
            return "The room name is occupied"
    return render_template('lobby.html', room_names=ROOMS)

def extract_filename():
    link = request.META['HTTP_REFERER']
    parsed_link = urllib.parse.urlparse(link)
    filename = parsed_link.path.split("/")[-1]

    return filename


@app.route('/chat/<room_name>', methods=['GET', 'POST'])
def chat(room_name):
        return render_template('chat.html', room=room_name)

@app.route('/api/chat/<room_name>', methods=['GET', 'POST'])
def update_msg(room_name):
        file_path = "os.getenv('ROOMS_DIR'){}.txt".format(room_name)
        if request.method == "POST":
            msg = request.form['msg']
            username = session['username']
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(file_path, 'a') as file:
                file.write(f'[{timestamp}] {username}: {msg}\n')
        with open(file_path, 'r') as file:
            file.seek(0)
            massages = file.read()
            return massages


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port='5000', debug='True')



