from flask import Flask, redirect,render_template,url_for,request,session
from flask import flash
from flask_mysqldb import MySQL


app=Flask(__name__)


app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="crud"

mysql=MySQL(app)


app.secret_key="layton"


@app.route('/')
def  home():
     cur=mysql.connection.cursor()
     cur.execute("SELECT * FROM employee")
     data=cur.fetchall()
     
     return render_template('index.html',employee=data)

@app.route('/add',methods=['POST','GET'])
def add():
       if request.method=='POST':
          name=request.form['name']
          email=request.form['email']
          number=request.form['number']

          cur=mysql.connection.cursor()
          cur.execute("INSERT INTO employee (name,email,number)VALUES(%s,%s,%s)",(name,email,number))
          flash("A new employee added successfully")
          mysql.connection.commit()
          cur.close()
          return redirect(url_for('home'))
       return render_template('add.html')
 
 
@app.route('/update/<id>', methods=['POST', 'GET'])
def update(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employee WHERE id=%s", (id,))
    data = cur.fetchone()
    cur.close()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        number = request.form['number']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE employee SET name=%s, email=%s, number=%s WHERE id=%s", (name, email, number, id))
        mysql.connection.commit()
        cur.close()
        flash("Employee updated successfully", "info")
        return redirect(url_for("home"))
    return render_template('update.html', data=data)


@app.route('/delete/<id>')
def delete(id):
     cur=mysql.connection.cursor()
     cur.execute("DELETE FROM employee WHERE id=%s",(id,))
     mysql.connection.commit()
     cur.close()
     return redirect(url_for('home'))    


if __name__=='__main__':
 app.run(debug=True)