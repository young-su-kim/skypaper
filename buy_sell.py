import pyupbit
import pprint

access = ""
secret = ""

#로그인
upbit=pyupbit.Upbit(access,secret)
print("autotrade start")

#시장가
#rfr_price = pyupbit.get_current_price("KRW-BTC")
#print(btc_price)


#시장가보다 저가매수
#resp=upbit.buy_market_order("KRW-BTC",10.1,600) #가격, 수량
#pprint.pprint(resp)

#잔고조회
btc=upbit.get_balance("KRW-BTC") 

#지정가 고가매도주문
if btc>0
resp1=upbit.sell_limit_order("KRW-BTC",42210000,btc*0.9995) #지정가 전량매도
pprint.pprint(resp1)
#resp1=upbit.sell_limit_order("KRW-BTC",,) #지정가 및 지정수량 매도

#지정하락시매도주문
#resp2=upbit.sell_limit_order("KRW-BTC",40000000,btc*0.9995) # 매수가의 2%하락시 전량매도
#pprint.pprint(resp2)

#과도하락매수취소
#uuid=""
#if rfr_price=rfr_price*0.95
#resp3=upbit.cancel_order(uuid) # 매수가의 2%하락시 전량매도
#pprint.pprint(resp3)
