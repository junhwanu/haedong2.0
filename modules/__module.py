import abc
import inspect
from log_manager import LogManager
from telepot_manager import TelepotManager


class ModuleClass(metaclass=abc.ABCMeta):
    log, res, err_log = None, None, None
    telepot = None

    def __init__(self):
        super(ModuleClass, self).__init__()
        self.init_logger()
        self.init_telepot()

    @abc.abstractmethod
    def get_name(self):
        raise NotImplementedError(inspect.stack()[0][3] + ' is not impplemented.')

    @abc.abstractmethod
    def print_status(self):
        raise NotImplementedError(inspect.stack()[0][3] + ' is not impplemented.')

    def init_logger(self):
        self.log, self.res, self.err_log = LogManager.__call__().get_logger()

    def init_telepot(self):
        self.telepot = TelepotManager.__call__()