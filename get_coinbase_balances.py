import hmac
import hashlib
import time 
import requests


coinbase_key= ""
coinbase_secret= ""



def get_balance():

    
    timestamp = str(int(time.time()))
    method= "GET"
    url_path=  "/api/v3/brokerage/accounts"
    url = "https://api.coinbase.com/api/v3/brokerage/accounts?limit=250"

    body=""
    message = timestamp+ method+ url_path+ body

    signature = hmac.new(coinbase_secret.encode('utf-8'), message.encode('utf-8'), digestmod=hashlib.sha256).digest()

    headers = {
    "accept": "application/json",
    "CB-ACCESS-KEY": coinbase_key,
    "CB-ACCESS-SIGN": signature.hex(),
    "CB-ACCESS-TIMESTAMP": timestamp
    }

    response = requests.get(url, headers=headers)

    data = response.json()
    first_data = data["accounts"]
    #Note the order should not be changed according to a coinbase dev in the forums 
      # Currently for this specific api key/secret is used to only retrieve two balances total so you will need to check yourself what order everything is coming in
    first_available_balance= float(first_data[0]["available_balance"]["value"])
    cash_available_balance= float(first_data[1]["available_balance"]["value"])
    
    # doing this math so if you use this balance to set an order you will have the correct decimals amounts. Will need to change as each pair has it own rules
    first_available_balance = int(first_available_balance * 10000) / 10000
    cash_available_balance = int(cash_available_balance * 10000) / 10000

    return cash_available_balance,first_available_balance

print(get_stablecoin_balance())
