import json
import hmac
import hashlib
import base64
import time 
import pandas as pd
import http.client
from get_trading_uuid import get_trading_uuid


coinbase_key=""
coinbase_secret=""

def send_limit_buy(amount_to_buy,limit_price):

    timestamp = str(int(time.time()))
    secretKey= coinbase_secret
    accessKey = coinbase_key
    conn = http.client.HTTPSConnection("api.coinbase.com")
    method = "POST"
    path = "/api/v3/brokerage/orders"
    int_order_id = get_trading_uuid()

    payload = json.dumps({
                                            "client_order_id": str(int_order_id),
                                            "product_id": "BTC-USD",
                                            "side": "BUY",
                                            "order_configuration": {
                                                "limit_limit_gtc": {
                                                    "base_size": str(amount_to_buy),
                                                    "limit_price": str(limit_price),
                                                     #just in case you always want to post first     
                                                    "post_only": True
                                                    }
                                                }
                                            })
    message = timestamp + method + path.split('?')[0] + str(payload)
    signature = hmac.new(secretKey.encode('utf-8'), message.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()

    headers={
    'CB-ACCESS-KEY': accessKey,
    'CB-ACCESS-TIMESTAMP': timestamp,
    'CB-ACCESS-SIGN': signature,
    'accept':'application/json'
    }

    conn.request(method, path, payload, headers)
    res = conn.getresponse()
    info = json.loads(res.read())
    trade_message= info["success"]
    if trade_message == True:
        return True
    else: 
        print(info)
        return False
