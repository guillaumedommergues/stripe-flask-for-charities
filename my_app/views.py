from flask import Flask, Response,render_template, request, redirect, url_for,session
from my_app import app
import stripe
import datetime



stripe_keys = {
  'secret_key': 'your secret key ',
  'publishable_key': 'your publishable key'
}

stripe.api_key = stripe_keys['secret_key']




@app.route('/',methods=['GET','POST'])
def main():
    return render_template("main.html", key=stripe_keys['publishable_key'])



@app.route('/one_time_payment',methods=['POST'])
def one_time_payment():

    if request.form['paymentAmount']:
        amount=int(request.form['paymentAmount'])*100
    else:
        amount=360*100

    customer = stripe.Customer.create(
        email=request.form['stripeTokenEmail'],
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    return redirect(url_for('main'))



@app.route('/monthly_payment',methods=['POST'])
def monthly_payment():
    print "monthly"

    if request.form['paymentAmount']:
        amount=int(request.form['paymentAmount'])*100
    else:
        amount=360*100

    plan_name= "monthly for %s per month" % (amount)

    try:
        plan = stripe.Plan.create(
        name=plan_name,
        id=plan_name,
        interval="month",
        currency="usd",
        amount=amount,
        )
    except:
        pass


    customer = stripe.Customer.create(
        email=request.form['stripeTokenEmail'],
        source=request.form['stripeToken']
    )

    stripe.Subscription.create(
        customer=customer.id,
        items=[{"plan": plan_name, },],
        )

    return redirect(url_for('main'))


