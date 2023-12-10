from enum import Enum
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()


class MarketDataType(Enum):
    IQFEED_TICK = 'IQFEED TICK'
    IQFEED_SECOND = 'IQFEED SECOND'  # Sampled at 1 Second resolution
    IQFEED_MINUTE = 'IQFEED MINUTE'
    IQFEED_MINUTE_FEATHER = 'IQFEED MINUTE FEATHER'     # TODO: I need to clean this once fully implemented

    IB_SECOND = 'IB SECOND'  # Sampled at 30 second resolution


class ChartType(Enum):
    RANGE_BAR = 'RANGE BAR'
    VOLUME_BAR = 'VOLUME BAR'
    TICK_BAR = 'TICK BAR'
    TIME_BAR = 'TIME BAR'


def _get_market_data_source_dir(source: MarketDataType):
    ohlc_cols = ['datetime', 'open_p', 'high_p', 'low_p', 'close_p', 'prd_vlm']
    tick_cols = ['datetime', 'bid', 'ask', 'last', 'last_sz']

    path_root_market_data_dir = Path(os.getenv('MARKET_DATA_LOCALHOST_DIR'))

    match source:
        case MarketDataType.IQFEED_TICK:
            return path_root_market_data_dir / 'iqfeed_tick', tick_cols
        case MarketDataType.IQFEED_SECOND:
            return path_root_market_data_dir / 'iqfeed_second', ohlc_cols
        case MarketDataType.IQFEED_MINUTE:
            return path_root_market_data_dir / 'iqfeed_minute', ohlc_cols
        case MarketDataType.IQFEED_MINUTE_FEATHER:
            return path_root_market_data_dir / 'iqfeed_minute_feather', ohlc_cols
        case MarketDataType.IB_SECOND:
            return path_root_market_data_dir / 'tws_second', ohlc_cols
