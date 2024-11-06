from flask import Flask, render_template, request, jsonify
from twilio.rest import Client
import os
import logging
import re  
from dotenv import load_dotenv

app = Flask(__name__)

# Load Twilio credentials from environment variables
load_dotenv()
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_PHONE_NUMBER')

# Verify that credentials are loaded
if not all([account_sid, auth_token, twilio_number]):
    raise EnvironmentError("Twilio credentials are missing in .env file.")

# Create a Twilio client
client = Client(account_sid, auth_token)

# Setup logging
logging.basicConfig(level=logging.INFO)

# Function to make a voice call
def make_call(phone_number):
    try:
        call = client.calls.create(
            twiml='<Response><Say>Ceci est un appel de démonstration !</Say></Response>',
            to=phone_number,
            from_=twilio_number
        )
        return call.sid
    except Exception as e:
        logging.error(f"Erreur lors de l'appel : {str(e)}")
        raise Exception(f"Erreur lors de l'appel : {str(e)}")

# Function to send an SMS
def send_sms(phone_number):
    try:
        message = client.messages.create(
            body="Hello!",  # SMS content
            from_=twilio_number,
            to=phone_number
        )
        return message.sid
    except Exception as e:
        logging.error(f"Erreur lors de l'envoi de SMS : {str(e)}")
        raise Exception(f"Erreur lors de l'envoi de SMS : {str(e)}")

# Serve the landing page with the phone number input form
@app.route('/')
def index():
    return render_template('index.html')

# Handle the form submission
@app.route('/submit-number', methods=['POST'])
def submit_number():
    data = request.get_json()
    phone_number = data.get('phoneNumber')
    logging.info(f"Received phone number: {phone_number}")
    
    
    phone_pattern = r'^\+?[0-9]{1,3}[0-9]{9,14}$'  

    if not re.match(phone_pattern, phone_number):
        # Return a validation error response if the phone number is invalid
        return jsonify({
           'message': 'Veuillez entrer un numéro de téléphone valide.',
            'error': 'Numéro de téléphone invalide.'
        }), 400  # Bad Request

    try:
        # Trigger the call
        call_sid = make_call(phone_number)
    
        # Trigger the SMS
        message_sid = send_sms(phone_number)

        # Return JSON response with success message
        #print("ici")
        return jsonify({
            'message': 'Loading...',
            'call_sid': call_sid,
            'message_sid': message_sid
        })
    
    except Exception as e:
        # Log the error and return error in JSON format
       logging.error(f"Erreur lors du traitement : {str(e)}")
       return jsonify({
           'message': 'Veuillez entrer votre numéro de téléphone, incluant votre indicatif pays (ex: +41 pour la Suisse).',
           'error': str(e)
        }), 500  # Internal Server Error

if __name__ == '__main__':
    app.run(debug=True, port=8080,host="0.0.0.0", use_reloader=False)
