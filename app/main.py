from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def hello():
    message = os.environ.get('MESSAGE', 'Olá, Kubernetes!')
    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

