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
app.config['MAIL_PASSWORD'] = config("MAIL_PASSWORD")  # Consider using environment variables

mail = Mail(app)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

@app.route('/send-email')
def send_email():
    try:
        msg = Message('Hello from Flask',
                    sender='noreply@ruma.stemgon.co.za',
                    recipients=['crn96m@gmail.com'])
        msg.body = 'This is a test email sent asynchronously from a Flask app.'

        # Start a new thread for async sending
        thread = threading.Thread(target=send_async_email, args=(app, msg))
        thread.start()

        return jsonify({'status': 'Email is being sent asynchronously'}), 200
    except:
        return jsonify({'status': 'Email failed to send asynchronously'}), 400

if __name__ == "__main__":
    app.run(debug=True)