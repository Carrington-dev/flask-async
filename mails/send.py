import requests
from decouple import config

API_KEY = config('MAIL_PASSWORD')

url = 'https://api.sparkpost.com/api/v1/transmissions'

payload = {
    "options": {
        "sandbox": False
    },
    "content": {
        "from": {
            "email": "Payglen <noreply@ruma.stemgon.co.za>",
            "name": "Your Company"
        },
        "subject": "Your OTP Code",
        "html": """
        <!DOCTYPE html>
        <html>
        <head><title>OTP</title></head>
        <body>
            <h2>Hello {{name}},</h2>
            <p>Your One-Time Password is: <strong>{{otp}}</strong></p>
        </body>
        </html>
        """,
        "use_draft_template": False
    },
    "substitution_data": {
        "name": "Carrington",
        "otp": "876098"
    },
    "recipients": [
        {
            "address": {
                "email": f"{config('ADMIN_EMAIL')}"
            }
        }
    ]
}

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.status_code)
print(response.json())
