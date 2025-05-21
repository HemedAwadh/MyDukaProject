from flask import Flask, render_template,request,redirect,url_for,flash,session
from database import fetch_products,fetch_sales,insert_products,insert_sales,profit_per_product,sales_per_product,sales_per_day,profit_per_day,check_user,add_user,insert_stock,fetch_stock,available_stock,product_name,edit_product
from flask_bcrypt import Bcrypt
from functools import wraps

#instantiating our application -initialize our app

app = Flask(__name__)
app.secret_key = 'hertgdikdghd'

bcrypt =Bcrypt(app)

@app.route('/')
def home():
    return render_template("index.html")

def login_required(f):
    @wraps(f)
    def protected(*args,**kwargs):
        if 'email' not in session:
            return redirect(url_for('login'))
        return f(*args,**kwargs)
    return protected


@app.route('/products')
@login_required
def products():
    products= fetch_products()
    stock = fetch_stock()
    return render_template("products.html",data = products)


@app.route('/stock')
@login_required
def stock():
    products= fetch_products()
    stock = fetch_stock()
    return render_template("stock.html",data = products,stock = stock)


@app.route('/add_stock', methods=["GET", "POST"])
def add_stock():
    if request.method =='POST':
        product_id = request.form['pid']
        quantity = request.form['quantity']
        new_stock =(product_id,quantity)
        insert_stock(new_stock)
        flash("Stock added successfully", "success")
        return redirect(url_for('stock'))


@app.route('/add_products', methods=["GET", "POST"])
def add_products():
    product_name = request.form['p-name']
    buying_price = request.form['b-price']
    selling_price = request.form['s-price']
    new_product = (product_name,buying_price,selling_price)
    insert_products(new_product)
    return redirect(url_for('products'))

@app.route('/update_product', methods = ['GET','POST'])
def update_product():
    if request.method == 'POST':
        pid = request.form['pid']
        name = request.form['name']
        buying_price = request.form['buying_price']
        selling_price = request.form['selling_price']
        edited_product =(pid,name,buying_price,selling_price)
        edit_product(edited_product)
        flash("Product edited successfully","success")
        return redirect(url_for('products'))
    


@app.route('/sales')
@login_required
def sales():
    sales_data = fetch_sales()
    products= fetch_products()
    return render_template('sales.html',data = sales_data, data1 =products)

@app.route('/make_sale', methods =["POST"])
def make_sale():
    product_id = request.form['pid']
    quantity = request.form['quantity']
    new_sale = (product_id,quantity)
    stock_available = available_stock(product_id)
    
    
    if stock_available < float(quantity):
        flash("Insufficient stock", "info")
        return redirect(url_for('sales'))

    insert_sales(new_sale)
    flash("Sale made "," success")
    return redirect(url_for('sales'))

@app.route('/dashboard')
@login_required
def dashboard():
    profit_product = profit_per_product()
    sales_product = sales_per_product()
    sales_day = sales_per_day()
    profit_day = profit_per_day()

    product_name = [str(i[0]) for i in profit_product]
    p_product= [float(i[1]) for i in profit_product]
    s_product =  [float(i[1]) for i in sales_product]
    date = [str (i[0]) for i in sales_day]
    profit = [float(i[1]) for i in profit_day]
    sales = [float(i[1]) for i in sales_day]

    return render_template('dashboard.html',
                           product_name = product_name ,
                             p_product = p_product, 
                             s_product= s_product,
                             s_day = sales_day,
                             p_day = profit_day,
                             date = date,
                             profit =profit,
                             sales = sales )


@app.route('/register',methods = ['GET','POST'])
def register():
    if request.method =='POST':
        name =request.form['name']
        email = request.form['email']
        phone_number = request.form['phone']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        flash(f"{name} Successfully registered", 'success')
        user = check_user(email)
        if not user:
            new_user =(name,email,phone_number,hashed_password)
            add_user(new_user)
            return redirect(url_for('login'))
        else:
            flash(f"Oops!!! {name} already registered", 'danger')
        
    return render_template("register.html")


@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = check_user(email)
        if not user:
            flash("User not found ,please register", "danger")
            return redirect(url_for('register'))
        else:
            if bcrypt.check_password_hash(user[-1],password):
                flash("Logged in successfully", 'success')
                session['email'] = email
                return redirect(url_for('home'))
            else:
                flash("incorrect password ", "danger")

    return render_template('login.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Process the form (e.g., send an email or save to a database)
    
        flash(f"Thank you {name}, your message has been sent!", 'success')

        return redirect(url_for('contact'))

    return render_template('contact.html')   


@app.route('/logout')
@login_required
def logout():
    session.pop('email',None)
    flash("Logged out Successfully!!", "info")

    return redirect(url_for('login'))


 
app.run(debug=True)