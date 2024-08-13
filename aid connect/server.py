from flask import Flask, render_template, request
from twilio.rest import Client
from data import SID, TOKEN, FROM_NO, TO_NO
from flask_sqlalchemy import SQLAlchemy

# Twilio credentials
ACCOUNT_SID = SID
AUTH_TOKEN = TOKEN

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datas.db'
db = SQLAlchemy(app)

class Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phno = db.Column(db.String(15), nullable=False)
    mail = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

def get_phonenumber():
    try:
        with app.app_context():
            phonenumbers = db.session.query(Details.phno).all()
            phno_list = [phno[0] for phno in phonenumbers]
            print(phno_list)
    except Exception as e:
        print(f"Error while retrieving the phone numbers: {e}")

# HOMEPAGE
@app.route('/')
def homepage():
    return render_template('index.html')

# GET-HELP
@app.route('/gethelp', methods=['POST', 'GET'])
def get_help():
    if request.method == 'POST':
        username = request.form['name']
        user_phno = request.form['phno']
        user_email = request.form['email']
        address = request.form['address']
        city = request.form['city']
        dis = request.form['district']
        state = request.form['state']
        zipcode = request.form['zip']
        user_add = f"{address}, {city}, {dis}, {state}, code - {zipcode}"
        
        new_details = Details(name=username, phno=user_phno, mail=user_email, address=user_add)
        
        try:
            with app.app_context():
                db.session.add(new_details)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Database Error: {e}")
            return render_template("error.html")
        
        # Print all phone numbers after the new entry is added
        get_phonenumber()
        
        return render_template('thanks.html')
    return render_template('get-help.html')

# DONATE-DETAILS
@app.route('/donate-details', methods=['GET', 'POST'])
def donate_page():
    if request.method == 'POST':
        try:
            name = request.form['name']
            phone_number = request.form['phno']
            recipient_email = request.form['email']
            address = request.form['address']
            donation_details = request.form['textarea']
            city = request.form['city']
            state = request.form['state']
            pincode = request.form['pincode']

            #TWILIO
            client = Client(ACCOUNT_SID, AUTH_TOKEN)
            greetings = f"A Heartfelt Contribution from {name}"
            full_address = f"{address},\n{city},\n{state} - {pincode}"
            contents = (f"{greetings}\n{name} has donated the following items to support your work.\n"
                        f"They have donated the following items: {donation_details}\n"
                        f"Their address is {full_address}\nPhone Number: {phone_number}")
            
            # Sending SMS
            message = client.messages.create(
                body=contents,
                from_=FROM_NO,
                to=TO_NO
            )
            print(f"Message sent: {message.sid}")
            return render_template('thanks.html')
        except Exception as e:
            print(f"Error: {e}")
            return render_template('error.html')
    return render_template('donate.html')

if __name__ == "__main__":
    app.run(debug=True)
