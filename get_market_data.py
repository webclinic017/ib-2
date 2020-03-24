from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
from datetime import datetime


class TestApp(EWrapper, EClient):
    
    def __init__(self):
        EClient.__init__(self,self)
        
    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)
        
    def tickPrice(self, reqId, tickType, price, attrib):
        print("Tick Price. Ticker ID: ", reqId, "tick Type:", TickTypeEnum.to_str(tickType), "Price:", price)
        
    def tickSize(self, reqId, tickType, size):
        print("Tick Size. Ticker Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Size:", size)


    #@iswrapper
    def tickByTickMidPoint(self, reqId, time, midPoint):
        super().tickByTickMidPoint(reqId, time, midPoint)
        print("Midpoint. ReqId:", reqId,
              "Time:", datetime.fromtimestamp(time).strftime("%Y%m%d %H:%M:%S"),
              "MidPoint:", midPoint)

    def tickByTickBidAsk(self, reqId, time, bidPrice, askPrice, bidSize, askSize, tickAttribBidAsk):
        super().tickByTickBidAsk(reqId, time, bidPrice, askPrice, bidSize, askSize, tickAttribBidAsk)
        print("Midpoint. ReqId:", reqId,
              "Time:", datetime.fromtimestamp(time).strftime("%Y%m%d %H:%M:%S"),
              "BidPrice", bidPrice,
              "AskPrice", askPrice,
              "BidSize", bidSize,
              "AskSize", askSize)
        print(tickAttribBidAsk.bidPastLow, tickAttribBidAsk.askPastHigh)
       
    
def main():
    
    app = TestApp()
    
    app.connect("127.0.0.1", 7497, 0)

    EURUSD = Contract()
    EURUSD.symbol = "EUR"
    EURUSD.secType = "CASH"
    EURUSD.exchange = "IDEALPRO"
    EURUSD.currency = "USD"

    # EURUSD = Contract()
    # EURUSD.symbol = "EUR"
    # EURUSD.secType = "CASH"
    # EURUSD.exchange = "IDEALPRO"
    # EURUSD.currency = "USD"

    
    app.reqMarketDataType(1) #switch to delayed-frozen data if live is not available
    #app.reqMktData(1,contract, "", False, False, [])
    #app.reqTickByTickData(19004, contract, "MidPoint", 0, False)
    app.reqTickByTickData(1, EURUSD, "BidAsk", 0, False)
    print("-------------CHECK---------------")
    
    app.run()
    
if __name__ == "__main__":
    main()