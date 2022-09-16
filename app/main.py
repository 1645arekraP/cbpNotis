import cbpro
import json
from twilio.rest import Client
from config import *
from datetime import date, datetime
import time
import requests

# Coinbase Pro
# This is a function to get the info of a portfolio, if a currency isnt found on the api then 
# the coinbase pro api is used, this is still being worked on for other conversions
def portfolioInfo(accounts):
    output = datetime.now().strftime("%m/%d/%Y at %I:%M %p\n")
    total = 0
    for account in accounts:
        currency = account['currency'] + "USDT"
        url = "https://api.binance.com/api/v3/ticker/price?symbol={currency}".format(currency = currency)
        data = requests.get(url)
        data = data.json()
        # KeyError Exception Handling
        try:
            usd_price = float(data['price'] )* float(account['balance'])
        except KeyError:
            usd_price = float(account['balance'])
        total += usd_price
        usd_price = "${:,.2f}".format(usd_price)
        output += account['currency'] + " - " + usd_price +"\n"
    output += "\nTotal: " + "${:,.2f}".format(total)
    return output

# Twilio
# Sends a SMS messsage 
# Twilio phone numbers are formatted as following, +11234567890
def sendMSG():
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    to = myNumber, 
    from_= twilioNumber,
    body=portfolioInfo(accounts))

# Text Timer
# Fix var names start_time and stop_time are used to silence notifications
# Add infinite loop somewhere and add minutes instead of hours
# Use flask to finish
def timedText(frequency_in_minutes, start_time=0, stop_time=23):
    current_time = int(datetime.now().strftime("%H"))
    while (start_time < current_time < stop_time):
        current_time = int(datetime.now().strftime("%H"))
        print(current_time)
        time.sleep(30)

# Crypto
# Get accounts
url="https://api.exchange.coinbase.com"

client = cbpro.AuthenticatedClient(
    api_key,
    api_secret,
    api_pass,
    api_url=url
)

allAccounts = client.get_accounts()
# Array to hold all accounts that have a balance greater than 0
accounts = [] 

for acc in allAccounts:
    if float(acc.get('balance')) > 0:
        accounts.append(acc)

sendMSG()