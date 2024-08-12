from flask import Flask, render_template, request
from twilio.rest import Client
import smtplib
import json
from data import SID, TOKEN, FROM_NO, TO_NO, MAIL, PASSWORD, RECIVER_MAIL
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
    phno = db.Column(db.String(15), unique=True, nullable=False)
    mail = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

# Email sending
def send_email(recipient_email, subject, message):
    try:
        port = 587
        with smtplib.SMTP("smtp.gmail.com", port) as connection:
            connection.starttls()
            connection.login(MAIL, PASSWORD)
            email_message = f"Subject: {subject}\n\n{message}"
            connection.sendmail(MAIL, recipient_email, email_message)
            print("Email is sent successfully")
    except Exception as e:
        print(f"Error while sending the message: {e}")

# Sending email for donation details
def sending_mail(subject, message):
    try:
        send_email(RECIVER_MAIL, subject, message)
        print("Email sent to recipient.")
    except Exception as e:
        print(f"Error while sending the email: {e}")
        return render_template("servererror.html")

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
        address = request.form['add']
        city = request.form['city']
        dis = request.form['dis']
        state = request.form['state']
        zipcode = request.form['code']
        user_add = f"{address}, {city}, {dis}, {state}, code - {zipcode}"
        
        new_details = Details(name=username, phno=user_phno, mail=user_email, address=user_add)
        with app.app_context():
            db.session.add(new_details)
            db.session.commit()
        
        newdata = {
            "users": {
                "username": username,
                "phone-number": user_phno,
                "email": user_email,
                "address": user_add
            }
        }
        
        try:
            with open('data.json', 'r') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = {}
        except FileNotFoundError:
            data = {}
        
        data.update(newdata)
        
        try:
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            print("Data is updated")
        except Exception as e:
            print(f"Unknown error occurred: {e}")
        
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
            
            client = Client(ACCOUNT_SID, AUTH_TOKEN)
            greetings = f"A Heartfelt Contribution from {name}"
            full_address = f"{address},\n{city},\n{state} - {pincode}"
            contents = (f"{greetings}\n{name} has donated the following items to support your work.\n"
                        f"They have donated the following items: {donation_details}\n"
                        f"Their address is {full_address}\nPhone Number: {phone_number}")
            
            message = client.messages.create(
                body=contents,
                from_=FROM_NO,
                to=TO_NO
            )
            
            sending_mail("Donation Details", contents)
            print(f"Message sent: {message.sid}")
            return render_template('thanks.html')
        except Exception as e:
            print(f"Error: {e}")
            return render_template('error.html')
    return render_template('donate.html')

if __name__ == "__main__":
    app.run(debug=True)
