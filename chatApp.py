from flask import Flask, render_template, redirect, url_for, request
import csv
import os
# import requests
import urllib.parse

app = Flask(__name__)
ROOMS = []
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
            writer.writerow([name, password.encode])


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



@app.route('/lobby', methods=['GET', 'POST'])
def lobby():
    if request.method == "POST":
        new_room = request.form['new_room']
        if new_room not in ROOMS:
            ROOMS.append(new_room)
            print(ROOMS)
            file_path = "ROOMS/{}.txt".format(new_room)
            try:
                # if not os.path.isdir("ROOMS"):
                #     os.makedirs("ROOMS")
                if not os.path.isfile(file_path):
                    with open(file_path, "w") as file:
                        file.write("Hello, this is some text. {}\n".format(new_room))
                # with open(file_path, "r+") as file:
                #     txt = file.read()
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




@app.route('/chat/<room_name>')
def chat(room_name):
    if request.method == "POST":
        get_msg = request.form['msg']
        room =extract_filename()
        return "room {}".format(room)
        file_path = "./ROOMS/{}.txt".format(room)
    return render_template('chat.html', room=room_name)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port='5000', debug='True')



