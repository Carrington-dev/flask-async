from flask import Flask, jsonify
from flask_mail import Mail, Message
import threading
from decouple import config

app = Flask(__name__)

# Configure your email settings
app.config['MAIL_SERVER'] = 'smtp.sparkpostmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'SMTP_Injection'
# app.config['MAIL_USERNAME'] = 'noreply@ruma.stemgon.co.za'
app.config['MAIL_PASSWORD'] = config("MAIL_PASSWORD")  # Consider using environment variables
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

@app.route('/send-email', methods=["GET", "POST"])
def send_email():
    try:
        msg = Message('Hello from Flask',
                    sender='noreply@ruma.stemgon.co.za',
                    recipients=['crn96m@gmail.com'])
        msg.body = 'This is a test email sent asynchronously from a Flask app.'

        # Start a new thread for async sending
        thread = threading.Thread(target=send_async_email, args=(app, msg))
        thread.start()
        print(thread.is_alive)
        return jsonify({'status': 'Email is being sent asynchronously'}), 200
    except:
        return jsonify({'status': 'Email failed to send asynchronously'}), 400
    
@app.route("/")
def index():
    try:
        msg = Message(subject='Hello from the other side!', sender='peter@mailtrap.io', recipients=['paul@mailtrap.io'])
        msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works."
        mail.send(msg)
        return "Message sent!"
    except Exception as e:
        print(e)
        return "Message not sent!"

if __name__ == "__main__":
    app.run(debug=True)