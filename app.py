from flask import Flask, render_template, flash,request, redirect, url_for, session, logging,jsonify #pip install flask
#from data import Articles
from flask_mysqldb import MySQL #pip install flask-mysqldb
from wtforms import Form, StringField, TextAreaField, PasswordField, validators #before this works, pip install flask-wtf
from passlib.hash import sha256_crypt #before this works, pip install passlib
from functools import wraps
import datetime
import json


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
    #This gets the featured products and pass them to the index page
    featuredProducts1 = getProducts("SELECT * FROM products INNER JOIN categories ON products.product_id = categories.cat_id limit 3")
    #This gets the featured products and pass them to the index page
    featuredProducts2 = getProducts("SELECT * FROM products INNER JOIN categories ON products.product_id = categories.cat_id limit 3")
    #This gets the latest products and pass them to the index page
    latestProducts = getProducts("SELECT * FROM products INNER JOIN categories ON products.product_id = categories.cat_id limit 3")
    #This gets the picked products and pass them to the index page
    pickedProducts = getProducts("SELECT * FROM products INNER JOIN categories ON products.product_id = categories.cat_id limit 3")
    
    
    allProducts = getProducts("SELECT * FROM products INNER JOIN categories ON products.product_id = categories.cat_id")
    return render_template("index.html",fp = featuredProducts1, fp2 = featuredProducts2, lp = latestProducts,  ap = allProducts, pp = pickedProducts)

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
        cpassword = request.form['confirmPassword'];
        
        if(cpassword == password):        
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
        else:
            flash('Passwords do not match', 'danger')
            
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

#This is for rendering the template for admin
@app.route('/admin')
def index_admin():
    session['index'] = False
    return render_template("index_admin.html")

#This is for rendering the orders.html template
@app.route('/orders')
def orders():
    session['index'] = False
    return render_template("orders.html")

#This is for rendering the product_mgt.html template
@app.route('/product_mgt')
def product_mgt():
    session['index'] = False
    return render_template("product_mgt.html")

#This is for rendering the users_details.html template
@app.route('/users_details')
def users_details():
    session['index'] = False
    return render_template("users_details.html")

#This is for rendering the admin_login.html template
@app.route('/admin_login')
def admin_login():
    session['index'] = False
    return render_template("admin_login.html")



#This function for search the products available.
@app.route("/search")
def search():
    searchText = request.args['searchText'] # get the text to search for
    text = "%" + request.args['searchText'] + "%" 
	# create an array with the query
     #create cursor
    cur = mysql.connection.cursor()
        #get user by username
    qresult = cur.execute("SELECT * FROM products WHERE product_title LIKE  %s", [text])
	# Get the data returned by the query
    all_data = cur.fetchall()
    
    
    result =  [c['product_title'] for c in all_data if searchText.lower() in c['product_title'].lower()]
    #print(result)
    cur.close()
	# return as JSON
    return json.dumps({"results":result}) 

#This function is to add tp cart.
@app.route("/addToCart")
def addToCart():
    product_id = request.args['product_id'] # get product id
    action = request.args['action'] # get action
    print(type(action))
     #create cursor
    ip_add = request.remote_addr
    print(ip_add)
    cur = mysql.connection.cursor()
    if product_id != -1:
                #use cursor
        cur2 =  mysql.connection.cursor()
        result = cur.execute("SELECT * FROM cart")
        if (result==0):
            query = 'INSERT INTO cart (p_id, ip_add, qty) VALUES (%s,%s,%s)' 
                #execute query
            cur2.execute(query,(product_id,ip_add,1))
                #commit DB
            mysql.connection.commit()
            cur2.close()
        for data in cur.fetchall():
            cur3 =  mysql.connection.cursor()
            qty = data["qty"]
            query = ""
            if data["p_id"] == int(product_id) and data["ip_add"]==ip_add:
                #-50 is used to denote if a user wants to add to cart
                if action=="-50":
                    qty = qty+1
                    query = "UPDATE cart SET qty = %s where p_id= %s"
                    cur3.execute(query,(qty,data["p_id"]))
                else:
                    qty = qty-1
                    query = "UPDATE cart SET qty = %s where p_id= %s"
                    cur3.execute(query,(qty,data["p_id"]))

            else:
                query = "INSERT INTO cart (p_id, ip_add, qty) VALUES (%s,%s,%s)"
                cur3.execute(query,(product_id,ip_add,1))
            mysql.connection.commit()
            cur3.close()

        cur.execute("DELETE FROM cart WHERE qty = -1")
        mysql.connection.commit()


    stmt = cur.execute("SELECT qty, product_price, product_title, p_id FROM cart , products where p_id=product_id")
    result2 = cur.fetchall()
    outp = [str(c['qty']) + str(c['product_price']) + c['product_title'] + str(c['p_id']) for c in result2]
    #print(result2)
    cur.close()
	# return as JSON
    return json.dumps({"results":result}) 

def getProducts(query):
    products = []
    #create cursor
    cur = mysql.connection.cursor()
    result = cur.execute(query)
    all_data = cur.fetchall()
    for data in all_data:
        product_id = str(data['product_id'])
        product_cat = data['cat_name']
        #product_brand = data['brand_name']
        product_title = data['product_title']
        product_price= str(data['product_price'])
        product_desc = data['product_desc']
        product_image= data['product_image']
        product_desc = data['product_keywords']
        #print(product_image)
        products.append(product_id+"#"+product_cat+"#"+product_title+"#"+product_price+"#"+product_desc+"#"+product_image+"#"+product_desc)
    return products
        
        
        
    
    
    
    
    


if __name__ == '__main__':
    app.secret_key = "114455"
    app.run(debug=True)