from flask import Flask, render_template, request, redirect,  flash, abort, url_for
from herbel import app,db,bcrypt,mail
from herbel.models import *
from herbel.forms import *
from flask_login import login_user, current_user, logout_user, login_required
from random import randint
import os
from PIL import Image
from flask_mail import Message


@app.route('/')
def index():
    pro = Materials.query.all()
    return render_template("index.html",pro=pro)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/playout')
def playout():
    return render_template("playout.html")

@app.route('/contact',methods=['GET', 'POST'])
def contact():
    if request.method=='POST':
        name= request.form['name']
        email= request.form['email']
        phone= request.form['phone']
        subject= request.form['subject']
        message= request.form['message']
        print(message)
        hashed_password = bcrypt.generate_password_hash(name).decode('utf-8')
        print(hashed_password)
        new1 = Feedback(name=name,email=email,phone=phone,subject=subject,message=message,usertype='public')
        try:
            db.session.add(new1)
            db.session.commit()
            return redirect('/')

        except:
            return 'not add'  
    return render_template("contact.html")

@app.route('/gallery')
def gallery():
    gallery = Gallery.query.all()
    return render_template("gallery.html",gallery=gallery)

@app.route('/registeruser',methods=['GET','POST'])
def registeruser():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new = Login(username= form.username.data, email=form.email.data, password=hashed_password,phone = form.phone.data,usertype= 'user' )
        db.session.add(new)
        db.session.commit()
        flash('Your account has been created! waiting for approval', 'success')
        return redirect('/')
    return render_template("registeruser.html",form=form)

@app.route('/registerseller',methods=["GET","POST"])
def registerseller():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new = Login(username= form.username.data, email=form.email.data, password=hashed_password,phone = form.phone.data,usertype= 'seller' )
        db.session.add(new)
        db.session.commit()
        flash('Your account has been created! waiting for approval', 'success')
        return redirect('/')
    return render_template("registerseller.html",form=form)

@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Login.query.filter_by(email=form.email.data, usertype= 'seller',status = 'approve' ).first()
        user1 = Login.query.filter_by(email=form.email.data, usertype= 'user').first()
        user2 = Login.query.filter_by(email=form.email.data, usertype= 'admin').first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/sindex')
        if user1 and bcrypt.check_password_hash(user1.password, form.password.data):
            login_user(user1, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/uindex')
        if user2 and user2.password== form.password.data:
            login_user(user2, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/admin')
        if user2 and bcrypt.check_password_hash(user2.password, form.password.data):
            login_user(user2, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/admin')

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("login.html",form=form)

@app.route('/uindex')
def uindex():
    return render_template("uindex.html")
@app.route('/ulayout')
def ulayout():
    return render_template("ulayout.html")

@app.route('/sindex')
def sindex():
    return render_template("sindex.html")

@app.route('/slayout')
def slayout():
    return render_template("slayout.html")

@app.route('/aindex')
def aindex():
    return render_template("aindex.html")

@app.route('/s_addmaterials',methods=['GET', 'POST'])
@login_required
def s_addmaterials():
    form=Material()
    if form.validate_on_submit():
        if form.pic.data:
            pic_file = save_picture(form.pic.data)
            view = pic_file
        print(view)  
        material = Materials(owner= current_user.id,name=form.name.data,brand=form.brand.data,desc = form.desc.data,price = form.price.data,image=view)
       
        db.session.add(material)
        db.session.commit()
        flash('Product added')
        return redirect('/sindex')
            
    
    return render_template("s_addmaterials.html",form=form)


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

@app.route('/smaterialsview')
@login_required
def smaterialsview():
    material = Materials.query.filter_by(owner=current_user.id)
    return render_template("smaterialsview.html",mat=material)

@app.route('/smaterialsedit/<int:id>', methods=['GET', 'POST'])
@login_required
def smaterialsedit(id):
    material = Materials.query.get_or_404(id)
    
    form = Material()
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            material.image = picture_file
        material.name = form.name.data
        material.brand = form.brand.data
        material.desc = form.desc.data
        material.price = form.price.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/smaterialsview')
    elif request.method == 'GET':
        form.name.data = material.name
        form.brand.data = material.brand
        form.desc.data = material.desc
        form.price.data = material.price

    image_file = url_for('static', filename='pics/' + material.image)
    return render_template('smaterialsedit.html',form=form, material=material)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    delet = Materials.query.get_or_404(id)

    try:
        db.session.delete(delet)
        db.session.commit()
        return redirect('/smaterialsview')
    except:
        return 'There was a problem deleting that task'

@app.route('/asellerview')
def asellerview():
    user = Login.query.filter_by(usertype='seller',status='NULL').all()
    return render_template("asellerview.html",user=user)

@app.route('/auserview')
def auserview():
    user = Login.query.filter_by(usertype='user').all()
    return render_template("auserview.html",user=user)

@app.route('/approve/<int:id>')
def approve(id):
    user = Login.query.get_or_404(id)
    user.status = 'approve'
    db.session.commit()
    return redirect('/asellerview')

@app.route('/reject/<int:id>')
def reject(id):
    user = Login.query.get_or_404(id)
    user.status = 'reject'
    db.session.commit()
    return redirect('/asellerview')

@app.route('/asellerapprove')
def asellerapprove():
    user = Login.query.filter_by(usertype='seller',status='approve')
    return render_template("asellerapprove.html",user=user)

@app.route('/asellerreject')
def asellerreject():
    user = Login.query.filter_by(usertype='seller',status='reject')
    return render_template("asellerreject.html",user=user)

@app.route('/uproducts')
def uproducts():
    pro = Materials.query.all()
    return render_template("uproducts.html",pro=pro)

@app.route('/ucartadd/<int:id>',methods = ['GET','POST'])
def ucartadd(id):
    product = Materials.query.get_or_404(id)
    cart = Cart(sowner=product.owner,uowner=current_user.id,name=product.name,brand=product.brand,price=product.price,desc=product.desc,image=product.image)
    db.session.add(cart)
    db.session.commit()
    return redirect('/uproducts')

@app.route('/ucart')
def ucart():
    pro = Cart.query.filter_by(uowner=current_user.id).all()
    return render_template("ucart.html",mat=pro)

@app.route('/cartremove/<int:id>')
def cartremove(id):
    delet = Cart.query.get_or_404(id)

    try:
        db.session.delete(delet)
        db.session.commit()
        return redirect('/ucart')
    except:
        return 'There was a problem deleting that task'

@app.route('/uproductprofile/<int:id>')
def uproductprofile(id):
    cart=Cart.query.get_or_404(id)
    return render_template("uproductprofile.html",cart=cart)

@app.route('/udelivery/<int:id>',methods=['GET','POST'])
def udelivery(id):
    form = Address()
    cart = Cart.query.get_or_404(id)
    if form.validate_on_submit():
        priceof1 = int(form.qnty.data)*int(cart.price)
        buy=  Buy(sowner = cart.sowner,uowner=cart.uowner,name=cart.name,brand=cart.brand,image=cart.image,desc=cart.desc,qnty=form.qnty.data , price = priceof1 ,deliname=form.name.data, deliaddress=form.address.data, delimobile = form.phone.data)
        try:
            db.session.add(buy)
            db.session.commit()
            return redirect('/upayment/'+str(buy.id))
        except:
            return 'notadd'

    return render_template("udelivery.html",form=form)

@app.route('/upayment/<int:id>')
@login_required
def upayment(id):
    form = Cod()
    form1 = Creditcard()
    form2 = Paypal()
    material = Buy.query.get_or_404(id)
    return render_template('upayment.html',material = material,form=form,form1 =form1,form2=form2)


@app.route('/cod/<int:id>',methods = ['GET','POST'])
@login_required
def cod(id):
    form = Cod()
    form1 = Creditcard()
    form2 = Paypal()
    material = Buy.query.get_or_404(id)
    if form.validate_on_submit():
        material.status = 'purchased'
        material.payment = 'Cash on delivery'
        db.session.commit()
        sendmail()
        return redirect('/successful')
    return render_template('/upayment.html',mat = material,form=form, form1 =form1,form2=form2)

def sendmail():
    msg = Message('successful',
                  recipients=[current_user.email])
    msg.body = f''' your Order Succsessfully Completed...   Track Your Order   'http://127.0.0.1:5000/login' '''
    mail.send(msg)

@app.route('/creditcard/<int:id>',methods = ['GET','POST'])
@login_required
def creditcard(id):
    form = Cod()
    form1 = Creditcard()
    form2 = Paypal()
    material = Buy.query.get_or_404(id)
    if form1.validate_on_submit():
        material.status = 'purchased'
        material.payment = 'Creditcard'
        db.session.commit()
    if form1.validate_on_submit():
        credit = Credit(buyid = material.id,name = form1.name.data,card= form1.number.data ,cvv=form1.cvv.data , expdate=form1.date.data)
        db.session.add(credit)
        db.session.commit()
        sendmail()
        return redirect('/successful1')
    return render_template('/upayment.html',form=form ,form1 =form1,form2=form2)

@app.route('/paypal/<int:id>',methods = ['GET','POST'])
@login_required
def paypal(id):
    form = Cod()
    form1 = Creditcard()
    form2 = Paypal()
    material = Buy.query.get_or_404(id)
    if form2.validate_on_submit():
        material.status = 'purchased'
        material.payment = 'Paypal'
        db.session.commit()
    if form2.validate_on_submit():
        pay = Pay(buyid = material.id,name = form2.name.data,card= form2.number.data ,cvv=form2.cvv.data , validdate=form2.date.data)
        db.session.add(pay)
        db.session.commit()
        sendmail()
        return redirect('/successful1')
    return render_template('/upayment.html',form=form ,form1 =form1,form2=form2)


@app.route('/successful')
@login_required
def successful():
    return render_template("successful.html")

@app.route('/successful1')
@login_required
def successful1():
    return render_template("successful1.html")


@app.route('/uordered')
def uordered():
    pro = Buy.query.filter_by(uowner=current_user.id).all()
    return render_template("uordered.html",mat=pro)


@app.route('/ucontact',methods=['GET', 'POST'])
def ucontact():
    if request.method=='POST':
        subject= request.form['subject']
        message= request.form['message']
        new1 = Feedback(name=current_user.username,email=current_user.email,phone=current_user.phone,subject=subject,message=message,usertype='user')
        try:
            db.session.add(new1)
            db.session.commit()
            return redirect('/uindex')

        except:
            return 'not add'  
    return render_template("ucontact.html")


@app.route('/scontact',methods=['GET', 'POST'])
def scontact():
    if request.method=='POST':
        subject= request.form['subject']
        message= request.form['message']
        new1 = Feedback(name=current_user.username,email=current_user.email,phone=current_user.phone,subject=subject,message=message,usertype='seller')
        try:
            db.session.add(new1)
            db.session.commit()
            return redirect('/sindex')

        except:
            return 'not add'  
    return render_template("scontact.html")

@app.route('/sordered')
def sordered():
    pro = Buy.query.filter_by(sowner=current_user.id).all()
    return render_template("sordered.html",mat=pro)

@app.route('/sstatus/<int:id>',methods=['GET','POST'])
def sstatus(id):
    pro = Buy.query.filter_by(sowner=current_user.id).all()
    product = Buy.query.get_or_404(id)
    if request.method=='POST':
        product.delivery= request.form['name']
        db.session.commit()
        return redirect('/sordered')
    return render_template("sordered.html",mat=pro)

@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')


@app.route('/imageadd',methods=['POST','GET'])
def imageadd():
    form=Imageadd()

    if form.validate_on_submit():

        if form.pic.data:
            pic_file = save_picture(form.pic.data)
            view = pic_file
        print(view)  
    
        gallery = Gallery(name=form.name.data,img=view )
       
        db.session.add(gallery)
        db.session.commit()
        print(gallery)
        flash('image added')
        return redirect('/viewimage')
            
    return render_template('imageadd.html',form=form)

@app.route('/viewimage')
def viewimage():
    gallery=Gallery.query.all()
    return render_template('viewimage.html',gallery=gallery)


@app.route("/view/<int:id>", methods=['GET', 'POST'])
def update_post(id):
    gallery = Gallery.query.get_or_404(id)
    form = Imageupdate()
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            gallery.img = picture_file
        gallery.name = form.name.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/viewimage')
    elif request.method == 'GET':
        form.name.data = gallery.name
    image_file = url_for('static', filename='pics/' + gallery.img)
    return render_template('galleryupdate.html',form=form)

@app.route("/view/<int:id>/delete")
def deleteimage(id):
    gallery =Gallery.query.get_or_404(id)
    db.session.delete(gallery)
    db.session.commit()
    flash('image has been deleted!', 'success')
    return redirect('/viewimage')

@app.route('/pfeedbackview')
def pfeedbackview():
    feedback1=Feedback.query.filter_by(usertype='public').all()
    return render_template("pfeedbackview.html",feedback=feedback1)

@app.route('/ufeedbackview')
def ufeedbackview():
    feedback1=Feedback.query.filter_by(usertype='user').all()
    return render_template("ufeedbackview.html",feedback=feedback1)

@app.route('/sfeedbackview')
def sfeedbackview():
    feedback1=Feedback.query.filter_by(usertype='seller').all()
    return render_template("sfeedbackview.html",feedback=feedback1)

@app.route('/aproductview')
def aproductview():
    user = Materials.query.all()
    return render_template("aproductview.html",user=user)


@app.route('/uprofile/<int:id>',methods=['GET','POST'])
def uprofile(id):
    form = Profile()
    login = Login.query.get_or_404(id)
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            login.image_file = picture_file
        login.username = form.username.data
        login.address = form.address.data
        login.phone = form.phone.data
        login.email = form.email.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/uindex')
    elif request.method == 'GET':
        form.username.data = login.username
        form.address.data = login.address
        form.phone.data = login.phone
        form.email.data = login.email
        form.pic.data = login.image_file
    image_file = url_for('static', filename='pics/' + login.image_file)
    return render_template("uprofile.html",form=form)

@app.route('/sprofile/<int:id>',methods=['GET','POST'])
def sprofile(id):
    form = Profile()
    login = Login.query.get_or_404(id)
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            login.image_file = picture_file
        login.username = form.username.data
        login.address = form.address.data
        login.phone = form.phone.data
        login.email = form.email.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/sindex')
    elif request.method == 'GET':
        form.username.data = login.username
        form.address.data = login.address
        form.phone.data = login.phone
        form.email.data = login.email
        form.pic.data = login.image_file
    image_file = url_for('static', filename='pics/' + login.image_file)
    return render_template("sprofile.html",form=form)