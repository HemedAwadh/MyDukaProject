from flask import Flask, render_template,request,redirect,url_for
from database import fetch_products,fetch_sales,insert_products

#instantiating our application -initialize our app

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")



@app.route('/products')
def products():
    products= fetch_products()
    return render_template("products.html",data = products)

@app.route('/add_products',methods=["GET,POST"])
def add_products():
    product_name = request.form['p-name']
    buying_price = request.form['b-price']
    selling_price = request.form['s-price']
    stock_quantity = request.form['stock']
    new_product = (product_name,buying_price,selling_price,stock_quantity)
    insert_products(new_product)
    return redirect(url_for('products'))

@app.route('/sales')
def sales():
    sales = fetch_sales()
    return render_template('sales.html',data = sales)
 
app.run(debug=True)