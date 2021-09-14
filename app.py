from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(port=4000, debug=True, use_reloader=True)
