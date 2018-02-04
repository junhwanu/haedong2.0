import abc
import inspect

from manager import log_manager


class BaseStrategy(metaclass=abc.ABCMeta):
    log, res, err_log = None, None, None

    stv = None
    chart = None

    def __init__(self):
        super(BaseStrategy, self).__init__()
        self.init_logger()

    @abc.abstractmethod
    def is_it_ok(self, current_price):
        raise NotImplementedError(inspect.stack()[0][3] + ' is not impplemented.')

    @abc.abstractmethod
    def is_it_sell(self, current_price):
        raise NotImplementedError(inspect.stack()[0][3] + ' is not impplemented.')

    @abc.abstractmethod
    def set_strategy_var(self):
        raise NotImplementedError(inspect.stack()[0][3] + ' is not impplemented.')

    @abc.abstractmethod
    def check_contract_in_candle(self, current_price):
        raise NotImplementedError(inspect.stack()[0][3] + ' is not impplemented.')

    @abc.abstractmethod
    def check_contract_in_tick(self, subject_code, current_price):
        raise NotImplementedError(inspect.stack()[0][3] + ' is not impplemented.')

    def init_logger(self):
        self.log, self.res, self.err_log = log_manager.LogManager().get_logger()