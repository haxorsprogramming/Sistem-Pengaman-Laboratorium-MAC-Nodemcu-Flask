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

@app.route('/dashboard/beranda')
def beranda():
    return render_template('main/beranda.html')

@app.route('/mahasiswa/data')
def mahasiswaData():
    mycursor.execute("SELECT * FROM tbl_mahasiswa")
    myresult = mycursor.fetchall()
    container = []
    ord = 1
    for x in myresult:
        mhs = {}
        mhs['no'] = ord
        mhs['kdMhs'] = x[1]
        mhs['nama'] = x[2]
        mhs['jk'] = x[3]
        mhs['prodi'] = x[4]
        mhs['nim'] = x[5]
        ord += 1
        container.append(mhs)
    return render_template('main/mahasiswa/mahasiswa.html', container=container)

@app.route('/mahasiswa/tambah/proses', methods = ['POST', 'GET'])
def mahasiswaTambahProses():
    kdMahasiswa = ''.join(random.choices(string.ascii_lowercase, k=7))
    context = {
        'status' : 'sukses',
        'kdMhs' : kdMahasiswa
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