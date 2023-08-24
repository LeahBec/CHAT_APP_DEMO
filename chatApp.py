from flask import Flask, render_template, redirect, url_for, request, session
import csv
import os
# import requests
import urllib.parse
from datetime import datetime

app = Flask(__name__)
ROOMS = []
app.secret_key="secret_key"
# file_path = "ROOMS/{}.txt"


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
            file_path = "ROOMS/{}.txt".format(new_room)
            try:
                  if not os.path.isdir("ROOMS"):
                      os.makedirs("ROOMS")
                  if not os.path.isfile(file_path):
                    with open(file_path, "w") as file:
                        file.write("Hello, this is some text. {}\n".format(new_room))
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



# @app.route('/chat/<room_name>')
# def chat(room_name):
#     if request.method == "POST":
#         return "sent"
#         file_path = "./os.getenv('ROOMS_DIR'){}.txt".format(room_name)
#     return render_template('chat.html', room=room_name)
@app.route('/chat/<room_name>', methods=['GET', 'POST'])
def chat(room_name):
        return render_template('chat.html', room=room_name)

@app.route('/api/chat/<room_name>', methods=['GET', 'POST'])
def update_chat(room_name):
        file_path = "ROOMS/{}.txt".format(room_name)
        print("{}".format(room_name))
        if request.method == "POST":
            
            print("aaa")
            message = request.form['msg']
            username = session['username']
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # Append the message to the room's unique .txt file
            with open(file_path, 'a') as file:
                            file.write(f'[{timestamp}] {username}: {message}\n')
        with open(file_path, 'r') as file:
            file.seek(0)
            all_data = file.read()
            return all_data


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port='5000', debug='True')



