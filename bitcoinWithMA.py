import pyupbit

df = pyupbit.get_ohlcv("BTC")
close = df['close']
ma5 = close.rolling(5).mean()
print(ma5)

