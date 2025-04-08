import json
from string import Template
from flask import Flask, request, jsonify
from sparkpost import SparkPost
from threading import Thread
from decouple import config

app = Flask(__name__)

# Your SparkPost API Key
SPARKPOST_API_KEY = config("MAIL_PASSWORD")  # Consider using environment variables
ADMIN_EMAIL = config('ADMIN_EMAIL')
sp = SparkPost(SPARKPOST_API_KEY)


def load_html_template(name: str) -> str:
    with open("send.html", "r", encoding="utf-8") as file:
        template = Template(file.read())
        return template.safe_substitute({"substitution_data": { 
                "name": "john",
                "otp": "123456"
            }})

def send_email_async(to, subject, message):
    try:
        html_content = load_html_template(name="Carrington")
        sp.transmissions.send(
            # recipients=[to],
             recipients=[{
                'address': to,
                'substitution_data': {
                    'username': 'Carrington06',
                    'name': 'Carrington',
                    'otp': '876098'
                }
            }],
            html=html_content,
            from_email='Payglen <noreply@ruma.stemgon.co.za>',
            subject=subject
        )
    except Exception as e:
        print(f"Email sending failed: {e}")

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "No JSON data provided"}), 400
    
    to = data.get('to', ADMIN_EMAIL)
    subject = data.get('subject', "Testing App")
    message = data.get('message', "Testing App")

    # Send email in a background thread
    Thread(target=send_email_async, args=(to, subject, message)).start()

    return jsonify({'status': 'Email is being sent asynchronously'}), 200

if __name__ == '__main__':
    app.run(debug=True)
