import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime

import base64


# This class stores the Mpesa credentials required for generating an access token.
class MpesaC2bCredential:
    # The Consumer Key for the Mpesa API.
    consumer_key = 'ShetFZbeG2YJSXIvUojmgGrzISPjJ4EQ'
    # The Consumer Secret for the Mpesa API.
    consumer_secret = 'd8VqfDwpR6MExxAU'
    # The URL for generating the access token.
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'


# This class generates the Mpesa access token using the credentials stored in MpesaC2bCredential.
'''class MpesaAccessToken:
    r = requests.get(MpesaC2bCredential.api_URL,  # Sends a GET request to the Mpesa API URL to generate the token.
                     auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret))  # Authenticates the request with the consumer key and consumer secret.
    # Converts the response from JSON format to a Python dictionary.
    print(r.text)
    mpesa_access_token = json.loads(r.text)
    # Stores the generated access token.
    validated_mpesa_access_token = mpesa_access_token['access_token']'''

# This class generates the online password required for processing an Mpesa transaction.


class LipanaMpesaPpassword:
    # Generates the current time in the specified format.
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    # The short code for the business making the transaction.
    Business_short_code = "174379"
    # The passkey for the Mpesa API.
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    # Concatenates the business short code, passkey, and time to form the data to be encoded.
    data_to_encode = Business_short_code + passkey + lipa_time
    # Encodes the data using base64 encoding.
    online_password = base64.b64encode(data_to_encode.encode())
    # Decodes the encoded password to string format.
    decode_password = online_password.decode('utf-8')


def getAccessToken():
    # Mpesa Consumer key and secret
    consumer_key = 'XjWEg9z1ihL9zoXO1JRaCOhfIJAgB8cu'
    consumer_secret = 'y48BAeDDA0AgXqI2'
    # Mpesa OAuth API URL
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    # Make a GET request to the API URL with consumer key and secret as basic auth credentials
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(url, auth=(consumer_key, consumer_secret))

    if response.status_code != 200:
        print(response.content)
        print("No data")
    else:
        data = json.loads(response.content)
        token = data["access_token"]
        return token
