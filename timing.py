from utils import time_utc
import datetime as dt

class Timing():
    def __init__(self, last_candle_time):
        self.last_complete_candle=last_candle_time
        if last_candle_time is None:
            self.last_candle = time_utc() - dt.timedelta(minutes=10)
        self.ready = False

    def __repr__(self):
        return str(vars(self))
