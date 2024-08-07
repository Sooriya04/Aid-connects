from flask import Flask, render_template, request
from twilio.rest import Client

ACCOUNT_SID = "xxxxxxxxxxxx"
AUTH_TOKEN = "xxxxxxxxxxxx"

app = Flask(__name__)

@app.route('/donate-details', methods=['GET', 'POST'])
def donate_page():
    if request.method == 'POST':
        try:
            name = request.form['name']
            no = request.form['phno']
            add = request.form['address']
            text = request.form['textarea']
            city = request.form['city']
            state = request.form['state']
            pincode = request.form['pincode']
            client = Client(ACCOUNT_SID, AUTH_TOKEN)
            greetings = f"A Heartfelt Contribution from {name}"
            address = f"{add},\n{city},\n{state} - {pincode}"
            contents = f"{greetings}\n{name} has donated the following items to support your work.\n He has the following items {text}\n His address is {address}\nPhone Number : {no}"
            message = client.messages.create(
                body=contents,
                from_="+12562545966",
                to="your phone number"
            )
            print(f"Message sent: {message.sid}")
        except Exception as e:
            print(f"Error: {e}")
            return render_template('donate.html', msg = False)
    return render_template('donate.html', msg = True)
if __name__ == "__main__":
    app.run(debug=True)
