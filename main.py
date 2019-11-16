import logging
import pyrebase
import pymysql
import pymysql.cursors
from flask import *

app = Flask(__name__)

firebaseConfig = { 
    'apiKey':"AIzaSyADsG358b27DZnVi5puA_wSvrBwCWPNf0o",
    'authDomain': "rewardmeasure.firebaseapp.com",
    'databaseURL': "https://rewardmeasure.firebaseio.com",
    'projectId': "rewardmeasure",
    'storageBucket': "rewardmeasure.appspot.com",
    'messagingSenderId': "615142054910",
    'appId': "1:615142054910:web:b7db88b965703c302b3eaf",
    'measurementId': "G-9VKVFYBJZV"
  }

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()

# def db_connection:
#     db_user = 'root'
#     db_password = '123456'
#     db_name = "point_system_2"
#     db_connection_name = 'rewardmeasure:us-central1:measureward2'


#     host = '127.0.0.1'
#     con = pymysql.connect(user=db_user,port=5432, password=db_password,host = host, db=db_name)
#     with con:
#         cur =con.cursor()
#         cur.execute("select * from user;")
#         output = cur.fetchall()
#         if not output:
#             print("empty")
#         else:
#             print(output)
#         print("test done!")


@app.route('/', methods = ['POST','GET'])
def hello():
    # return 'Hello World!'
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['pass']
        try:
            auth.create_user_with_email_and_password(email,password)
            return "sucessful"
        except expression as identifier:
            return expression
    else:
        db_user = 'root'
        db_password = '123456'
        db_name = "point_system_2"
        db_connection_name = 'rewardmeasure:us-central1:measureward2'
        unix_socket = '/cloudsql/{}'.format(db_connection_name)

        host = '127.0.0.1'
        con = pymysql.connect(user=db_user, password=db_password,unix_socket=unix_socket,host = host, db=db_name)
        with con:
            cur =con.cursor()
            cur.execute("select * from user;")
            output = cur.fetchall()
            if not output:
                print("empty")
                return "empty"
            else:
                print(output)
                return "something"
            print("test done!")
            # return render_template("test.html")
        con.close()
        # return "test"


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)