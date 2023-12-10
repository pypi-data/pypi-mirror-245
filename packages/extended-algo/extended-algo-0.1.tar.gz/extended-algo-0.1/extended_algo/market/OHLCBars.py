import logging

import pandas as pd
import datetime as dt
from extended_algo.market.common import MarketDataType, _get_market_data_source_dir
from dotenv import load_dotenv

load_dotenv()


class OHLCBars:

    def __init__(self, source: MarketDataType, symbol, start: dt.datetime, end: dt.datetime, **kwargs):
        assert end - start >= dt.timedelta(milliseconds=0), 'end date must be greater than start date'
        assert source != MarketDataType.IQFEED_TICK, 'ohlc only available vi seconds, minute data'

        self._source_dir, self._default_cols = _get_market_data_source_dir(source)
        self.symbol = symbol
        self.start = start
        self.end = end
        self.kwargs = kwargs

        logging.info(f'Get {self._source_dir.parts[-2:]} | {symbol=} {start=} {end=}')

        self.data = self._load_historical_data()

    def _load_historical_data(self):
        load_file_years = list(range(self.start.year, self.end.year + 1))
        path_symbol_dir = self._source_dir / self.symbol

        df = []
        for year in load_file_years:
            _data = pd.read_feather(path_symbol_dir / f'{year}.f', columns=self.kwargs.get('columns', self._default_cols))
            df.append(_data)

        df = pd.concat(df, ignore_index=True)
        df = df.sort_values('datetime', ascending=True)
        df = df.query(f'datetime >= @self.start and datetime <= @self.end')

        return df