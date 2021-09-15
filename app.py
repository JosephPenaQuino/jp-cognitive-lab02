from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'sql10.freemysqlhosting.net' 
app.config['MYSQL_USER'] = 'sql10437299'
app.config['MYSQL_PASSWORD'] = 'jFwnNf68jz'
app.config['MYSQL_DB'] = 'sql10437299'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', users=data)

@app.route('/add_users', methods=['POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, lastname) VALUES (%s,%s)", (name, lastname))
        mysql.connection.commit()
        flash('User Added successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_user(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-user.html', user = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_user(id):
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE users
            SET name = %s,
                lastname = %s,
            WHERE id = %s
        """, (name, lastname, id))
        flash('User Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM users WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('User Removed Successfully')
    return redirect(url_for('Index'))

# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
