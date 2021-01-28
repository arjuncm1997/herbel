from herbel import db,app,login_manager
from flask_login import UserMixin
from flask_table import Table, Col, LinkCol
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(id):
    return Login.query.get(int(id))

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.VARCHAR)
    email= db.Column(db.VARCHAR)
    phone= db.Column(db.Integer)
    subject = db.Column(db.VARCHAR)
    message= db.Column(db.VARCHAR)
    usertype= db.Column(db.VARCHAR)

class Login(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80),default='NULL')
    address = db.Column(db.String(80),default='NULL')
    status=db.Column(db.String(80),default='NULL')
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    usertype = db.Column(db.String(80), nullable=False)

class Materials(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    owner = db.Column(db.String)
    name = db.Column(db.String(200))
    brand = db.Column(db.String(200))
    price = db.Column(db.String(200))
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    status = db.Column(db.String(200))
    desc = db.Column(db.String(200))

class Cart(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    sowner = db.Column(db.String)
    uowner = db.Column(db.String)
    name = db.Column(db.String(200))
    brand = db.Column(db.String(200))
    price = db.Column(db.String(200))
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    desc = db.Column(db.String(200))

class Buy(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    sowner = db.Column(db.String)
    uowner = db.Column(db.String)
    name = db.Column(db.String(200))
    brand = db.Column(db.String(200))
    price = db.Column(db.String(200))
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    desc = db.Column(db.String(200))
    qnty = db.Column(db.String(200))
    status = db.Column(db.String(200))
    deliname = db.Column(db.String(200))
    deliaddress = db.Column(db.String(200))
    delimobile = db.Column(db.String(200))
    payment = db.Column(db.String(200))
    delivery = db.Column(db.String(200))

class Credit(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    buyid = db.Column(db.String)
    name = db.Column(db.String(200))
    card = db.Column(db.String(200))
    cvv = db.Column(db.String(200))
    expdate = db.Column(db.String(200))


class Pay(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    buyid = db.Column(db.String)
    name = db.Column(db.String(200))
    card = db.Column(db.String(200))
    cvv = db.Column(db.String(200))
    validdate = db.Column(db.String(200))

class Gallery(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.VARCHAR)
    img = db.Column(db.String(20), nullable=False, default='default.jpg')