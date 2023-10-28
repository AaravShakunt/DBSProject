from flask import Flask, Response, render_template, request, jsonify
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import psycopg2
import requests
import os

conn = psycopg2.connect(
     host="db.eoehrierllfhmxlltdyf.supabase.co",
     database="postgres",
     user="postgres",
     password="Mhash@win576"
 )

# # Create a cursor object
cur = conn.cursor()

# # Execute a query
# cur.execute("SELECT * FROM your_table")

# # Fetch the results
# results = cur.fetchall()

# # Close the cursor and connection
# cur.close()
# conn.close()

app = Flask(__name__)
OUTPUT_FOLDER = 'static'
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER



conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="Mhash@win576",
    host="db.eoehrierllfhmxlltdyf.supabase.co",
    port="5432"
)

userid = 0

@app.route('/')
def redirect_to_home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE emailid = %s AND password = %s", (email, password))
        user = cur.fetchone()
        print(user)
        global login_data
        login_data = user
        print(login_data)
        conn.commit()
        cur.close()
        if user:
            return render_template('index.html')
        else:
            return render_template('invalidlogin.html')
    return render_template('login.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/student.html')
def student_page():
    return render_template('student.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        dob = request.form['date']
        type = request.form['usertype']

        cur = conn.cursor()
        cur.execute("INSERT INTO users (emailid, password,type,name,phoneno,dob) VALUES (%s, %s,%s,%s,%s,%s)", (email, password,type,name,phone,dob))
        conn.commit()
        cur.execute("SELECT userid FROM users WHERE emailid = %s AND password = %s", (email, password))
        global userid
        userid = cur.fetchone()
        if(type == "student"):
            return redirect('/studentregister')
        if(type == "startup owner"):
            return redirect('/startupregister')
        if(type == "investor"):
            return redirect('/investorregister')

    return render_template('register.html')

@app.route('/studentregister', methods=['GET', 'POST'])
def studentregister():
    if request.method == 'POST':
        branch = request.form['branch']
        cgpa = request.form['cgpa']
        domain = request.form['domain']
        regno = request.form['regno']

        cur = conn.cursor()
        cur.execute("INSERT INTO students (userid, branch, cgpa, interest_domain,regno) VALUES (%s,%s, %s,%s,%s)", (userid,branch, cgpa,domain,regno))
        conn.commit()
        cur.close()
        return render_template('registersucess.html')

    return render_template('studentregister.html')

@app.route('/startupregister', methods=['GET', 'POST'])
def startupregister():
    if request.method == 'POST':
        valuation = request.form['valuation']
        revenue = request.form['revenue']
        #approvalstatus = request.form['approval']
        investmentraised = request.form['investment']
        companyname = request.form['cname']

        cur = conn.cursor()
        cur.execute("INSERT INTO startupowner (userid, company_name) VALUES (%s,%s)", (userid,companyname))
        cur.execute("INSERT INTO company (valuation, ownerid, revenue, approvalstatus, investmentraised,companyname) VALUES (%s,%s, %s,%s,%s,%s)", (valuation,userid, revenue,'approved',investmentraised,companyname))
        conn.commit()
        cur.close()
        return render_template('registersucess.html')

    return render_template('startupregister.html')

@app.route('/investorregister', methods=['GET', 'POST'])
def investorregister():
    if request.method == 'POST':
        firm_name = request.form['fname']

        cur = conn.cursor()
        cur.execute("INSERT INTO investor (userid, firm_name) VALUES (%s,%s)", (userid,firm_name))
        conn.commit()
        cur.close()
        return render_template('registersucess.html')

    return render_template('investorregister.html')

@app.route('/profile.html')
def profile():
    return render_template('profile.html', data = login_data)

if __name__ == '__main__':
    app.run(debug=True)
 