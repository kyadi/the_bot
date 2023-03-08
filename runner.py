from oanda_api import OandaAPI

api = OandaAPI()

while True:
    command = input('Enter command, T for trade, Q for to quit, C to close trade, SL to set stop loss :  ')
    if command == 'T':
        tradeID, tp, sl = api.placeTrade("AUD_CHF", -100, take_profit=0.6572, stop_loss=0.6599)
        print("you have made a trade with ID: ", tradeID, ", take profit of: ", tp,", and stop loss of: ", sl)
        pass
    elif command=='C':
        trade_id = input("Enter trade ID that you wish to close:  ")
        api.close_trade(trade_id)

    elif command=='SL':
        trade_id = input("Enter trade ID that you wish to set stop loss:  ")
        price = input("Enter the stop loss price:  ")
        reply = api.set_sl_tp("STOP_LOSS", price, trade_id)
        print(reply)
    elif command=='Q':
        break
    else:
        print('enter correct commands, either T , Q, C, SL in block letters')
        pass