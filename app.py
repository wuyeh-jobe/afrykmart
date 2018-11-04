from flask import Flask, render_template, flash,request, redirect, url_for, session, logging,jsonify #pip install flask
#from data import Articles
from flask_mysqldb import MySQL #pip install flask-mysqldb
from wtforms import Form, StringField, TextAreaField, PasswordField, validators #before this works, pip install flask-wtf
from passlib.hash import sha256_crypt #before this works, pip install passlib
from functools import wraps
import datetime


app = Flask(__name__)
#config db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'afrykmart'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#init MYSQL
mysql = MySQL(app)

#This renders the homepage
@app.route('/')
def index():
    session['index'] = True
    return render_template("index.html")

#This is for rendering the product-page.html template
@app.route('/product')
def product():
    session['index'] = False
    return render_template("product-page.html")

#This is for rendering the products.html template
@app.route('/products')
def products():
    session['index'] = False
    return render_template("products.html")

#This is for rendering the checkout.html template
@app.route('/checkout')
def checkout():
    session['index'] = False
    return render_template("checkout.html")

#This is for rendering the login.html template
@app.route('/login', methods = ["POST","GET"])
def login():
    session['index'] = False
    if request.method == 'POST':
        #get for fields
        email = request.form['email']
        password_given = request.form['password']

        #create cursor
        cur = mysql.connection.cursor()

        #get user by username
        result = cur.execute('Select * from users where email = %s', [email])
        if result > 0:
            data = cur.fetchone()
            password = data['password']
            email = data['email']
            name = data['full_name']
            role = data['role']
            #compare passwords
            if password_given == password:
                #passed
                session['logged_in'] = True
                session['name'] = name
                session['role'] = role
                flash("Logged in as "+name+".",'success')
                if role == "Admin":
                    print("Admin")
                    #return redirect(url_for('update'))
                else:
                    return redirect(url_for('checkout'))
            else:
                error = "Wrong password."
                return render_template('login.html', error=error)
            #close connection
            cur.close()
        else:
            error = "Email not found. Please create a new account if you haven't"
            return render_template('login.html', error=error)        
    return render_template("login.html")

#This is for rendering the signup.html template
@app.route('/signup', methods = ["POST","GET"])
def signup():
    session['index'] = False
    if request.method == "POST":
        name = request.form['fullname']
        gender = request.form['gender']
        dob = request.form['dob']
        email = request.form['email']
        password = request.form['password']
        
        try:
            # prepare update query and data
            query = 'INSERT INTO users (full_name, gender, date_of_birth, email, password) VALUES(%s,%s,%s,%s,%s)'        
            #use cursor
            cur =  mysql.connection.cursor()
            #execute query
            cur.execute(query,(name,gender,dob,email,password))
            #commit DB
            mysql.connection.commit()
            #close connect
            cur.close()
            flash(name+', your account is successfully created!', 'success')
            session['name'] = name
            session['logged_in'] = True
            return redirect(url_for('checkout'))
        except:
            print("Error in adding to database")
    return render_template("signup.html")


#This is for rendering the about.html template
@app.route('/about')
def about():
    session['index'] = False
    return render_template("about.html")

#This is for rendering the faq.html template
@app.route('/faq')
def faq():
    session['index'] = False
    return render_template("faq.html")


#check if logged_in, not be able to go to a link by changing url in bar
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthourized access, please log in', 'danger')
            return redirect('login')
    return wrap



#user logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are logged out', 'success')
    return redirect(url_for('index'))

#This is for rendering the shipping.html template
@app.route('/shipping')
@is_logged_in #Verify that the user is logged before accessing this page
def shipping():
    session['index'] = False
    return render_template("shipping.html")




if __name__ == '__main__':
    app.secret_key = "114455"
    app.run(debug=True)