from flask import Flask, render_template, request
from twilio.rest import Client
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def donate_page():
    if request.method == ['POST', 'GET']:
        name = request.form['name']
        no = request.form['phno']
        add = request.form['address']
        text = request.form['textarea']
        city = request.form['city']
        state = request.form['state']
        pincode = request.form['pincode']
    return render_template('donate.html')


if __name__ == "__main__":
    app.run(debug = True)