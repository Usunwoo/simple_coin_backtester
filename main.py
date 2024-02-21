import sys

import pandas as pd
from backtesting import Backtest

from get_data import get_data
from strategy import EmaCross


def main():
    # 데이터 로드
    if len(sys.argv) == 1:
        sys.argv.extend(['BTCUSDT', '1d'])
    symbol, interval = sys.argv[1], sys.argv[2]
    df = get_data(symbol, interval).iloc[:,:5]
    df.columns=['Open', 'High', 'Low', 'Close', 'Volume']

    # 백테스팅
    cash = 10000
    fee = 0.0005
    leverage = 1

    strategy = EmaCross
    bt = Backtest(df, strategy, cash=cash, commission=fee, margin=1/leverage, trade_on_close=True, exclusive_orders=True)
    stats = bt.run()
    print(stats)
    bt.plot(resample=False)

if __name__ == '__main__':
    main()
