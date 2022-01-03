from flask import Flask, render_template,url_for,request,redirect,Response,session,send_file
from flask_sqlalchemy import SQLAlchemy
import time,datetime




app = Flask(__name__, template_folder='./templates')

app.secret_key = '\xea\x1a\xb2\x8a\xefk\xd6V%\xf7\xb4\xe5\xa9\r=&'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:linux123@localhost/products'

db = SQLAlchemy(app)

class Products(db.Model):
    __tablename__ ="products"
    id = db.Column(db.Integer,primary_key = True)
    database_import = db.Column(db.String(25))
    read = db.Column(db.String(25))
    dist = db.Column(db.Integer)
    comp = db.Column(db.String(25))
    data_posted = db.Column(db.DateTime, nullable = False, default = datetime.datetime.now())
    def __init__(self,dist,read,comp):
        self.read = read
        self.dist = dist
        self.comp = comp
    def __repr__(self):
        return f"User('{self.database_import}','{self.read}','{self.comp}','{self.dist}','{self.data_posted}')"

# class(db.Model)

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

