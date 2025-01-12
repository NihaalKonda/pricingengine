import backtrader as bt

class Sma(bt.Strategy):
    # creating custom strategy to define parameters/indicators inheriting from bt.strategy base class
    
    params = dict(
            pfast = 60,
            pslow = 128
        )
    
    def __init__(self):
      # defining two simple moving averages
      fast_av = bt.ind.SMA(period=self.p.pfast) #.ind.SMA serves as built in indicator of price over period
      slow_av = bt.ind.SMA(period=self.p.pslow)

      # checking crossover indicator for valid parameters
      if ((self.p.pfast <= self.p.pslow) and (self.p.pslow - self.p.pfast >= 5)) :
        self.crossover = bt.ind.CrossOver(fast_av, slow_av)
        # above creates crossover indicator: -1 when fast above slow, 1 when slow above fast, 0 when no crossover
      else :
        raise bt.StrategySkipError
    
    def next(self):
      # runs on each day of the daily data - defines trading logic
      if not self.position: # makes sure strategy doesn't currently own stock
        if self.crossover==1:
          self.buy() # longing position - placing an order
      elif self.crossover==-1: #strategy is already in the market, so can sell
        self.close() # automatically sells any open long position
    
    def stop(self):
      print("(Fast Av Period: ", self.params.pfast, ") (Slow Av Period: ", self.params.pslow, ") (Portfolio Value: ", self.broker.getvalue(), ")")
      #log backtest performance based on portfolio val after different parameters