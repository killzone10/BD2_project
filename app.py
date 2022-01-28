from turtle import back
from xmlrpc.client import Boolean
from flask import Flask, render_template,url_for,request,redirect,Response,session,send_file,flash
from flask_sqlalchemy import SQLAlchemy
import time,datetime
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref
from forms import RegistrationForm,LoginForm



app = Flask(__name__, template_folder='./templates')

# app.secret_key = '\xea\x1a\xb2\x8a\xefk\xd6V%\xf7\xb4\xe5\xa9\r=&'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:linux123@localhost/products' ## postgres ://nazwa uzytkownima : haslo @ localhost/nazwa bazy danych
app.config['SECRET_KEY']='f027a3f2e1b601db1ae08006930c074f'







db = SQLAlchemy(app)

product_is_favourite = db.Table('product_is_favourite', db.Model.metadata,
    db.Column('product.id', db.Integer,db.ForeignKey('product.id')),
    db.Column('user.id', db.Integer,db.ForeignKey('user.id'))
    )

product_has_cart = db.Table('product_has_cart', db.Model.metadata,
    db.Column('product.id', db.Integer,db.ForeignKey('product.id')),
    db.Column('cart.id', db.Integer,db.ForeignKey('cart.id'))
    )

product_has_order = db.Table('product_has_order', db.Model.metadata,
    db.Column('product.id', db.Integer,db.ForeignKey('product.id')),
    db.Column('order.id', db.Integer,db.ForeignKey('order.id'))
    )
class Product(db.Model):
    __tablename__ ="product" 
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(25))
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    description = db.Column(db.String(25))

    
    favourite = db.relationship("User",secondary = product_is_favourite)
    comments = db.relationship("Comment",backref = "Comment")
    has_cart = db.relationship("Cart",secondary = product_has_cart)
    brand_id = db.Column(db.Integer,db.ForeignKey('brand.id'),nullable = False)
    type_id = db.Column(db.Integer,db.ForeignKey('product_type.id'),nullable = False)
    has_order = db.relationship("Order", secondary = product_has_order)
    sectors = db.Column(db.Integer,db.ForeignKey('sector.id'),nullable = False)
    warehouses = db.Column(db.Integer,db.ForeignKey('warehouse.id'),nullable = False)

    
    def __repr__(self):
        return f"Product('{self.name}','{self.price}','{self.quantity}')"


class Order(db.Model):
    __tablename__="order"
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, nullable = False)
    status = db.Column(db.Integer, nullable = False)
        # first_name = db.Column(db.String(15), nullable = False)
        # second_name = db.Column(db.String(15), nullable = False)
        # address = db.Column(db.String(15), nullable = False)
        # email = db.Column(db.String(20), nullable = False)
        # postal_code = db.Column(db.String(20), nullable = False)
    total_price = db.Column(db.Float, nullable = False)
    adress_id = db.Column(db.Integer,db.ForeignKey("address.id"))
    address = relationship("Address")
    # phone = db.Column(db.Integer, nullable = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = False) 
    def __repr__(self):
        return f"Order('{self.name}','{self.price}','{self.quantity}')"
    

class Invoice(db.Model):
    __tablename__="invoice"
    id = db.Column(db.Integer, primary_key = True)
    # first_name = db.Column(db.String(15), nullable = False)
    # second_name = db.Column(db.String(15), nullable = False)
    # address = db.Column(db.String(15), nullable = False)
    data = db.Column(db.DateTime, nullable = False, default = datetime.datetime.now())
    seller = db.Column(db.String(15), nullable = False)
    identification_number = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False, unique = True)
    order = db.relationship("Order",backref=backref("Order", uselist=False))
    # order_id = db.Column(db.Integer,db.ForeignKey('order.id'),nullable = False, unique = True)

    address_id = db.Column(db.Integer,db.ForeignKey("address.id"))
    address = relationship("Address",backref = backref("Invoice",uselist = False))




class Brand(db.Model):
    __tablename__="brand"
    id = db.Column(db.Integer,primary_key = True)
    description = db.Column(db.String(25),nullable = False)
    product_id = db.relationship('Product',backref = "Produkt")

class Product_type(db.Model):   
    __tablename__="product_type"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(45), nullable = False) 
    product_id = db.relationship('Product',backref = "Produkt")
    parent = db.relationship('Tag', remote_side=[id])
    parent_id = db.Column(db.Integer, db.ForeignKey('product_type.id'), nullable = True)
    

class Cart(db.Model):
     __tablename__ ="cart" 
     id = db.Column(db.Integer,primary_key = True)
     user = relationship("User",back_populates="cart",uselist = False)
    #  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #  user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False) # tutaj id z clasy user
     



class Comment(db.Model):
    __tablename__ ="comment" 
    id = db.Column(db.Integer,primary_key=True)
    description=db.Column(db.Text,unique=True,nullable=False) 
    title = db.Column(db.String(100),nullable=False)  
    data_posted = db.Column(db.DateTime, nullable = False, default = datetime.datetime.now())
    star_amount = db.Column(db.Integer) 
    
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False) # tutaj id z clasy user
    product_id = db.Column(db.Integer,db.ForeignKey('product.id'), nullable = False)    
    
    def __repr__(self):
        return f"Comment('{self.title}','{self.data_posted}')"

user_role = db.Table('user_role', db.Model.metadata,
    db.Column('user.id', db.Integer,db.ForeignKey('user.id')),
    db.Column('role.id',db.Integer, db.ForeignKey('role.id'))
    )

class User(db.Model): #1
    __tablename__ ="user" 
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)# unique  - jeden username dla jednego uzytkownika, nullable  =  musi istniec #default 
    password = db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(20),unique=True,nullable=False)
    first_name = db.Column(db.String(30),nullable=False)
    second_name = db.Column(db.String(30),nullable=True)
    phone = db.Column(db.Integer)
    # postal_code = db.Column(db.Integer)

    # product_fav_id = db.Column(db.Integer,db.ForeignKey   ('product.id'), nullable = False) 
    comments = db.relationship('Comment',backref = 'author', lazy = True) # backref dodajemy kolumne do Comment lazy true sql alchemy load TRUE asap
    # roles = db.relationship('User_role',backref = 'User_role',lazy = True) DOKONCZ RELACJE wiele do wielu
    roles = db.relationship("Role",secondary = user_role)
    orders = db.relationship('Order',backref = 'Order', lazy = True) # backref dodajemy kolumne do Comment lazy true sql alchemy load TRUE asap


    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'),unique = True)
    # cart = db.relationship("Cart",backref=backref("User", uselist=False))
    cart = db.relationship("Cart",back_populates = "User")
    # cart = db.relationship("Cart",uselist = False,backref = "user")

    


    def __repr__(self): # wyspeciikujemy klase z relacja
        return f"User('{self.database_import}','{self.read}','{self.comp}','{self.dist}','{self.data_posted}')"

class Role(db.Model):
    __tablename__ ="role" 
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),nullable=False)# unique  - jeden username dla jednego uzytkownika, nullable  =  musi istniec #default 



class Warehouse(db.Model):
    __tablename__ ="warehouse" 
    id = db.Column(db.Integer, primary_key = True)
    max_capacity = db.Column(db.Integer, nullable=False)
    # address = db.Column(db.String(30), nullable=False)
    # postal_code = db.Column(db.String(6), nullable=False)#!!! miasto z postal code zrobic jako oddzielna encje w 3PN
    product_id = db.relationship('Product',backref = "Produkt")
    sectors = db.relationship('Sector', backref = 'warehouse')

    address_id = db.Column(db.Integer,db.ForeignKey('address.id'))
    address = relationship("Address",backref = backref("Warehouse",uselist = False))
    def __repr__(self):
        return f"Warehouse('{self.database_import}','{self.read}','{self.comp}','{self.dist}','{self.data_posted}')"

class Sector(db.Model):
    __tablename__ ="sector" 
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)

    warehouse_id = db.Column(db.Integer,db.ForeignKey('warehouse.id'), nullable = False)
    workers = db.relationship('Worker', backref = 'sector')
    product_id = db.relationship('Product',backref = "Produkt")
    def __repr__(self):
        return f"Sector('{self.database_import}','{self.read}','{self.comp}','{self.dist}','{self.data_posted}')"

class Worker(db.Model):
    __tablename__ ="worker" 
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    position = db.Column(db.String(15), nullable=False) #!!! position zrobic jako odzielna encje w 3PN
    
    parent_id = db.Column(db.Integer, db.ForeignKey('worker.id'), nullable = True)
    sector_id = db.Column(db.Integer,db.ForeignKey('sector.id'), nullable = False)
    parent = db.relationship('Tag', remote_side=[id])
    def __repr__(self):
        return f"Worker('{self.database_import}','{self.read}','{self.comp}','{self.dist}','{self.data_posted}')"


class Address(db.Model):
    __tablename__ = "address"
    id = db.Column(db.Integer, primary_key = True)
    # country = db.Column(db.String(70),nullable  = False)
    # city = db.Column(db.String(70),nullable = False)
    street = db.Column(db.String(70),nullable = True)
    house_nr = db.Column(db.Integer, nullable = False) 
    postal_code = db.Column(db.String(15), nullable = False)
    # postal_code = db.Column(db.String(15), nullable = False)
    city_id = db.Column(db.Integer,db.ForeignKey('city.id'),nullable = False)


    #city relationship
    


class City(db.Model):
    __tablename__= 'city'
    id = db.Column(db.Integer,primary_key=True)
    country = db.Column(db.String(70),nullable  = False)
    name = db.Column(db.String(70),nullable = False) 
    address_id = db.relationship('Address',backref = "Address")




# db.create_all()


# @app.route('/picture')
# def picture():
#     return send_file(path,mimetype = '/image')
@app.route("/", methods =  ["POST", "GET"])
def index():
    if request.method == "POST":
        return redirect (url_for("tasks"))
    else:
        return render_template('index.html')


@app.route("/about")
def about():
    return render_template('error.html', title = "Ekran")

@app.route("/products")
def products():
    return render_template('products.html',title = "Products")

@app.route("/register",methods = ['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('index'))
    return render_template('register.html',title = "Register",form = form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html',title = "Login",form = form)
# @app.route("/tasks", methods=['POST', 'GET'])
# def tasks():
#     global switch, camera,res,res1
#     if "printer" in session:
#         printer = session["printer"]

#         if request.method == 'POST':
#             if request.form.get('click') == 'Capture':
#                 global capture
#                 capture = 1
#                 sleep(0.05) ## uspanie, by zdazyl zrobic zdjecie
#                 strg = strng.strg(session["printer"])
#                 b = strg.ret()
#                 # conn = connecting.connecting(b)
#                 # a = conn.reading()
#                 a = ['123131231','09 2022','1asda']

#                 if a[0] == "Error":
#                     return render_template('Error.html')
#                 # obj = searchingNewest.searchingNewest()
#                 # path = obj.searching()
#                 # logger.info(path)
#                 # OCR = processing.imageProcessing_gray(path,a)
#                 # a,zeros,out,distance = OCR.run()
#                 out = ["1","2","3"]
#                 distance = ['1','2','3']
#                 path = 'abcd'
#                 l1=[]
#                 list=[]
#                 for iteration,x in enumerate(out):
#                     r = new_list(a, out, distance, iteration)
#                     l1.append(r)
#                     ind = index(a, out,iteration)
#                     list.append(ind)
#                 # print(list)
#                 # logging.info(list)
#                 logger.info(l1)
#                 for iteration, x in enumerate(l1):
#                     record = Record(database_import = x[0],read = x[1],dist = x[2], comp = x[3])
#                     db.session.add(record)
#                 db.session.commit()
#                 return render_template('Final.html',path = path,list = l1,index = list)


#             elif request.form.get('stop') == 'Stop/Start':

#                 if (switch == 1):
#                     switch = 0
#                     camera.release()
#                     cv2.destroyAllWindows()

#                 else:
#                     camera = cv2.VideoCapture(0) # polaczenie po htppsie wysylanie obrazu
#                     switch = 1

#             elif request.form.get('res') == 'res':
#                 global res
#                 res = res - 1

#             elif request.form.get('res1') == 'res1':
#                 res = res + 1
#             elif request.form.get('red') == 'red':
#                 global red
#                 red = not red
#             elif request.form.get('black') == 'black':
#                 global black
#                 black = not black

#             # elif request.form.get('back') == 'Wróć':
#             #     return render_template('home.html',printers = printers)


#         elif request.method == 'GET':
#             return render_template('zamiennik.html', title="OCR", printer=printer)
#         return render_template('zamiennik.html', title="OCR", printer=printer)


if __name__ =='__main__':
    app.run(debug=True)

