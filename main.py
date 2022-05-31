from flask import Flask, redirect, url_for, render_template, request, jsonify   
import jwt
from matplotlib.style import context
import mysql.connector
import random
import string

app = Flask(__name__)

secret_key = "LFFDssr63U4LYbUf"

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="dbs_yaser"
)
#fungsi koneksi database
mycursor = mydb.cursor()


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
    mycursor.execute("SELECT * FROM tbl_mahasiswa")
    myresult = mycursor.fetchall()
    container = []
    for x in myresult:
        mhs = {}
        mhs['nama'] = x[2]
        mhs['jk'] = x[3]
        mhs['prodi'] = x[4]
        mhs['nim'] = x[5]
        container.append(mhs)
        # print(x[2])
    
    context = {
        'mahasiswa' : container
    }
    return jsonify(context)

@app.route('/data-mahasiswa/tambah/proses', methods = ['POST', 'GET'])
def prosesTambahMahasiswa():
    kdMahasiswa = ''.join(random.choices(string.ascii_lowercase, k=7))
    namaMhs = request.form['namaMhs']
    jk = request.form['jk']
    prodi = request.form['prodi']
    nim = request.form['nim']
    sql = "INSERT INTO tbl_mahasiswa (kd_mahasiswa, nama_mahasiswa, jk, prodi, nim) VALUES (%s, %s, %s, %s, %s)"
    val = (kdMahasiswa, namaMhs, jk, prodi, nim)
    mycursor.execute(sql, val)
    mydb.commit()

    context = {
        'status' : 'sukses',
        'kdMhs' : kdMahasiswa
    }
    return jsonify(context)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # app.run()