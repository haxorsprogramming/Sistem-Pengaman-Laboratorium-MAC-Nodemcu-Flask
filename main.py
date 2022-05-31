from flask import Flask, redirect, url_for, render_template, request, jsonify   
import jwt
from matplotlib.style import context
import pymysql.cursors, os

app = Flask(__name__)

secret_key = "LFFDssr63U4LYbUf"

conn = cursor = None
#fungsi koneksi database
def openDb():
   global conn, cursor
   conn = pymysql.connect("127.0.0.1","root","","dbs_yaser")
   cursor = conn.cursor()

def closeDb():
   global conn, cursor
   cursor.close()
   conn.close()


@app.route('/')
def index():
    return render_template('auth/login.html')

@app.route('/auth/login/proses', methods = ['POST', 'GET'])
def loginProses():
    username = request.form['username']
    password = request.form['password']
    payload = {'username':username}

    if username == 'admin' and password == 'admin':
        status = 'sukses'
    else:
        status = 'gagal'

    token = jwt.encode(payload, secret_key, algorithm="HS256")
    context = {
        'status' : status,
        'username' : username,
        'token' : token
    }
    return jsonify(context)

@app.route('/dashboard')
def dashboard():
    return render_template('main/dashboard.html')

@app.route('/data-mahasiswa')
def dataMahasiswa():
    openDb()
    container = []
    sql = "SELECT * FROM tbl_mahasiswa;"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
      container.append(data)
    closeDb()
    context = {
        'mahasiswa' : container
    }
    return jsonify(context)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # app.run()