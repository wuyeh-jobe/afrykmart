from flask import Flask, render_template, flash, request, redirect, url_for, session, logging, jsonify  #pip install flask
#from data import Articles
from flask_mysqldb import MySQL  #pip install flask-mysqldb
from wtforms import Form, StringField, TextAreaField, PasswordField, validators  #before this works, pip install flask-wtf
from passlib.hash import sha256_crypt  #before this works, pip install passlib
from functools import wraps
from flask import request
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
@app.route('/login')
def login():
    session['index'] = False
    return render_template("login.html")


#This is for rendering the signup.html template
@app.route('/signup')
def signup():
    session['index'] = False
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


#This is for rendering the shipping.html template
@app.route('/shipping')
def shipping():
    session['index'] = False
    return render_template("shipping.html")


@app.route("/addToCart")
def addToCart():
    p_id = int(request.args.get('product_id'))
    ip_add = request.remote_addr
    qty = 1
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cart (p_id, ip_add, qty) VALUES (?, ?, ?)",
                       (p_id, ip_add, qty))
        msg = "Added successfully"
    except:
        conn.rollback()
        msg = "Error occured"
        conn.close()
    return redirect(url_for('root'))


if __name__ == '__main__':
    app.secret_key = "114455"
    app.run(debug=True)