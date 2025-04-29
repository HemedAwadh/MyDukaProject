import psycopg2
from datetime import datetime

#create a connection to the db
conn = psycopg2.connect(user = "postgres",password = "admin",host ="localhost",port ="5432",database = "myduka")
now = datetime.now

#cursur- execute queries or db operations
cur = conn.cursor()

#query to fetch products
cur.execute('select from products;')
products = cur.fetchall()

for product in products :
    print(product)

#fuction to fetch products
def fetch_products():
    cur.execute('select from products;')
    products = cur.fetchall()       
    return products

#fuction to fetch products
def fetch_sales():
    cur.execute('select from sales;')
    sales= cur.fetchall()          
    return sales

#inserting data 
#fetch products

def insert_products():
    cur.execute("insert into products(name,buying_price,selling_price,stock_quantity)values('juice',100,150,70)")
    conn.commit()

def insert_sales():
    cur.execute("insert into sales(pid,quantity,created_at)values(21,1,'{now}')")
    conn.commit()

insert_products()
insert_sales()

fetch_products()
fetch_sales()

# A function to fetch data from  any table of your choice
def fetch_data(table):
    cur.execute(f"select * from {table};")
    data = cur.fetchall()
    return data

products = fetch_data('products')
sales = fetch_data('sales')
print("Fetching sales from fetch fun :\n",products)



#inserting data 
# method 1 -insert products function that takes value as a parameter and uses placeholders
#number of placeholders has to match no of columns

def insert_products(values):
    insert = "insert into products(name,buying_price,selling_price,stock_quantity)values(%s,%s,%s,%s) "
    cur.execute(insert,values)
    conn.commit()

product1 = ("bread",150,200,50)    
insert_products(product1)
products = fetch_data('products')
print("Fetching sales from fetch fun :\n",products)

#method 2- insert products function that takes values as parameter and uses formatted string

def insert_products_method_2(values):
    insert = f"insert into products(name,buying_price,selling_price,stock_quantity)values{values}"
    cur.execute(insert)
    conn.commit()


product2 = ("soap",20,30,80)    
insert_products(product2)
products = fetch_data('products')
print("Fetching sales from fetch fun :\n",products)

#method 3- insert data in any table 
#this function takes table,columns and values as parameters 

def insert_data(table,columns,data):
    cur.execute(f"insert into {table} ({columns}) values {values}")
    conn.commit()

table = 'products'   
columns = 'name,buying_price,selling_price,stock_quantity'
values = ("bag",300,450,5)
insert_data(table,columns,values)
products = fetch_data('products')
print("Fetching sales from fetch fun :\n",products)






 
  