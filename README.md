# CoinbaseProNotis
Because Coinbase Pro does not offer notifications, and I forget to check my account, I have started this project to help with my Python and FLask skills. The goal is to have Twilio SMS bot to send the user updates on their portfolio. I'm still figuring out what I want to send and how I want it to look, but right now it sends all Cryptocurrencies in a Coinbase Pro portfolio, and the USD price of the Crypto Coin along with the total portfolio worth. Texts are sent every 30 minutes.

# Version 1.1
- Protected some variables
- Fixed price formatting
 
# To Do list
- Fix the spaghetti code
- Find how much a Crypto coin was worth when user first bought it and display total gain/loss in USD
- Create a webapp using Flask framework
- Add error handling for Crypto Currencies that aren't found in the API
