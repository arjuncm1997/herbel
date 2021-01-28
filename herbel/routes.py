import os 
from flask import Flask, flash, session
from flask import render_template, flash, redirect, request, abort, url_for
from herbel import app, db, bcrypt, mail
from herbel.models import Login, Shippingdetails, Productadd, Contact, Gallery
from herbel.forms import Shipform , Shipdetailsform, Productaddform, Delivery, RegistrationForm, Imageadd, Changepassword, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
from random import randint
import random       
import string
from flask_mail import Message

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/gallery')
def gallery():
    gallery = Gallery.query.all()
    return render_template("gallery.html", gallery = gallery)

@app.route('/agalleryadd',methods=['POST','GET'])
@login_required
def agalleryadd():
    form=Imageadd()

    if form.validate_on_submit():

        if form.pic.data:
            pic_file = save_picture(form.pic.data)
            view = pic_file
        print(view)  
    
        gallery = Gallery(name=form.name.data,image=view )
       
        db.session.add(gallery)
        db.session.commit()
        print(gallery)
        flash('image added', 'success')
        return redirect('/agalleryview')
            
    return render_template('agalleryadd.html',form=form)

@app.route("/agalleryedit/<int:id>", methods=['GET', 'POST'])
@login_required
def agalleryedit(id):
    gallery = Gallery.query.get_or_404(id)
    form = Imageadd()
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            gallery.image = picture_file
        gallery.name = form.name.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/agalleryview')
    elif request.method == 'GET':
        form.name.data = gallery.name
    return render_template('agalleryedit.html',form=form, gallery = gallery)


@app.route('/agalleryview')
@login_required
def agalleryview():
    image = Gallery.query.all()
    return render_template("agalleryview.html", image = image)

@app.route('/agallerydelete/<int:id>')
@login_required
def agallerydelete(id):
    delete = Gallery.query.get_or_404(id)
    db.session.delete(delete)
    db.session.commit()
    return redirect('/agalleryview')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method=='POST':
        name= request.form['name']
        email= request.form['email']
        subject= request.form['subject']
        message= request.form['message']
        
        new = Contact(name= name, email = email, subject =subject, message=message, usertype = 'public')
        try:
            db.session.add(new)
            db.session.commit()
            return redirect('/')

        except:
            return 'not add'  
    else:
        return render_template("contact.html")

@app.route('/scontact', methods=['GET', 'POST'])
@login_required
def scontact():
    if request.method=='POST':
        subject= request.form['subject']
        message= request.form['message']
        
        new = Contact(name= current_user.username, email = current_user.email, subject =subject, message=message, usertype = 'ship')
        try:
            db.session.add(new)
            db.session.commit()
            return redirect('/sindex')

        except:
            return 'not add'  
    else:
        return render_template("scontact.html")

@app.route('/ucontact', methods=['GET', 'POST'])
@login_required
def ucontact():
    if request.method=='POST':
        subject= request.form['subject']
        message= request.form['message']
        
        new = Contact(name= current_user.username, email = current_user.email, subject =subject, message=message, usertype = 'user')
        try:
            db.session.add(new)
            db.session.commit()
            return redirect('/uindex')

        except:
            return 'not add'  
    else:
        return render_template("ucontact.html")

@app.route("/uindex")
@login_required
def uindex():
    return render_template("uindex.html")

@app.route('/sindex')
@login_required
def sindex():
    return render_template("sindex.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Login.query.filter_by(email=form.email.data, usertype = 'user' ).first()
        user1 = Login.query.filter_by(email=form.email.data,  usertype = 'ship').first()
        user2 = Login.query.filter_by(email=form.email.data,  usertype = 'admin').first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/uindex')
        if user1 and bcrypt.check_password_hash(user1.password, form.password.data):
            login_user(user1, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/sindex')
        if user2 and user2.password== form.password.data:
            login_user(user2, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/admin')

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form = form)

@app.route('/userregister',methods=['GET','POST'])
def userregister():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new = Login(username= form.username.data,email=form.email.data, address=form.add.data, phone=form.phone.data,password=hashed_password, usertype= 'user' )
        db.session.add(new)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect('/')
    return render_template('userregister.html', form=form)


@app.route('/shipregister',methods=['GET','POST'])
def shipregister():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new = Login(username= form.username.data,email=form.email.data, address=form.add.data, phone=form.phone.data,password=hashed_password, usertype= 'ship' )
        db.session.add(new)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect('/')
    return render_template('shipregister.html',form=form)


@app.route('/sdetails')
@login_required
def sdetails():
    return render_template("sdetails.html")


@app.route('/sprofile/<int:id>',methods=['GET','POST'])
@login_required
def sprofile(id):
    form = Shipform()
    task = Login.query.get_or_404(id)
    if form.validate_on_submit():
        if form.pic.data:
            view = save_picture(form.pic.data)
            task.image = view
        task.username = form.name.data
        task.email = form.email.data
        task.address = form.add.data
        task.phone = form.phone.data
        db.session.commit() 
        return redirect("")

    elif request.method == 'GET':
        form.name.data = task.username
        form.email.data = task.email
        form.add.data = task.address
        form.phone.data = task.phone
    return render_template("sprofile.html",form=form)


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def save_picture(form_picture):
    random_hex = random_with_N_digits(14)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(random_hex) + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route('/sdetailsadd',methods=['GET','POST'])
@login_required
def sdetailsadd():
    form = Shipdetailsform()
    if form.validate_on_submit():
        new = Shippingdetails(ownerid = current_user.id,ownername = current_user.username,fromplace = form.fromplace.data,toplace=form.to.data,date=form.date.data,time =form.time.data ,desc =form.desc.data  )
        db.session.add(new)
        db.session.commit()
        return redirect('/sdetailsview')
    return render_template('sdetailsadd.html', form = form)


@app.route('/sdetailsview')
@login_required
def sdetailsview():
    tasks = Shippingdetails.query.filter_by(ownerid=current_user.id).all()
    return render_template("sdetailsview.html", tasks = tasks)


@app.route('/sdetailsdelete/<int:id>')
@login_required
def sdetailsdelete(id):
    delete = Shippingdetails.query.get_or_404(id)
    try:
        db.session.delete(delete)
        db.session.commit()
        return redirect('/sdetailsview')
    except:
        return 'There was an issue deleting your task'


@app.route('/sdetailsedit/<int:id>',methods=['GET','POST'])
@login_required
def sdetailsedit(id):
    form = Shipdetailsform()
    ship = Shippingdetails.query.get_or_404(id)
    if form.validate_on_submit():
        ship.fromplace = form.fromplace.data
        ship.toplace = form.to.data
        ship.date = form.date.data
        ship.time = form.time.data
        ship.desc = form.desc.data
        db.session.commit() 
        return redirect('/sdetailsview')
    elif request.method == 'GET':
        form.fromplace.data = ship.fromplace
        form.to.data = ship.toplace
        form.date.data = ship.date
        form.time.data = ship.time
        form.desc.data = ship.desc
    return render_template('sdetailsedit.html', form = form)


@app.route('/udetails')
@login_required
def udetails():
    details = Shippingdetails.query.all()
    return render_template("udetails.html", details = details)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/uproductadd/<int:id>',methods=['GET','POST'])
@login_required
def uproductadd(id):
    form = Productaddform()
    det = Shippingdetails.query.get_or_404(id)
    if form.validate_on_submit():
        new = Productadd(ownerid =current_user.id ,pdtname =form.product.data ,weight = form.weight.data,delname =form.name.data,deladdress =form.address.data ,detailsid = det.id,shipid = det.ownerid,shipname = det.ownername,fromplace = det.fromplace,toplace=det.toplace,date=det.date,time =det.time ,desc =det.desc ,status = '',delstatus='',productid='' )
        db.session.add(new)
        db.session.commit()
        flash('Product add successfully','success')
        return redirect('/uindex')
    return render_template('uproductadd.html', form = form)


@app.route('/uproductdetails')
@login_required
def uproductdetails():
    details = Productadd.query.filter_by(ownerid=current_user.id).all()
    return render_template("uproductdetails.html",details = details)


@app.route('/uapprovedproducts')
@login_required
def uapprovedproducts():
    details = Productadd.query.filter_by(status='approved', ownerid=current_user.id).all()
    return render_template("uapprovedproducts.html",details = details)




@app.route('/sproducts',methods=['GET','POST'])
@login_required
def sproducts():
    form =Delivery()
    details = Productadd.query.filter_by(status='approved',shipid=current_user.id).all()
    return render_template("sproducts.html",details = details, form=form)

@app.route('/sproductsform/<int:id>',methods=['GET','POST'])
@login_required
def sproductsform(id):
    form =Delivery()
    details = Productadd.query.get_or_404(id)
    if form.validate_on_submit():
        details.delstatus = form.status.data
        db.session.commit() 
        return redirect('/sproducts')
    elif request.method == 'GET':
        form.status.data = details.delstatus
    return render_template("sproducts.html", form=form)


@app.route('/admin')
@login_required
def admin():
    return render_template("admin.html")

@app.route('/aproducts')
@login_required
def aproducts():
    details = Productadd.query.filter_by(status='').all()
    return render_template("aproducts.html", details=details)


@app.route('/aproductsview/<int:id>')
@login_required
def aproductsview(id):
    details = Productadd.query.get_or_404(id)
    return render_template("aproductsview.html", details=details)

@app.route('/aproductapprove/<int:id>')
@login_required
def aproductapprove(id):
    details = Productadd.query.get_or_404(id)
    no = details.ownerid
    log = Login.query.get_or_404(no)
    def randomString(stringLength=5):
        letters = string.digits
        return ''.join(random.choice(letters) for i in range(stringLength))
    number =randomString()
    details.status='approved'
    details.productid = number
    approvemail(log,number)
    db.session.commit()
    return redirect('/aproducts')

def approvemail(log,number):
    msg = Message('Successfull',
                  recipients=[log.email])
    msg.body = f''' Product approved number: {number} '''
    mail.send(msg) 


@app.route('/aproductreject/<int:id>')
@login_required
def aproductreject(id):
    details = Productadd.query.get_or_404(id)
    details.status='rejected'
    db.session.commit()
    flash('Product Rejected ', 'success')
    return redirect('/aproducts')

@app.route('/aproductsapprove')
@login_required
def aproductsapprove():
    details = Productadd.query.filter_by(status='approved').all()
    return render_template("aproductsapprove.html", details=details)

@app.route('/aproductstatus')
@login_required
def aproductstatus():
    details = Productadd.query.filter_by(status='approved').all()
    return render_template("aproductstatus.html", details=details)

@app.route('/aproductsreject')
@login_required
def aproductsreject():
    details = Productadd.query.filter_by(status='rejected').all()
    return render_template("aproductsreject.html", details=details)

@app.route('/aview/<int:id>')
@login_required
def aview(id):
    details = Productadd.query.get_or_404(id)
    return render_template("aview.html", details=details)


@app.route('/ucheckstatus',methods=['GET','POST'])
@login_required
def ucheckstatus():
    form =Delivery()
    if form.validate_on_submit():
        number = form.status.data
        return redirect('/ustatus/'+str(number))

    return render_template("ucheckstatus.html", form=form)

    
@app.route('/ustatus/<number>')
@login_required
def ustatus(number):
    details = Productadd.query.filter_by(productid = number).first()

    return render_template("ustatus.html",details=details)

@app.route('/apubliccontact')
@login_required
def apubliccontact():
    f = Contact.query.filter_by(usertype='public').all()
    return render_template("apubliccontact.html", f=f)

@app.route('/ausercontact')
@login_required
def ausercontact():
    f = Contact.query.filter_by(usertype='user').all()
    return render_template("ausercontact.html", f=f)

@app.route('/ashipcontact')
@login_required
def ashipcontact():
    f = Contact.query.filter_by(usertype='ship').all()
    return render_template("ashipcontact.html", f=f)

@app.route('/auser')
@login_required
def auser():
    user = Login.query.filter_by(usertype='user').all()
    return render_template("auser.html", user=user)


@app.route('/aship')
@login_required
def aship():
    ship = Login.query.filter_by(usertype='ship').all()
    return render_template("aship.html", ship=ship)

@app.route('/resetrequest', methods=['GET','POST'])
def resetrequest():
    if request.method == 'POST':
        email=request.form['email']
        user = Login.query.filter_by(email=email).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect('/login')
    return render_template('resetrequest.html')

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('resettoken', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/resetpassword/<token>", methods=['GET', 'POST'])
def resettoken(token):
    user = Login.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect('/resetrequest')
    form = Changepassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect('/login')
    return render_template('resetpassword.html', title='Reset Password', form=form)