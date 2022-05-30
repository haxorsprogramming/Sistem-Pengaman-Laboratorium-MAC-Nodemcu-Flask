from flask import Flask, redirect, url_for, render_template, request, jsonify   

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('auth/login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # app.run()