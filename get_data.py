import time
import os
import sys

import pandas as pd
from binance.spot import Spot
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

client = Spot(api_key, api_secret)

def get_data(symbol, interval):
    directory = f'data/{symbol}'
    file_path = f'{directory}/{symbol}_{interval}.csv'
    
    os.makedirs(directory, exist_ok=True)

    if not os.path.exists(file_path):
        klines = client.klines(symbol, interval, limit=1000)
        df = pd.DataFrame(klines, columns=[
            'open_time', 'open', 'high', 'low', 'close', 'volume', 
            'close_time', 'quote_asset_volume', 'number_of_trades', 
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        while True:
            klines = client.klines(symbol, interval, limit=1000, endTime=int(df['open_time'].iloc[0])-1)
            if not klines:
                break
            df = pd.concat([pd.DataFrame(klines, columns=df.columns), df])
            time.sleep(0.2)

        df = df.drop(columns=['close_time', 'ignore'])
        df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
        df = df.rename(columns={'open_time':'time'}).set_index('time')
        df = df.apply(pd.to_numeric, errors='coerce')
        
        df.to_csv(file_path)
    else:
        df = pd.read_csv(file_path, index_col='time')
        df.index = pd.to_datetime(df.index)

    return df

if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.argv.extend(['BTCUSDT', '1d'])
    symbol, interval = sys.argv[1], sys.argv[2]
    get_data(symbol, interval)
