from abc import ABC, ABCMeta, abstractmethod
import logging
import datetime as dt
import pandas as pd
import numpy as np
import inspect
from pathlib import Path
from extended_algo.market.OHLCBars import OHLCBars
from extended_algo.market.common import MarketDataType
from extended_algo import symbol_lookup
from extended_algo.report.CalculatePnLStats import CalculatePnLStats

pd.set_option('display.width', 1000, 'display.max_columns', 1000)

# TODO: I may want to create an override startegy path? Thoughts on this

class VectorStrategy(ABC):

    def __init__(self, symbol, start, end, profit_target=100, stop_loss=100,
                 closeout_ttl: (dt.timedelta | dt.time) = dt.timedelta(hours=1), market_data_cls=OHLCBars,
                 market_type=MarketDataType.IQFEED_MINUTE_FEATHER, restrict_feature_cols: (set, list) = {}, **kwargs):
        self.strategy_name = self.__class__.__name__
        self.save_dir = Path(inspect.getfile(self.__class__)).parent / 'vector'
        self.save_dir.mkdir(exist_ok=True)

        self.symbol = symbol
        self.start = start
        self.end = end

        self.lookback_days = kwargs.pop('lookback_days', 0)
        self.market_type = market_type
        self.market_data_class = market_data_cls
        self.profit_target = profit_target
        self.stop_loss = stop_loss
        self.closeout_ttl = closeout_ttl
        self.restrict_feature_cols = restrict_feature_cols
        self.kwargs = kwargs

        logging.info(f'Starting vectorized calc | {self.strategy_name} {self.symbol} from {self.start} - {self.end}')

        self.market_data = self._get_tradeable_market_data()
        self.features_data = pd.DataFrame()
        self.signal_data = self.market_data.copy()

        self.run()

    def _get_tradeable_market_data(self):
        start = self.start - pd.offsets.Day(self.lookback_days)
        market = OHLCBars(source=self.market_type, symbol=self.symbol, start=start, end=self.end, **self.kwargs)
        market = market.data
        market['is_live'] = np.where(market.datetime < self.start, 0, 1)
        market = market.set_index('datetime')
        return market

    @abstractmethod
    def signal(self) -> pd.DataFrame(columns=['signal']):
        raise NotImplementedError('''
            must return dataframe with datetime index and signal columns
        
            Provide logic for generating trading signal by leveraging df = self.signal_data
            The signal dataframe must contain the following as a minimum
            signal (-1 = NEW SHORT TRADE | 1 = NEW LONG TRADE | 0 = NO ACTION ) as the inception of the trade
            quantity is always defaulted to 1/lot sizes based on commission; in-order to implement a scalp and swing strategy two strategies need to be implemented 
            with varying profit target and stop loss reflecting the trades 
            ''')

    def _generate_mfe_mae_stats(self, x):
        try:
            m = self.market_data[x.name:][['high_p', 'low_p', 'close_p']]

            m = m.loc[m.index <= x.forced_closeout]

            m['1_sl_exit'] = np.where(((x.signal == -1) & (m.high_p >= x.sl)) |
                                      ((x.signal == 1) & (m.low_p <= x.sl)), x.sl, np.nan)
            m['2_cl_exit'] = np.where(m.index.time == m.index.time.max(), m.close_p, np.nan)
            m['3_pt_exit'] = np.where(((x.signal == -1) & (m.low_p <= x.pt)) |
                                      ((x.signal == 1) & (m.high_p >= x.pt)), x.pt, np.nan)

            m.drop_duplicates(['3_pt_exit', '1_sl_exit', '2_cl_exit'], inplace=True)
            m.dropna(thresh=4, inplace=True)

            exit = m.iloc[0][['3_pt_exit', '1_sl_exit', '2_cl_exit']].sort_index().dropna().reset_index()
            exit['index'] = exit['index'].map(
                {'1_sl_exit': 'stop_loss', '2_cl_exit': 'close_out', '3_pt_exit': 'profit_target'})

            exit_type = exit.iloc[0][0]
            exit_price = exit.iloc[0][1]
            exit_time = exit.columns[1]

            return [exit_price, exit_time, exit_type]

        except (IndexError, ValueError):
            logging.info(f'   - Could not compute exit stats for the following timestamp {x.name}')
            return [np.nan, np.nan, np.nan]

    def _apply_stoploss_and_profit_targets(self):
        df = self.signal_data
        assert 'signal' in df.columns, 'signal column missing, please set [-1=SHORT, 1=LONG] for abstart method signal() '

        try:
            df.set_index('datetime', inplace=True)
        except:
            pass
        df = df[df.is_live == 1]
        df = df[df.signal != 0]
        df = df[~df.signal.isnull()]

        df['pt'] = np.where(df.signal == -1, df.close_p - self.profit_target, np.nan)
        df['pt'] = np.where(df.signal == 1, df.close_p + self.profit_target, df.pt)
        df['sl'] = np.where(df.signal == -1, df.close_p + self.stop_loss, np.nan)
        df['sl'] = np.where(df.signal == 1, df.close_p - self.stop_loss, df.sl)

        if isinstance(self.closeout_ttl, dt.timedelta):
            df['forced_closeout'] = df.index + self.closeout_ttl
        elif isinstance(self.closeout_ttl, dt.time):
            df['forced_closeout'] = df.index.to_series().apply(lambda x: dt.datetime.combine(x, self.closeout_ttl))

        df['exit'] = df.apply(self._generate_mfe_mae_stats, axis=1)

        # TODO: this might need to be improved
        df[['exit_price', 'exit_time', 'exit_type']] = pd.DataFrame(df.exit.tolist(), index=df.index)
        df = df.drop('exit', axis=1, errors='ignore')

        return df

    def _calc_trades(self):
        df = self.signal_data
        assert (sym_detail := symbol_lookup.get(self.symbol)), f'symbol_lookup and tick multiplier missing for {self.symbol}'
        df['symbol'] = self.symbol
        df['quantity'] = self.kwargs.get('quantity', 1)
        df['tick_multiplier'] = sym_detail.multiplier
        df['commission'] = df.quantity * sym_detail.commission

        rename_cols = ['datetime', 'price', 'action', 'symbol', 'quantity', 'commission']
        df['entry_time'] = df.index
        entry_trades = df[['entry_time', 'close_p', 'signal', 'symbol', 'quantity', 'commission']]
        exit_trades = df[['exit_time', 'exit_price', 'signal', 'symbol', 'quantity', 'commission']]

        entry_trades.columns = rename_cols
        exit_trades.columns = rename_cols
        exit_trades.action = exit_trades.action * -1

        df = pd.concat([entry_trades, exit_trades], ignore_index=True)
        df = df.sort_values('datetime', ascending=True, ignore_index=True)
        df.action = df.action.map({-1: 'SELL', 1: 'BUY'})

        return df

    def _calc_stats(self):
        s = CalculatePnLStats(trade_data=self.trade_data, features_data=self.features_data, stats_chunk=100_000,
                              restrict_feature_cols=self.restrict_feature_cols)
        pnl = s.pnl_data
        stats = s.stats_data

        return pnl, stats

    def run(self):
        s = dt.datetime.now()
        self.signal_data = self.signal()
        self.signal_data = self._apply_stoploss_and_profit_targets()
        self.trade_data = self._calc_trades()
        self.pnl_data, self.stats_data = self._calc_stats()

        for f in ['market_data', 'features_data', 'signal_data', 'trade_data', 'pnl_data', 'stats_data']:
            df = getattr(self, f)
            df.to_pickle(self.save_dir / f'{f}.p')

        e = dt.datetime.now()
        logging.info(f'Elapsed time: {e - s}')
