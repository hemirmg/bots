# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame

# --- Custom libs here ---
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

# Class should have same name as file
class SmaRSI(IStrategy):
    #timeframe = "1h"
    timeframe = "1d"
    # Both stoploss and roi are set to 100 to prevent them to give a sell signal.
    stoploss = -0.254
    #stoploss = -0.150
    #stoploss = -0.3
    minimal_roi = {"0": 100}

# --- Plotting ---

    # Use this section if you want to plot the indicators on a chart after backtesting
    plot_config = {
        'main_plot': {
            # Create sma line
            'sma': {'color': 'blue'},
        },
        'subplots': {
            # Create rsi subplot
            "rsi": {
                'rsi': {'color': 'orange'},
                'rsi_hline': {'color': 'grey','plotly': {'opacity': 0.4}}
            },
        },
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["sma"] = ta.SMA(dataframe, timeperiod=21)
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)
        dataframe["rsi_hline"] = 50
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
           (
               # Buy when close price > sma and rsi > rsi_hline (no crossover signal, just above...)
               (dataframe['close'] > dataframe['sma'])
               & (dataframe['rsi'] > dataframe['rsi_hline'])
           ),
           'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
           (
               # Sell when close price < sma and rsi < rsi_hline (no crossover signal, just below...)
               (dataframe['close'] < dataframe['sma'])
               & (dataframe['rsi'] < dataframe['rsi_hline'])
           ),
           'sell'] = 1
        
        return dataframe