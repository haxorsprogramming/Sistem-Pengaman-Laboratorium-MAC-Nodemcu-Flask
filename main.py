from flask import Flask, redirect, url_for, render_template, request, jsonify   
import jwt

app = Flask(__name__)

secret_key = "LFFDssr63U4LYbUf"

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # app.run()