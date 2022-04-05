from pprint import isreadable
from twilio.rest import Client
import numpy as np
import pandas as pd
from subprocess import Popen, PIPE
import json
from datetime import date, datetime
import time
import hmac
import hashlib
import base64
import requests
import schedule
import config

# TO DO LIST
# Protect vars
# Add timed texts
# Find a way to store prices of when the coin was bought
# Add a Gains and losses function
# Create a flask website
# Format prices to end in 0 if they are to the tenth - DONE

# Coinbase Pro API endpoint:
# Credit simplyrangel
endpoint = "https://api.exchange.coinbase.com"

# Get all Coinbase Pro trading pairs:
cmd = [
    "curl",
    "%s/products"%endpoint,
    "--header",
    "Accept: application/json",
    "--header",
    "Content-Type: application/json",
    ]
p = Popen(cmd,stdout=PIPE,stderr=PIPE)
stdout,stderr = p.communicate()

# parse stdout json data:
products_query = json.loads(stdout)

# Find a way to put protect these
API_SECRET  = config.MY_SECRET_API_KEY
API_KEY = config.MY_API_KEY
API_PASSPHRASE  = config.MY_API_PASSPHRASE

# signature generation function:
def timestamp_and_signature(
    method,
    api_secret,
    request_path,
    body,
    ):
    hmac_key = base64.b64decode(api_secret)
    timestamp = str(time.time())
    message = timestamp + method + request_path + body
    message = message.encode('ascii')
    signature = hmac.new(
        hmac_key,
        message,
        hashlib.sha256,
        )
    signature_b64 = base64.b64encode(
        signature.digest()
        ).decode('utf-8')
    return timestamp, signature_b64

    # create the timestamp and the signature:
accounts_url = "https://api.exchange.coinbase.com/accounts"
timestamp, sign = timestamp_and_signature(
    "GET",
    API_SECRET,
    "/accounts",
    "", #no body message necessary
    )

# define required commands that don't require 
# authentication:
unauth_cmd = [
    "curl",
    accounts_url,
    "--header",
    "Accept: application/json",
    "--header",
    "Content-Type: application/json",
    ]

# define the required authentication commands:
auth_cmd = [
    "--header",
    "CB-ACCESS-KEY: %s"%API_KEY,
    "--header",
    "CB-ACCESS-SIGN: %s"%sign,
    "--header",
    "CB-ACCESS-TIMESTAMP: %s"%timestamp,
    "--header",
    "CB-ACCESS-PASSPHRASE: %s"%API_PASSPHRASE,
    ]

# submit request:
accounts_cmd = unauth_cmd + auth_cmd
p = Popen(accounts_cmd,stdout=PIPE,stderr=PIPE)
stdout,stderr = p.communicate()
accounts_output = json.loads(stdout)

def extract_balances(output):
    accounts = []
    for account in output:
        balance = float(account["balance"])
        if balance > 0.0:
            accounts.append(account)
    return accounts

# actual extraction:
accounts = extract_balances(accounts_output)

# Getting a USD balance of a portfolio

def portfolioValue(accounts):
    totalValue = 0
    output = str(datetime.now().strftime("%m/%d/%Y at %I:%M %p\n"))
    for account in accounts:
        coin = account['currency'] + "USDT"
        # Add statements if a coin isnt in the API
        if coin != "USDUSDT":
            key = "https://api.binance.com/api/v3/ticker/price?symbol={currency}".format(currency = coin)
            data = requests.get(key)
            data = data.json()
            usdPrice = round(float(data['price']) * float(account['balance']),2)
            stringPrice = "${:,.2f}".format(usdPrice)
            totalValue += usdPrice
            output += account['currency'] + " - " + stringPrice +"\n"
    output += "\nTotal: " + "${:,.2f}".format(totalValue)
    return output

# Sample Output
# [{'id': '',
#  'currency': 'ATOM',
#  'balance': '0.0000660000000000',
#  'hold': '0.0000000000000000',
#  'available': '0.000066',
#  'profile_id': '',
#  'trading_enabled': True},

# Twilio
# To do: When Coinbase Pro is working, add a time module so it sends texts every x amnt of time

def sendMSG():
    account_sid = config.MY_ACCOUNT_SID
    auth_token  = config.MY_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    to = config.myNumber, 
    from_= config.twilioNumber,
    body=portfolioValue(accounts))

schedule.every(30).minutes.do(sendMSG)
# Send timed texts 
#while 1:
#    schedule.run_pending()
#    time.sleep(1)

dt = datetime.now().strftime("%M")
""" while 1:
    dt = datetime.now().strftime("%M")
    if int(dt) % 30 == 0:
        sendMSG()
        print("Sent at " + datetime.now().strftime("%M"))
        time.sleep(1800) """

sendMSG()
