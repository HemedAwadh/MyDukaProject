import psycopg2
from datetime import datetime

#create a connection to the db
conn = psycopg2.connect(user = "postgres",password = "admin",host ="localhost",port ="5432",database = "myduka")
now = datetime.now

#cursur- execute queries or db operations
cur = conn.cursor()

#query to fetch products
# cur.execute('select * from products;')
# products = cur.fetchall()

# for product in products :
#     print(product)

#fuction to fetch products
def fetch_products():
    cur.execute('select * from products;')
    products = cur.fetchall()       
    return products

#fuction to fetch products
def fetch_sales():
    cur.execute('select * from sales;')
    sales= cur.fetchall()          
    return sales

#inserting data 
#fetch products

# def insert_products():
#     cur.execute("insert into products(name,buying_price,selling_price,stock_quantity)values('juice',100,150,70)")
#     conn.commit()

def insert_sales(values):
    insert=("insert into sales(pid,quantity,created_at)values(%s,%s,now())")
    cur.execute(insert,values)
    conn.commit()


def insert_stock(values):
    insert=("insert into stock(pid,stock_quantity,created_at)values(%s,%s,now())")
    cur.execute(insert,values)
    conn.commit()


def fetch_stock():
    cur.execute("select * from stock;")
    stock = cur.fetchall()
    return stock 

def available_stock(pid):
    cur.execute("select coalesce(sum(stock_quantity), 0) from stock where pid = %s" , (pid,)) 
    total_stock = cur.fetchone()[0]
    cur.execute("select coalesce(sum(sales.quantity),0) from sales where pid = %s" , (pid,)) 
    total_sold = cur.fetchone()[0] or 0
    return total_stock - total_sold

def product_name(pid):
    cur.execute("SELECT name from products WHERE id = %s",(pid))
    product = cur.fetchone()[0] or "unknown prod"
    return product

def edit_product(values):
    cur.execute("update products set name = %s,buying_price = %s,selling_price = %s where id = %s",values)
    conn.commit()



# insert_products()
# insert_sales()

# fetch_products()
# fetch_sales()

# A function to fetch data from  any table of your choice

# def fetch_data(table):
#     cur.execute(f"select * from {table};")
#     data = cur.fetchall()
#     return data

# products = fetch_data('products')
# sales = fetch_data('sales')
# print("Fetching sales from fetch fun :\n",products)



#inserting data 
# method 1 -insert products function that takes value as a parameter and uses placeholders
#number of placeholders has to match no of columns

def insert_products(values):
    insert = "insert into products(name,buying_price,selling_price)values(%s,%s,%s) "
    cur.execute(insert,values)
    conn.commit()

# product1 = ("bread",150,200,50)    
# insert_products(product1)
# products = fetch_data('products')
# print("Fetching sales from fetch fun :\n",products)

#method 2- insert products function that takes values as parameter and uses formatted string

def insert_products_method_2(values):
    insert = f"insert into products(name,buying_price,selling_price,stock_quantity)values{values}"
    cur.execute(insert)
    conn.commit()


# product2 = ("soap",20,30,80)    
# insert_products(product2)
# products = fetch_data('products')
# print("Fetching sales from fetch fun :\n",products)

#method 3- insert data in any table 
#this function takes table,columns and values as parameters 

# def insert_data(table,columns,data):
#     cur.execute(f"insert into {table} ({columns}) values {values}")
#     conn.commit()

# table = 'products'   
# columns = 'name,buying_price,selling_price,stock_quantity'
# values = ("bag",300,450,5)
# insert_data(table,columns,values)
# products = fetch_data('products')
# print("Fetching sales from fetch fun :\n",products)

# 1.profit per product
def profit_per_product():
  cur.execute("""select products.name,sum((products.selling_price - products.buying_price)*sales.quantity)
           as profit from products join sales on products.id = sales.pid group by(products.name);""")
  profit_per_product = cur.fetchall()
  return profit_per_product

# 2.profit per day
def profit_per_day():
   cur.execute("""select date(sales.created_at),sum((products.selling_price - products.buying_price)*sales.quantity)
            as profit from products join sales on products.id = sales.pid group by(sales.created_at);""")
   profit_per_day = cur.fetchall()
   return profit_per_day

# 3.sales per product
def sales_per_product():
    cur.execute("""select products.name,sum(products.selling_price * sales.quantity)
             as revenue from products join sales on products.id = sales.pid group by(products.name);""")
    sales_per_product = cur.fetchall()
    return sales_per_product

# 4.sales per day
def sales_per_day():
    cur.execute("""select date(sales.created_at),sum(products.selling_price * sales.quantity)
           as revenue from sales join products on products.id = sales.pid group by(sales.created_at);""")
    sales_per_day = cur.fetchall()
    return sales_per_day

def check_user(email):
    query = "SELECT * FROM users WHERE email = %s"
    cur.execute(query,(email,))
    user = cur.fetchone()
    return user

def add_user(user_details):
    query = "insert into users(full_name , email, phone_number,password)values(%s,%s,%s,%s)"
    cur.execute(query,user_details)
    conn.commit()
    





 
  