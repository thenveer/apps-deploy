import time
import datetime 

from flask import Flask, render_template, request, redirect, url_for

import models
from models import app, db

@app.route("/")
def hello():
    session = db.session()
    customers = session.query(models.Customer).all()
    return render_template("customers.html", customers = customers)

@app.route("/invoices", methods=['GET'])
def invoices():
    cid = request.args.get('cid')
    added = request.args.get('info')
    session = db.session
    customer = session.query(models.Customer).filter(models.Customer.id == cid).first()
    invoices = session.query(models.Invoice).filter(models.Invoice.customer_id == cid).all()
    if request.headers.get('Accept') == 'application/json':
        ret = []
        for i in invoices:
            ret.append(dict(date = i.date, particulars = i.particulars, amount = i.amount))
        return dict(invoices = ret)
    else:
        return render_template("invoices.html", customer = customer, invoices = invoices, added = added)


            

@app.route("/invoices", methods=['POST'])
def create_invoice():
    session = db.session()
    particulars = request.form['particulars']
    amount = request.form['amount']
    cid = request.form['cid']
    
    invoice = models.Invoice(date = datetime.date.today(),
                             particulars = particulars,
                             customer_id = int(cid),
                             amount = amount)
    
    session.add(invoice)
    session.commit()
    return redirect(url_for('invoices', cid=cid, info="added"))

@app.route("/", methods=['POST'])
def get_data():
    session = db.session()
    name =request.form['name']
    date =request.form['jdate']
    address =request.form['address']
    email =request.form['email']

    c= models.Customer(name =name,
                       jdate =date,
                      address =address,
                       email =email
                          )
    session.add(c)
    session.commit()

    return redirect(url_for('hello'))

    
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/info")
def info():
    session = db.session()
    rows = session.query(models.Customer).count()
     # customer = session.query(models.Customer).filter(models.Customer.id == cid).first()
   # cust= session.query(models.Customer).filter(models.Customer.id == '4').all()
   # obj = session.query(models.Invoice). (models.Invoice.id.desc()).first()
    
   
    return render_template("info.html", row= rows)
