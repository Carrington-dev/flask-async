import json
from flask import Flask, request, jsonify
from sparkpost import SparkPost
from threading import Thread
from decouple import config

app = Flask(__name__)

# Your SparkPost API Key
SPARKPOST_API_KEY = config("MAIL_PASSWORD")  # Consider using environment variables

sp = SparkPost(SPARKPOST_API_KEY)

def send_email_async(to, subject, message):
    try:
        sp.transmissions.send(
            recipients=[to],
            html=message,
            from_email='noreply@ruma.stemgon.co.za',
            subject=subject
        )
    except Exception as e:
        print(f"Email sending failed: {e}")

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "No JSON data provided"}), 400
    print(data)
    to = data['to']
    subject = data['subject']
    message = data['message']

    # Send email in a background thread
    Thread(target=send_email_async, args=(to, subject, message)).start()

    return jsonify({'status': 'Email is being sent asynchronously'}), 200

if __name__ == '__main__':
    app.run(debug=True)
