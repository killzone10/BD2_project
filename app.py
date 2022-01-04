from flask import Flask, render_template,url_for,request,redirect,Response,session,send_file
from flask_sqlalchemy import SQLAlchemy
import time,datetime

from sqlalchemy.orm import backref




app = Flask(__name__, template_folder='./templates')

app.secret_key = '\xea\x1a\xb2\x8a\xefk\xd6V%\xf7\xb4\xe5\xa9\r=&'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:linux123@localhost/products'

db = SQLAlchemy(app)

product_is_favourite = db.Table('product_is_favourite', db.Model.metadata,
    db.Column('product.id', db.Integer,db.ForeignKey('product.id')),
    db.Column('user.id', db.Integer,db.ForeignKey('user.id'))
    )

class Product(db.Model):
    __tablename__ ="product" # niepotrzebne
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(25))
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    description = db.Column(db.String(25))
    favourite = db.relationship("User",secondary =product_is_favourite)
    comments = db.relationship("Comment",backref = "Product")
    def __repr__(self):
        return f"Product('{self.name}','{self.price}','{self.quantity}')"



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
    email = db.Column(db.String(120),unique=True,nullable=False)
    first_name = db.Column(db.String(30),nullable=False)
    second_name = db.Column(db.String(30),nullable=True)
    phone = db.Column(db.Integer)
    postal_code = db.Column(db.Integer)

    comments = db.relationship('Comment',backref = 'author', lazy = True) # backref dodajemy kolumne do Comment lazy true sql alchemy load TRUE asap
    # roles = db.relationship('User_role',backref = 'User_role',lazy = True) DOKONCZ RELACJE wiele do wielu
    roles = db.relationship("Role",secondary = user_role)
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
    address = db.Column(db.String(30), nullable=False)
    postal_code = db.Column(db.String(6), nullable=False)#!!! miasto z postal code zrobic jako oddzielna encje w 3PN
    
    sectors = db.relationship('Sector', backref = 'warehouse')
    def __repr__(self):
        return f"Warehouses('{self.database_import}','{self.read}','{self.comp}','{self.dist}','{self.data_posted}')"

class Sector(db.Model):
    __tablename__ ="sector" 
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)

    warehouse_id = db.Column(db.Integer,db.ForeignKey('warehouse.id'), nullable = False)
    workers = db.relationship('Worker', backref = 'sector')
    def __repr__(self):
        return f"Sectors('{self.database_import}','{self.read}','{self.comp}','{self.dist}','{self.data_posted}')"

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
        return f"Workers('{self.database_import}','{self.read}','{self.comp}','{self.dist}','{self.data_posted}')"



# class User_role(db.Model):
#     user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False) # tutaj id z clasy user
#     role_id = db.Column(db.Integer,db.ForeignKey('role.id'),nullable = False)
    
# class Role(db.Model):
#     id = db.Column(db.Integer,primary_key=True,nullable = False)
#     name = db.Column(db.String(50),unique = False, nullable = True)
#     user_role = db.relationship('User_role',backref = "")
 

# class User(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     username=db.Column(db.String(20),unique=True,nullable=False)# unique  - jeden username dla jednego uzytkownika, nullable  =  musi istniec #default 
#     email=db.Column(db.String(120),unique=True,nullable=False) 
#     password=db.Column(db.String(30),nullable=False)

#     def __repr__(self):
#         return f"Products('{self.database_import}','{self.read}','{self.comp}','{self.dist}','{self.data_posted}')"


# class User(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     username=db.Column(db.String(20),unique=True,nullable=False)# unique  - jeden username dla jednego uzytkownika, nullable  =  musi istniec #default 
#     email=db.Column(db.String(120),unique=True,nullable=False) 
#     password=db.Column(db.String(30),nullable=False)

#     def __repr__(self):
#         return f"e('{self.database_import}','{self.read}','{self.comp}','{self.dist}','{self.data_posted}')"




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


# @app.route("/about")
# def about():
#     return render_template('index.html',printers = printers, title = "Ekran")
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

