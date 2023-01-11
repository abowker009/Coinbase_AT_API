
import websocket
import json
import time
import hmac 
import hashlib 

#put the respective keys into here. Permissions I have to set for websocket: wallet:accounts:read; wallet:notifications:read; wallet:user:read
API_KEY = ""
SECRET = ""

#this is where the orderbook is saved
bid_orderbook = {}
offer_orderbook = {}


def get_orderbook_depth(websocket_message):
   
    for update in websocket_message:
        side = update['side']
        price = float(update['price_level'])
        new_quantity = float(update['new_quantity'])

        if side == 'bid':
            if new_quantity != 0:
                bid_orderbook[price] = new_quantity
            else:
                del bid_orderbook[price]
        else:
            if new_quantity != 0:
                offer_orderbook[price] = new_quantity
            else:
                del offer_orderbook[price]
     # sort the bids 
    sorted_bids= sorted(bid_orderbook.items(), key= lambda x: x[0],reverse=True)
    bid_orderbook.clear()
    bid_orderbook.update(sorted_bids)
    sorted_bids.clear()
    #sort the offers
    sorted_offers= sorted(offer_orderbook.items(), key= lambda x: x[0],reverse=False)
    offer_orderbook.clear()
    offer_orderbook.update(sorted_offers)
    sorted_offers.clear()
    #print(bid_orderbook)
    #print(offer_orderbook)
    first_price_bid, first_quantity_bid  = next(iter(bid_orderbook.items()))
    first_price_offer, first_quantity_offer  = next(iter(offer_orderbook.items()))

    return first_price_bid,first_quantity_bid,first_price_offer,first_quantity_offer

def sign_message(message):
    digest = hmac.new(SECRET.encode('utf-8'), message.encode('utf-8'), digestmod=hashlib.sha256).digest()
    return digest.hex()
    



def run_dai_ws():

    subscribe_msg = '''
    {
        "type": "subscribe",
        "product_ids": [
            "BTC-USD"
        ],
        "channel": "level2"
    }
    '''


    subs = json.loads(subscribe_msg)
    subs["api_key"] = API_KEY
    subs["timestamp"] = str(int(time.time()))
    subs["signature"] = sign_message(str(subs["timestamp"])+"level2"+"BTC-USD")
    ws = websocket.create_connection("wss://advanced-trade-ws.coinbase.com")
    ws.send(json.dumps(subs))


    
    while True: 
        ticker_data = ws.recv()
        ticker_json = json.loads(ticker_data)
        message_number= ticker_json["sequence_num"]
        
        #this closes the websocket after the 4th sequence number. take this out if you want it to run forever. Note you will run into an error and need to handle this yourself.
        if message_number >= 4: 

            print(close_ws_message(ws))
            break
        elif message_number == 0 or message_number>1:
            print(message_number)
            snapshot= ticker_json["events"][0]["updates"]
            print((get_orderbook_depth(snapshot)))
            
            #run snap shot here
        elif message_number== 1: 
            print("message 1")
        else:
            print(ticker_data)
            break
    return ticker_data




def close_ws_message(ws):
    unsubscribe_msg = '''
    {
        "type": "unsubscribe",
        "product_ids": [
            "BTC-USD"
        ],
        "channel": "level2"
    }
    '''
    subs2 = json.loads(unsubscribe_msg)
    subs2["api_key"] = API_KEY
    subs2["timestamp"] = str(int(time.time()))
    subs2["signature"] = sign_message(str(subs2["timestamp"])+"level2"+"BTC-USD")
    ws.send(json.dumps(subs2))
    ws.close()
    statement = "Websocket was closed"
    return statement

    
run_dai_ws()
