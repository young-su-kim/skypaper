import time
import pyupbit
import datetime
import schedule
from fbprophet import Prophet

access = ""
secret = ""

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=30) #30일로 변경
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=30) #30일로 변경
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

predicted_close_price = 0
def predict_price(ticker):
    """Prophet으로 당일 종가 가격 예측"""
    global predicted_close_price
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=600, period=1) #당일종가예측 600시간 테이터 시간수집 20210728 count=600, period=1 추가
    df = df.reset_index()
    df['ds'] = df['index']
    df['y'] = df['close']
    data = df[['ds','y']]
    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=24, freq='H')
    forecast = model.predict(future)
    closeDf = forecast[forecast['ds'] == forecast.iloc[-1]['ds'].replace(hour=9)]
    if len(closeDf) == 0:
        closeDf = forecast[forecast['ds'] == data.iloc[-1]['ds'].replace(hour=9)]
    closeValue = closeDf['yhat'].values[0]
    predicted_close_price = closeValue
predict_price("KRW-BTC")
schedule.every().hour.do(lambda: predict_price("KRW-BTC"))

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)
        schedule.run_pending()

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC", 0.4) #변동성 돌파예측 매수가
            current_price = get_current_price("KRW-BTC") #현재가
            if target_price < current_price and current_price < predicted_close_price: #예측 매수조건 - 매수가<현재가<예상종가 이면 매수
                krw = get_balance("KRW")
                if krw > 5000: #보유자산 5천이상이면 매수
                    upbit.buy_market_order("KRW-BTC", krw*0.9995) #0.9995는 수수료
        else:
            btc = get_balance("BTC") #종가에 전량매도
            if btc > 0.00008: # 현재잔고가 5천원이상이면 
                upbit.sell_market_order("KRW-BTC", btc*0.9995) #8시 50분부터 전량 매도, 0.9995는 수수료
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
