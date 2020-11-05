from flask import Flask, redirect, url_for, escape, flash, render_template, request, session
import calendar
import sqlite3 as sql
import func

app = Flask(__name__)
app.secret_key='p'

@app.route('/')
def index():
    return render_template("index2.html")

"""
@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/signin')
def signin():
    return render_template("signin.html")
"""

@app.route('/signin',methods=["GET","POST"])
def signin():
    if request.method == 'POST': #try:
         u = session['username'] = request.form.get('username')
         p = session['password'] = request.form.get('pwd')
         try:
             with sql.connect(r"C:\Users\Admin\Userdatabase.db") as con:
                 query = "select count(*) from User where UserEmailId = ? and UserPassword = ?"
                 cur = con.cursor()
                 cur.execute(query,(u,p))
                 x=cur.fetchone()
                 print(x)
                 if(x[0]==1):
                    msg="Logged in as:"+u
                    print("LOGGED IN AS : ", u)
                    return render_template("location1.html",msg=msg)
                 else:
                    msg = "Invalid Username or Password !!"
                    print(msg)
                    return render_template('signin.html',msg=msg)
         except:
             print("in except")
             con.rollback()
             print("Error signin!!")
         finally:
             print("in finally")
             con.close()
             print("con closed")
    return render_template('signin.html')


@app.route('/signup',methods=["GET","POST"])
def signup():
    if request.method == 'POST':
        fname = request.form.get('fname',False)
        lname = request.form.get('lname', False)
        email = request.form.get('email', False)
        passwd = request.form.get('pass', False)
        phone = request.form.get('phone', False)
        try:
            with sql.connect(r"C:\Users\Admin\Userdatabase.db") as conn:
                cur = conn.cursor()
                cur.execute('INSERT INTO User VALUES(?,?,?,?,?)',(email,fname,lname,passwd,phone))
                conn.commit()
                print("record inserted")
                print("hello :", fname)
                msg="Account created successfully !!"
                return render_template("signin.html",msg=msg)
        except:
            print("in except")
            conn.rollback()
            print("Error in record insertion !!")
        finally:
            print("in finally")
            conn.close()
            print("conn closed")
    return render_template("signup.html")


@app.route('/index2')
def index2():
    return render_template("index2.html")

@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/location1',methods=["GET","POST"])
def location1():
    print("here")
    if request.method == 'POST':
        u=session['username']
        print(u)
        location = request.form.get('s', False)
        m = request.form.get('m', False)
        print(location)
        print(m)
        month=calendar.month_name[int(m)]
        print(month)
        a = location
        crops = func.f(a, m)
        c = crops.split(',')
        print(c)
        return render_template("result.html",lst=c,user=u,loc=location,month=month)
        return render_template("location1.html")


if __name__ == '__main__':
    app.run(debug=True)