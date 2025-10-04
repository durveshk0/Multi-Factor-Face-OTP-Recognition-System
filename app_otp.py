from flask import Flask, render_template, request, redirect, flash, session, url_for
import random
from twilio.rest import Client

app = Flask(__name__)
app.secret_key = 'me'

# Replace these with your actual Twilio credentials
account_sid = "AC7cb8f5045641f145cd352ec64ac1ee81"
auth_token = "6d07ae64afb27cd26caefe3177dc5cee"
client = Client(account_sid, auth_token)
twilio_number = "+17749012631"

# Define the OTP expiration time in seconds (e.g., 300 seconds = 5 minutes)
otp_expiration_time = 300

# Function to validate login
def valid_login(username, password):
    # Replace this with your actual login validation logic
    return username == 'bhushan' and password == '123456'

# Function to generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Function to send OTP via Twilio
def send_otp(otp, to_phone_number):
    try:
        message = client.messages.create(
            body=f"Your OTP is: {otp}",
            from_=twilio_number,
            to=to_phone_number  # Replace with the recipient's phone number
        )
        return True  # OTP sent successfully
    except Exception as e:
        print(f"Failed to send OTP: {e}")
        return False

@app.route('/')
def main():
    return render_template('otp-verification.html', otp_expiration=otp_expiration_time)

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            otp = generate_otp()
            to_phone_number = "+1234567890"  # Replace with the recipient's phone number
            if send_otp(otp, to_phone_number):
                session['otp'] = otp
                return render_template('otp_verification.html', otp=otp, otp_expiration=otp_expiration_time)
            else:
                return render_template('index.html', error='Failed to send OTP')
        else:
            return render_template('index.html', error='Invalid username or password')

    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    user_input = request.form['otp_input']
    stored_otp = session.get('otp')
    if stored_otp and user_input == stored_otp:
        return redirect(url_for('success'))
    else:
        return redirect(url_for('face_recognition'))

@app.route('/success')
def success():
    return "Successful Login! Access granted"

@app.route('/face_recognition')
def face_recognition():
    return render_template('findex.html')

if __name__ == '__main__':
    app.run(debug=True, port=8098)