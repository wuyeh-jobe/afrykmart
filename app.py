from flask import Flask, render_template, flash, request, redirect, url_for, session, logging, jsonify  #pip install flask
#from data import Articles
from flask_mysqldb import MySQL  #pip install flask-mysqldb
from wtforms import Form, StringField, TextAreaField, PasswordField, validators  #before this works, pip install flask-wtf
from passlib.hash import sha256_crypt  #before this works, pip install passlib
from functools import wraps
from flask import request
import datetime
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
#config db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'afrykmart'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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


@app.route("/addProduct", methods=["GET", "POST"])
def addProduct():
    if request.method == "POST":
        product_cat = request.form['category']
        product_brand = request.form['brand']
        product_title = request.form['title']
        product_price = request.form['price']
        product_desc = request.form['description']
        product_keywords = request.form['keyword']

        #Uploading image procedure
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imagename = filename
            try:
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(
                    '''INSERT INTO products (product_cat, product_brand,product_title, product_price,
                    product_desc, image, product_keywords) VALUES (?, ?, ?, ?, ?, ?,?)''',
                    (product_cat, product_brand, product_title, product_price,
                     product_desc, image, product_keywords))
                conn.commit()
                msg = "added successfully"
            except:
                msg = "error occured"
                conn.rollback()
        conn.close()
        print(msg)
        render_template("index.html")


@app.route("/addToCart")
def addToCart():
    if request.method == "POST":
        p_id = int(request.args.get('product_id'))
        ip_add = request.remote_addr
        qty = 1
        try:

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO cart (p_id, ip_add, qty) VALUES (?, ?, ?)",
                (p_id, ip_add, qty))
            conn.commit()
            msg = "Added successfully"
        except:
            conn.rollback()
            msg = "Error occured"
            conn.close()
    render_template("index.html")


if __name__ == '__main__':
    app.secret_key = "114455"
    app.run(debug=True)

    # https://github.com/BrOrlandi/SFECommerce/commit/441649f3fc4b2fde9816d1a6de28d671ea287f52
    # https://github.com/mohsinenur/menshut