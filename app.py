from flask import Flask, render_template, flash, request, redirect, url_for, session, logging, jsonify  #pip install flask
#from data import Articles
from flask_mysqldb import MySQL  #pip install flask-mysqldb
from wtforms import Form, StringField, TextAreaField, PasswordField, validators  #before this works, pip install flask-wtf
from passlib.hash import sha256_crypt  #before this works, pip install passlib
from functools import wraps
from flask import request
import datetime
import json
from werkzeug.utils import secure_filename
import os
from flask_mail import Mail, Message


app = Flask(__name__)

app.secret_key = "114455"

#config db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'afrykmart'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


#Email Configuration should be here

mail = Mail(app)


# UPLOAD_FOLDER = os.path.basename('static/img')
# ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app_root = os.path.dirname(os.path.abspath(__file__))

#init MYSQL
mysql = MySQL(app)


from werkzeug.datastructures import ImmutableOrderedMultiDict
import requests


#This renders the homepage
@app.route('/')
def index():
    session['index'] = True
    #This gets the featured products and pass them to the index page
    featuredProducts1 = getProducts(
        "SELECT * FROM products INNER JOIN categories ON products.product_id = categories.cat_id ORDER BY RAND() limit 5"
    )
    #This gets the featured products and pass them to the index page
    featuredProducts2 = getProducts(
        "SELECT * FROM products INNER JOIN categories ON products.product_id = categories.cat_id ORDER BY RAND() limit 4"
    )
    #This gets the latest products and pass them to the index page
    latestProducts = getProducts(
        "SELECT * FROM products INNER JOIN categories ON products.product_id = categories.cat_id ORDER BY RAND() limit 4"
    )
    #This gets the picked products and pass them to the index page
    pickedProducts = getProducts(
        "SELECT * FROM products INNER JOIN categories ON products.product_id = categories.cat_id ORDER BY RAND() limit 4"
    )

    allProducts = getProducts(
        "SELECT * FROM products INNER JOIN categories ON products.product_id = categories.cat_id"
    )
    return render_template(
        "index.html",
        fp=featuredProducts1,
        fp2=featuredProducts2,
        lp=latestProducts,
        ap=allProducts,
        pp=pickedProducts)

    featuredProducts1 = getProducts(
        "SELECT * FROM products INNER JOIN categories ON products.product_cat = categories.cat_id INNER JOIN brands ON products.product_cat = brands.brand_id ORDER BY RAND() limit 5"
    )
    #This gets the featured products and pass them to the index page
    featuredProducts2 = getProducts(
        "SELECT * FROM products INNER JOIN categories ON products.product_cat = categories.cat_id INNER JOIN brands ON products.product_cat = brands.brand_id ORDER BY RAND() limit 4"
    )
    #This gets the latest products and pass them to the index page
    latestProducts = getProducts(
        "SELECT * FROM products INNER JOIN categories ON products.product_cat = categories.cat_id INNER JOIN brands ON products.product_cat = brands.brand_id ORDER BY RAND() limit 4"
    )
    #This gets the picked products and pass them to the index page
    pickedProducts = getProducts(
        "SELECT * FROM products INNER JOIN categories ON products.product_cat = categories.cat_id INNER JOIN brands ON products.product_cat = brands.brand_id ORDER BY RAND() limit 4"
    )

    allProducts = getProducts(
        "SELECT * FROM products INNER JOIN categories ON products.product_cat = categories.cat_id INNER JOIN brands ON products.product_cat = brands.brand_id"
    )
    return render_template(
        "index.html",
        fp=featuredProducts1,
        fp2=featuredProducts2,
        lp=latestProducts,
        ap=allProducts,
        pp=pickedProducts)


@app.route('/ipn/', methods=['POST'])
def ipn():
    try:
        arg = ''
        request.parameter_storage_class = ImmutableOrderedMultiDict
        values = request.form
        for x, y in values.iteritems():
            arg += "&{x}={y}".format(x=x, y=y)

        validate_url = 'https://www.sandbox.paypal.com' \
                       '/cgi-bin/webscr?cmd=_notify-validate{arg}' \
                       .format(arg=arg)
        r = requests.get(validate_url)
        if r.text == 'VERIFIED':
            try:
                payer_email = thwart(request.form.get('payer_email'))
                unix = int(time.time())
                payment_date = thwart(request.form.get('payment_date'))
                username = thwart(request.form.get('custom'))
                last_name = thwart(request.form.get('last_name'))
                payment_gross = thwart(request.form.get('payment_gross'))
                payment_fee = thwart(request.form.get('payment_fee'))
                payment_net = float(payment_gross) - float(payment_fee)
                payment_status = thwart(request.form.get('payment_status'))
                txn_id = thwart(request.form.get('txn_id'))
            except Exception as e:
                with open('afrykmart/ipnout.txt', 'a') as f:
                    data = 'ERROR WITH IPN DATA\n' + str(values) + '\n'
                    f.write(data)

            with open('afrykmart/ipnout.txt', 'a') as f:
                data = 'SUCCESS\n' + str(values) + '\n'
                f.write(data)

            #c,conn = connection()
            c = mysql.connection.cursor()
            c.execute(
                "INSERT INTO ipn (unix, payment_date, username, last_name, payment_gross, payment_fee, payment_net, payment_status, txn_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (unix, payment_date, username, last_name, payment_gross,
                 payment_fee, payment_net, payment_status, txn_id))
            #conn.commit()
            mysql.connection.commit()
            c.close()
            #conn.close()
            gc.collect()

        else:
            with open('/afrykmart/ipnout.txt', 'a') as f:
                data = 'FAILURE\n' + str(values) + '\n'
                f.write(data)

        return r.text
    except Exception as e:
        return str(e)


#check if logged_in, not be able to go to a link by changing url in bar
def is_logged_in2(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in2' in session:
            return f(*args, **kwargs)
        else:
            flash('Please log in to proceed', 'danger')
            return redirect('admin_login')

    return wrap


#This is for rendering the products.html template
@app.route('/products')
def products():
    session['index'] = False
    allProducts = getProducts(
        "SELECT * FROM products INNER JOIN categories ON products.product_cat = categories.cat_id INNER JOIN brands ON products.product_brand= brands.brand_id ORDER BY RAND()"
    )
    return render_template("products.html", ap=allProducts)


#This is for rendering the admin_products.html template

@app.route('/product_mgt', methods=["POST","GET"])
def admin_products():
    session['index'] = False
    allProducts = displayProducts(
        "SELECT * FROM products INNER JOIN categories ON products.product_cat = categories.cat_id INNER JOIN brands ON products.product_brand= brands.brand_id"
    )
    categories = displayCategory("SELECT * FROM categories")
    brands = displayBrand("SELECT * FROM brands")
    if request.method == "POST":
        product_cat = request.form['category']
        product_brand = request.form['brand']
        product_title = request.form['title']
        product_price = request.form['price']
        product_desc = request.form['description']
        product_keywords = request.form['keywords']
        file = request.files['fileUpload']
        image = file.filename
        target = os.path.join(app_root, 'static/img/')
        destination = '/'.join([target, image])
        #f = os.path.join(app.config['UPLOAD_FOLDER'], image)
        file.save(destination)
        try:
            # prepare update query and data
            query = 'INSERT INTO products (product_cat, product_brand,product_title, product_price,product_desc,product_image,product_keywords) VALUES (%s,%s,%s,%s,%s,%s,%s)'
            #use cursor
            cur = mysql.connection.cursor()
            #execute query
            cur.execute(query,
                        (product_cat, product_brand, product_title,
                         product_price, product_desc, image, product_keywords))
            #commit DB

            mysql.connection.commit()
            cur.close()
            msg = "added successfully"
            print(msg)
            #close connect

            return redirect(url_for('admin_products'))
        except:
            msg = "error occured"
            print(msg)
    return render_template(
        "product_mgt.html", ap=allProducts, ca=categories, brand=brands)

#This is for rendering the login.html template
@app.route('/login', methods=["POST", "GET"])
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
                session['email'] = email
                session['role'] = role
                flash("Logged in as " + name + ".", 'success')
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
@app.route('/signup', methods=["POST", "GET"])
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
            cur = mysql.connection.cursor()
            #execute query
            cur.execute(query, (name, gender, dob, email, password))
            #commit DB
            mysql.connection.commit()
            #close connect
            cur.close()
            flash(name + ', your account is successfully created!', 'success')
            session['name'] = name
            session['logged_in'] = True
            return redirect(url_for('checkout'))
        except:
            print("Error in adding to database")

        cpassword = request.form['confirmPassword']

        if (cpassword == password):
            try:
                # prepare update query and data
                query = 'INSERT INTO users (full_name, gender, date_of_birth, email, password) VALUES(%s,%s,%s,%s,%s)'
                #use cursor
                cur = mysql.connection.cursor()
                #execute query
                cur.execute(query, (name, gender, dob, email, password))
                #commit DB
                mysql.connection.commit()
                #close connect
                cur.close()
                flash(name + ', your account is successfully created!',
                      'success')
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
            flash('Please log in to proceed', 'danger')
            return redirect('login')

    return wrap


#user logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are logged out', 'success')
    return redirect(url_for('index'))


#admin logout
@app.route('/admin_logout')
@is_logged_in
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))


#This is for rendering the shipping.html template
@app.route('/shipping')
@is_logged_in  #Verify that the user is logged before accessing this page
def shipping():
    session['index'] = False
    return render_template("shipping.html")


#This is for rendering the orders.html template
@app.route('/orders')
def orders():
    session['index'] = False
    return render_template("orders.html")


#This is for rendering the users_details.html template
@app.route('/users_details')
def users_details():
    session['index'] = False
    return render_template("users_details.html")


#This is for rendering the admin_login.html template
@app.route('/admin_login', methods=["POST", "GET"])
def admin_login():
    session['index'] = False
    if request.method == 'POST':
        #get for fields
        email = request.form['email']
        password_given = request.form['password']
        #create cursor
        cur = mysql.connection.cursor()

        #get user by username
        result = cur.execute('Select * from users where email = %s', [email])
        print(result)
        if result > 0:
            data = cur.fetchone()
            password = data['password']
            email = data['email']
            role = data['role']
            print(role)
            print(email)
            print(password)
            #compare passwords
            if password_given == password:
                #passed
                session['logged_in2'] = True
                # session['name'] = name
                session['role'] = role
                # flash("Logged in as " + name + ".", 'success')
                if role == "Admin":
                    return redirect(url_for('index_admin'))

                else:
                    error = "Admin Login Only"
                    flash(error)
                    return redirect(url_for('admin_login', error=error))

            else:
                error = "Wrong password."
                return render_template('admin_login.html', error=error)
            #close connection
            cur.close()
        else:
            error = "Email not found. Please check email input"
            return render_template('admin_login.html', error=error)

    return render_template("admin_login.html")


#This function for search the products available.

#This function for search the products available, function that sends request in includes/_footer.html


@app.route("/search")
def search():
    searchText = request.args['searchText']  # get the text to search for
    text = "%" + request.args['searchText'] + "%"
    # create an array with the query
    #create cursor
    cur = mysql.connection.cursor()

    #get user by username
    qresult = cur.execute(
        "SELECT * FROM products WHERE product_title LIKE  %s", [text])
    # Get the data returned by the query
    all_data = cur.fetchall()

    result = [
        c['product_title'] for c in all_data
        if searchText.lower() in c['product_title'].lower()
    ]
    #print(result)
    #get user by username
    qresult = cur.execute(
        "SELECT * FROM products WHERE product_title LIKE %s or product_desc LIKE %s or product_keywords LIKE %s",
        (text, text, text))
    # Get the data returned by the query
    all_data = cur.fetchall()
    result = [(c['product_title'], c['product_id']) for c in all_data]

    cur.close()
    # return as JSON
    return json.dumps({"results": result})


def selectQuery(query):
    cur = mysql.connection.cursor()
    result = cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return result, data


def insertQuery(query, parameter):
    cur = mysql.connection.cursor()
    cur.execute(query, parameter)
    #commit DB
    mysql.connection.commit()
    cur.close()


def deleteQuery(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    cur.close()


#This is for rendering the product-page.html template
@app.route('/viewproduct/<string:idd>')
def product(idd):
    session['index'] = False
    cur = mysql.connection.cursor()
    product = cur.execute(
        "SELECT * FROM products INNER JOIN categories ON products.product_cat = categories.cat_id INNER JOIN brands ON products.product_cat = brands.brand_id where product_id = %s",
        [idd])
    pr = []
    if product > 0:
        data = cur.fetchone()
        pr.append((data["product_title"], data["product_price"],
                   data["product_desc"], data["product_image"],
                   data["product_keywords"], data["cat_name"],
                   data["brand_name"], data["product_id"]))
    cur.close()
    pickedProducts = getProducts(
        "SELECT * FROM products INNER JOIN categories ON products.product_cat = categories.cat_id INNER JOIN brands ON products.product_cat = brands.brand_id ORDER BY RAND() limit 4"
    )
    return render_template("product-page.html", prs=pr, pp=pickedProducts)


#This function renders product page base sidelinks
@app.route('/viewproducts/<string:id>')
def viewproducts(id):
    session['index'] = False
    products = getProducts(
        "SELECT * FROM products INNER JOIN categories ON products.product_cat = categories.cat_id INNER JOIN brands ON products.product_cat = brands.brand_id where cat_id = "
        + id)
    pickedProducts = getProducts(
        "SELECT * FROM products INNER JOIN categories ON products.product_cat = categories.cat_id INNER JOIN brands ON products.product_cat = brands.brand_id ORDER BY RAND() limit 4"
    )
    return render_template("products.html", ap=products, pp=pickedProducts)


@app.route('/viewproductss/<string:i>')
def viewproductss(i):
    session['index'] = False
    productss = getProducts(
        "SELECT * FROM products INNER JOIN categories ON products.product_cat = categories.cat_id INNER JOIN brands ON products.product_cat = brands.brand_id where brand_id = "
        + i)
    pickedProducts = getProducts(
        "SELECT * FROM products INNER JOIN categories ON products.product_cat = categories.cat_id INNER JOIN brands ON products.product_cat = brands.brand_id ORDER BY RAND() limit 4"
    )
    return render_template("products.html", ap=productss, pp=pickedProducts)


#This function gets the ip address of the clients computer
def ipAddress():
    ip_add = ""
    if request.headers.getlist("X-Forwarded-For"):
        ip_add = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip_add = request.remote_addr
    return ip_add


#This function adds to cart from the single product page view
@app.route("/addSingle", methods=["POST", "GET"])
def addFromSingle():
    if request.method == "POST":
        p_id = request.form['p_id']
        qty = request.form['qty']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM cart where p_id = %s", [p_id])
        if result == 0:
            query = "INSERT INTO cart (p_id, ip_add, qty) VALUES (%s,%s,%s)"
            insertQuery(query, (int(p_id), ipAddress(), int(qty)))

        for data in cur.fetchall():
            oldQty = data['qty']
            newQty = int(qty) + oldQty
            cur.execute("UPDATE cart SET qty = %s WHERE p_id = %s",
                        (newQty, p_id))
            mysql.connection.commit()
        cur.close()
        flash('Product Added!', 'Success')
        return redirect(url_for('viewCart'))


#This function is to add tp cart.
@app.route("/addToCart")
def addToCart():
    product_id = request.args['product_id']  # get product id
    action = request.args['action']  # get action
    ip_add = ipAddress()
    if product_id != "-1":
        result = selectQuery("SELECT * FROM cart")
        foundProduct = False
        for data in result[1]:
            qty = data["qty"]
            if ((data["p_id"] == int(product_id))
                    and (data["ip_add"] == ip_add)):
                foundProduct = True
                #-50 is used to denote if a user wants to add to cart
                print(action == "-50")
                if action == "-50":
                    qty = qty + 1
                    query = "UPDATE cart SET qty = %s where p_id= %s"
                    insertQuery(query, (qty, data["p_id"]))
                elif action == "-100":
                    qty = qty - 1
                    query = "UPDATE cart SET qty = %s where p_id= %s"
                    insertQuery(query, (qty, data["p_id"]))
        if (foundProduct == False):
            query = "INSERT INTO cart (p_id, ip_add, qty) VALUES (%s,%s,%s)"
            insertQuery(query, (product_id, ip_add, 1))

        deleteQuery("DELETE FROM cart WHERE qty = 0")
    if action == "-500":
        deleteQuery("DELETE FROM cart WHERE p_id =" + product_id)

    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM cart INNER JOIN products ON cart.p_id = products.product_id AND cart.ip_add = %s",
        [ip_add])
    result2 = cur.fetchall()
    cur.close()
    # return as JSON
    return json.dumps({"results": result2})


#This function is to add order
def addOrder():
    session['index'] = False
    email=session['email']
    cur = mysql.connection.cursor()
    result = cur.execute('Select * from users where email = %s', [email])
    all_data = cur.fetchall()
    for res in all_data:
        user_id = res['user_id']  
        name=res['full_name'] 
    details=displayOrder()[0]
    amount=displayCart()[2]
    status="Order in Progress"
    now = datetime.datetime.now()
    date_ordered=now.strftime("%Y-%m-%d %H:%M")    
    cur.execute("INSERT INTO orders(user_id,cost, details, status, date_ordered) VALUES (%s,%s,%s,%s,%s)",[user_id,amount,details,status,date_ordered])
    mysql.connection.commit()
    cur.close()
    # deleteCart()






@app.route("/viewcart")
def viewCart():
    session['index'] = False
    return render_template("cart.html")


#This is for rendering the checkout.html template
@app.route('/checkout')
@is_logged_in  #Verify that the user is logged before accessing this page
def checkout():
    session['index'] = False
    session["amount"] = displayCart()[2]
    addOrder()
    deleteCart()
    return render_template("checkout.html")


@app.route('/success/', methods=['GET', 'POST'])
def success():
    return redirect(url_for("index"))


#Displays cart at the top right hand corner, currently suspend because alternative method and more effective method discovered.
def displayCart():
    cur = mysql.connection.cursor()
    stmt = cur.execute(
        "SELECT DISTINCT * FROM cart, products where products.product_id = p_id"
    )
    all_data = cur.fetchall()
    res = []
    q = 0
    p = 0
    for data in all_data:
        res.append((data["product_title"], data["product_image"],
                    data["product_price"], data["qty"]))
        q = q + data["qty"]
        p = p + data["product_price"] * data["qty"]
    cur.close()
    return res, q, p

#Displays order details 
def displayOrder():
    cur = mysql.connection.cursor()
    stmt = cur.execute(
        "SELECT DISTINCT * FROM cart, products where products.product_id = p_id"
    )
    all_data = cur.fetchall()
    q = 0
    p = 0
    for data in all_data:
        res=data["product_title"]+ " qty:  "+str(data["qty"])
        q = q + data["qty"]
        p = p + data["product_price"] * data["qty"]
    cur.close()
    return res, q, p


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
        product_price = str(data['product_price'])
        product_desc = data['product_desc']
        product_image = data['product_image']
        product_desc = data['product_keywords']
        #print(product_image)
        products.append(product_id + "#" + product_cat + "#" + product_title +
                        "#" + product_price + "#" + product_desc + "#" +
                        product_image + "#" + product_desc)
    return products


def displayProducts(query):
    products = []
    #create cursor
    cur = mysql.connection.cursor()
    result = cur.execute(query)
    all_data = cur.fetchall()
    for data in all_data:
        product_id = str(data['product_id'])
        product_cat = data['cat_name']
        product_brand = data['brand_name']
        product_title = data['product_title']
        product_price = str(data['product_price'])
        product_desc = data['product_desc']
        product_image = data['product_image']
        product_key = data['product_keywords']
        #print(product_image)
        products.append(product_id + "#" + product_cat + "#" + product_title +
                        "#" + product_price + "#" + product_desc + "#" +
                        product_image + "#" + product_key + "#" +
                        product_brand)
    return products


def loadCategories():
    cat_name=[]
    cat_id=[]
    sql ="SELECT * FROM categories"
    cur = mysql.connection.cursor()
    result = cur.execute(sql)
    all_data = cur.fetchall()
    for data in all_data:
        category_id = data['cat_id']
        category_cat = data['cat_name']
        cat_id.append(category_id)
        cat_name.append(category_cat)
    return cat_id,cat_name


def displayCategory(query):
    products = []
    #create cursor
    cur = mysql.connection.cursor()
    result = cur.execute(query)
    all_data = cur.fetchall()
    for data in all_data:
        category_id = str(data['cat_id'])
        category_cat = data['cat_name']

        products.append(category_id + "#" + category_cat)
    return products


# delete cart
def deleteCart():
    ip_add=ipAddress()
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cart WHERE ip_add=%s",[ip_add])
    cur.close()


def displayBrand(query):
    products = []
    #create cursor
    cur = mysql.connection.cursor()
    result = cur.execute(query)
    all_data = cur.fetchall()
    for data in all_data:
        brand_id = str(data['brand_id'])
        brand_name = data['brand_name']

        products.append(brand_id + "#" + brand_name)
    return products


#Delete product
@app.route("/delete/<string:id>", methods=["POST", "GET"])
def delete_prod(id):
    # Create cursor
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM products where product_id = %s",
        [id])
    try:
        target = os.path.join(app_root, 'static/img/')
        data = cur.fetchone() #get image name from database
        fileToRemove = '/'.join([target, data["product_image"]])
        os.remove(fileToRemove)

        # Execute
        cur.execute("DELETE FROM products WHERE product_id = %s", [id])
        # Commit to DB
        mysql.connection.commit()
        #Close connection
        cur.close()
        flash('Product Deleted', 'success')
        return redirect(url_for('admin_products'))
    except:
        # cur.rollback()
        msg = "Error occured"
        cur.close()
        print(msg)


#Admin Edit product
@app.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_product(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Execute
    result = cur.execute(
        "SELECT * FROM products INNER JOIN categories ON products.product_id = categories.cat_id INNER JOIN brands ON products.product_cat= brands.brand_id  WHERE product_id = %s",
        [id])
    if request.method == "POST":
        product_cat = request.form['category']
        product_brand = request.form['brand']
        product_title = request.form['title']
        product_price = request.form['price']
        product_desc = request.form['description']
        product_keywords = request.form['keywords']
        try:
            file = request.files['fileUpload']
            image = file.filename
            target = os.path.join(app_root, 'static/img/')
            destination = '/'.join([target, image])
            file.save(destination)
            data = cur.fetchone() #get image name from database
            fileToRemove = '/'.join([target, data["product_image"]])
            os.remove(fileToRemove)
            cur.execute(
            "UPDATE products SET product_cat=%s, product_brand=%s,product_title=%s, product_price=%s,product_desc=%s,product_image=%s,product_keywords=%s WHERE product_id=%s",
            (product_cat, product_brand, product_title, product_price,
             product_desc, image, product_keywords, id))
            
        except:
            cur.execute(
            "UPDATE products SET product_cat=%s, product_brand=%s,product_title=%s, product_price=%s,product_desc=%s,product_keywords=%s WHERE product_id=%s",
            (product_cat, product_brand, product_title, product_price,
             product_desc, product_keywords, id))
            print("Image not updated")
        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        # flash('Article Updated', 'success')

        return redirect(url_for('admin_products'))


#This is for rendering the template for admin
@app.route('/admin')
@is_logged_in2
def index_admin():
    return render_template('index_admin.html')

@app.route("/email", methods=["POST","GET"])
def email():
    if request.method == "POST":
        email = request.form['email']
        print (email)
        msg = Message("Welcome to Afryk Mart Newsletter!",
                  sender="rahmat.raji@ashesi.edu.gh",
                  recipients=[email])
        msg.body= "You have successfully been added to Afyrk Mart's Mailing List. We will keep you updated on the latest products, promotions and discounts"
        mail.send(msg)
    return redirect(url_for("index"))



if __name__ == '__main__':
    app.run(debug=True)

# all the type submit(add product, delete, update) are referring to product_mgt....casausing confusion which type submit to submit
