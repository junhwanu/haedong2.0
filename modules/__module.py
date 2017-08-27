import abc
import inspect
from manager import log_manager, telepot_manager


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
        self.log, self.res, self.err_log = log_manager.LogManager.__call__().get_logger()

    def init_telepot(self):
        self.telepot = telepot_manager.TelepotManager.__call__()