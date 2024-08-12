from flask import Flask, render_template, request
from twilio.rest import Client
import smtplib
import json
from data import SID, TOKEN, FROM_NO, TO_NO, MAIL, PASSWORD
ACCOUNT_SID = SID #USE TWILIO TO GET YOUR SID
AUTH_TOKEN = TOKEN #USE TWILIO TO GET YOUR TOKEN

def send_email(recipient_email, message):
    try:
        port = 587
        with smtplib.SMTP("smtp.gmail.com", port) as connection:
            connection.starttls()
            #MAIL = YOUR_MAIL || PASSWORD = PASSKEY
            connection.login(MAIL, PASSWORD)
            connection.sendmail(MAIL, recipient_email, message)
            print("Email is sent successfully")
    except Exception as e:
        print(f"Error while sending the message: {e}")

app = Flask(__name__)
#HOMEPAGE
@app.route('/')
def homepage():
    return render_template('index.html')

#GET-HELP
@app.route('/gethelp', methods = ['POST', 'GET'])
def get_help():
    if request.method == 'POST':
        name = request.form['name'] 
        phno = request.form['phno']
        email = request.form['email']
        address = request.form['add']
        city = request.form['city']
        dis = request.form['dis']
        state = request.form['state']
        zipcode = request.form['code']
        add = f"{address}, {city}, {dis}, {state}, code - {zipcode}"
        newdata = {
                name: {
                    "username": name,
                    "phone-number": phno,
                    "email": email,
                    "address": add
                }
            }
        try:
            with open('data.json', 'r') as file:
                try:
                    data = json.load(file)
                    print(data)
                except json.JSONDecodeError:
                     data = {} 
        except FileNotFoundError:
                data = {}
        data.update(newdata)
        try: 
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            print("Data is updated")
        except:
            print("unknow error occured")
        return render_template ('thanks.html')
    return render_template ('get-help.html')
print(f"Data successfully written successfully")
#DONATE-DETAILS
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
            contents = f"{greetings}\n{name} has donated the following items to support your work.\nThey have donated the following items: {donation_details}\nTheir address is {full_address}\nPhone Number: {phone_number}"
            
            message = client.messages.create(
                body=contents,
                from_ = FROM_NO, #TWILIO PHONENUMBER
                to = TO_NO #YOUR PHONENUMBER
            )
            send_email(recipient_email, contents) 
            print(f"Message sent: {message.sid}")
            return render_template('thanks.html')
        except Exception as e:
            print(f"Error: {e}")
            return render_template('error.html')
    return render_template('donate.html')

if __name__ == "__main__":
    app.run(debug=True)