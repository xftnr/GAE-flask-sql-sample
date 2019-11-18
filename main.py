import logging
import pyrebase
import pymysql
import pymysql.cursors
from flask import *
from datetime import datetime
from dateutil.relativedelta import relativedelta

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

# database connection
def db_connection():
    # hidden from the public
    db_user = 'root'
    db_password = '123456'
    db_name = "rewardmeasure2"
    db_connection_name = 'rewardmeasure:us-central1:measureward2'
    unix_socket = '/cloudsql/{}'.format(db_connection_name)

    host = '127.0.0.1'
    con = pymysql.connect(user=db_user, password=db_password, unix_socket=unix_socket,host = host, db=db_name)
    # con = pymysql.connect(user=db_user, password=db_password,port= 5432,host = host, db=db_name)
    return con

@app.route('/', methods = ['POST','GET'])
def hello():
    # return 'Hello World!'
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['pass']
        try:
            user = auth.sign_in_with_email_and_password(email,password)
            print(user)
            email = auth.get_account_info(user['idToken'])['users'][0]['email']
            con = db_connection()
            with con.cursor() as cur:
                query = "select username, role from users where email=%s"
                cur.execute(query,email)
                (name, role) = cur.fetchone()
                cur.close()
            con.close()
            if role == "admin":
                return redirect(url_for('admin_page'))

            elif role == "user":
                return redirect(url_for('user_page',name=name))
                # redirect('/user_page')
            else:
                return "Ask admin for access!"

        except Exception as e:
            return "Login unsuccessful, Contact the Admin."
    else:
        return render_template("index.html")


@app.route('/user_page/<name>', methods = ['GET','POST'])
def user_page(name):
    if request.method == 'POST':
        # name = request.args.get('name')
        receiver = request.form['receiver']
        amount = int(request.form['amount'])
        message = request.form['message']
        # limit the message length
        message = message[:200]
        con = db_connection()
        with con.cursor() as cur:
            # check the left over points
            # print(request.args.get('name'))
            query = f"select to_give from account where username = '{name}'"
            cur.execute(query)
            leftover = int(cur.fetchall()[0][0])
            if leftover < amount:
                return "No enough points"
            # check the receiver
            query2 = f"select username from users where username !='{name}' "
            cur.execute(query2)
            receiverlist = list(cur.fetchall())
            if (receiver,) not in receiverlist:
                return "Cannot find Receiver"
            # Good to insert
            # insert the trasaction
            now = datetime.now()
            timestamp = now.strftime("%Y%m%d%H%M%S")
            query3 = f"INSERT INTO transaction(sender, receiver, timestamp, amount, message) VALUES ('{name}', '{receiver}',{timestamp}, {amount}, '{message}')"
            cur.execute(query3)
            # update the user 
            newbalance = leftover - amount
            query4 = f"UPDATE account SET to_give = {newbalance} where username = '{name}';"
            cur.execute(query4)
            # update the receiver
            query5 = f"select to_receive from account where username='{receiver}'"
            cur.execute(query5)
            # print(cur.fetchone()[0])
            receive = int(cur.fetchone()[0])
            newincome = receive + amount
            query6 = f"UPDATE account SET to_receive = {newincome} where username = '{receiver}';"
            cur.execute(query6)
            cur.close()
        con.commit()
        con.close()
        return redirect(url_for('user_page',name=name))

    else:
        #query things
        con = db_connection()
        with con.cursor() as cur:
            # query for transaction
            query = f"select * from transaction where sender='{name}' or receiver = '{name}'"
            cur.execute(query)
            transcation = list(cur.fetchall())
            # query for personal info
            query2 = f"select * from account where username= '{name}'"
            cur.execute(query2)
            personalinfo = list(cur.fetchone())
            cur.close()
        con.close()
        return render_template("userpage.html", username = name, package = transcation, info = personalinfo)


@app.route('/admin_page', methods = ['GET','POST'])
def admin_page():
    if request.method == 'POST':
        con = db_connection()
        with con.cursor() as cur:
            # query for transaction
            query = "UPDATE account set to_give = 1000, to_receive = 0, to_redeem = 0"
            cur.execute(query)
            cur.close()
        con.commit()
        con.close()
        return redirect(url_for('admin_page'))

    else:
        con = db_connection()
        with con.cursor() as cur:
            # query for transaction
            query = "select * from account"
            cur.execute(query)
            allaccountinfo = list(cur.fetchall())
            # query for personal info
            query2 = f"select * from redemption"
            cur.execute(query2)
            redeem = list(cur.fetchall())
            cur.close()
        con.close()
        # handle the all account info
        package1 = []
        package2 = []
        for i in allaccountinfo:
            temp =[]
            temp.append(i[0])
            temp.append(i[2])
            temp.append(1000-i[1])
            package1.append(temp)
            temp2 = []
            temp2.append(i[0])
            temp2.append(i[1])
            package2.append(temp2)
        package1 = sorted(package1, key = lambda x: x[1], reverse= True)
        # handle the redeem
        package3 = []
        for i in redeem:
            if i[1]+relativedelta(months=+3) > datetime.now():
                package3.append(i)
        return render_template("adminpage.html", package1 =package1, package2=package2, package3=package3)




# datebase testing purpose
@app.route('/db_test', methods = ['GET'])
def db_test():
    result = ""
    con = db_connection()
    with con.cursor() as cur:
        query = "select username, role from users"
        cur.execute(query)
        result = cur.fetchone()
        cur.close()
    con.close()
    if not result:
        return "No connection"
    else:
        return "OK"





@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)