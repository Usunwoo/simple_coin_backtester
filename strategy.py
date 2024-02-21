import talib
from backtesting import Strategy
from backtesting.lib import crossover


class EmaCross(Strategy):
    future=False
    short=9
    long=25

    def init(self):
        self.short_ema = self.I(talib.EMA, self.data.Close, self.short)
        self.long_ema = self.I(talib.EMA, self.data.Close, self.long)
    def next(self):
        if crossover(self.short_ema, self.long_ema):
            self.buy()
        elif crossover(self.long_ema, self.short_ema):
            if self.future:
                self.sell()
            else:
                self.position.close()

class CustomStrategy(Strategy):
    def init(self):
        pass
    def next(self):
        pass
