from wallstreet import Stock
from maldives.regression import LinearRegressor
from maldives.api import FredData
from maldives.backtest.model_utils import CalculateProbability, VisualizeProbability

import pandas as pd
import numpy as np
import plotly.express as px


class GoldPriceModel(object):
    def __init__(self, shift=30):
        self.df = None
        self.fitted = False

        self.model = None
        self.last_date = None
        self.current_price = np.nan
        self.prob = None
        self.uncertainty = None
        self.shift = shift

    def load_data(self, fred_api_key, start=pd.Timestamp.today()-pd.tseries.offsets.BDay(1500), end=pd.Timestamp.today()):
        if type(start) is int:
            start = end - pd.tseries.offsets.BDay(start)

        # load gold futures prices
        days_back_required = (pd.Timestamp.today()-start).round('D').days

        gold = Stock('GC=F').historical(days_back=days_back_required)
        gold['Date'] = pd.to_datetime(gold['Date'])
        gold['ClosingPrice'] = gold['Close']
        gold = gold.set_index('Date')[['ClosingPrice']]
        self.current_price = gold.ClosingPrice.values[-1]

        # load cpi and treasury yield
        fred = FredData(fred_api_key)
        cpi, treasury = fred.CPI(), fred.Treasury10Y()

        df = pd.merge_asof(gold.join(
            treasury), cpi, left_index=True, right_index=True, direction='nearest')
        df = df.dropna().loc[start.date():end.date()]
        self.df = df
        self.last_date = self.df.index[-1].strftime('%Y-%m-%d')

    def fit(self):
        if self.df is None:
            raise ValueError(
                'No data available. Please call load_data() before calling fit().')
        self.model = LinearRegressor(transform=np.log, invtransform=np.exp)
        X, y = self.df[['CPI', 'Treasury10Y']], self.df['ClosingPrice']
        self.model.fit(X, y, shift=-self.shift)
        
        self.df['Prediction'] = self.model.predict(X)
        CalculateProbability(self.model, np.linspace(0.8, 1.2, 1001))

    def display(self, return_figures=False):
        if not self.fitted:
            self.fit()

        # prob distribution
        title=f"R2={self.model.R2:.2f} (as of {self.last_date})"
        fig1 = VisualizeProbability(self.model, self.current_price, 'Gold Price', title, False)

        # time series of predictions
        self.df = self.df.join( self.df.Prediction.shift(self.shift, freq='B').rename('PredictedPrice') , how='outer')
        fig2 = px.line(self.df.ffill(), y=['PredictedPrice', 'ClosingPrice'])
        fig2.update_layout(xaxis_title='Time',
                           yaxis_title='Price', hovermode='x')
        if not return_figures:
            fig1.show(), fig2.show()
        else:
            return fig1, fig2
