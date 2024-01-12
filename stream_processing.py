import numpy as np
import json
from kafka import KafkaConsumer, KafkaProducer

consumer = KafkaConsumer('my-topic', bootstrap_servers=['localhost:9092'])
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
def is_larger_than_all(matrix, value):
    return np.greater(value, matrix).all()

def moving_average(data, n):
    """
    Calculates the moving average of a stock over a specified number of periods.
    """
    return np.convolve(data, np.ones(n)/n, mode='valid')

def exponential_moving_average(data, n):
    """
    Calculates the exponential moving average of a stock over a specified number of periods.
    """
    alpha = 2/(n+1)
    ema = [data[0]]
    for i in range(1, len(data)):
        ema.append(alpha*data[i] + (1-alpha)*ema[i-1])
    return ema

def relative_strength_index(data, n):
    """
    Calculates the relative strength index of a stock over a specified number of periods.
    """
    delta = np.diff(data)
    gains = delta.copy()
    losses = delta.copy()
    gains[gains < 0] = 0
    losses[losses > 0] = 0
    avg_gain = moving_average(gains, n)
    avg_loss = -moving_average(losses, n)
    rs = avg_gain/avg_loss
    rsi = 100 - (100/(1+rs))
    return rsi


data_by_symbol = {}

for message in consumer:
    data = json.loads(message.value)

    if 'data_type' not in data.keys():
        main_data = data
        print('\n' + 50 * '*' + ' MAIN DATA ' + 50 * '*' + '\n')
      

        
        n = 3
      

    
        symbol = main_data['stock_symbol']
        if symbol not in data_by_symbol:
          data_by_symbol[symbol] = []
        data_by_symbol[symbol].append(main_data)
      
        print(data_by_symbol)
        
        # Calculate the indicators for each stock symbol
        for symbol, data in data_by_symbol.items():
          closing_prices = [d['closing_price'] for d in data]
          if n < len(closing_prices):
              ma = moving_average(closing_prices, n)
              ema = exponential_moving_average(closing_prices, n)
              rsi = relative_strength_index(closing_prices, n)
              print(f"Stock symbol: {symbol}")
              print(f"Moving average: {ma}")
              print(f"Exponential moving average: {ema}")
              print(f"Relative strength index: {rsi}")
              current_price = closing_prices[-1]
              if is_larger_than_all(ma, current_price) and is_larger_than_all(ema, current_price) and is_larger_than_all(rsi, 30):
                  signal = "Buy"
              elif (not is_larger_than_all(ma, current_price)) and (not is_larger_than_all(ema, current_price)) and (not is_larger_than_all(rsi, 30)):
                  signal = "Sell"
              else:
                  signal = "Hold"
              print(f"Signal: {signal}")
              producer.send('my-signal-topic', json.dumps({'stock_symbol': symbol, 'signal': signal}).encode('utf-8'))

    else:
      meta_data = data
      print('\n' + 50 * '*' + ' META DATA ' + 50 * '*' + '\n')
      print(meta_data)
