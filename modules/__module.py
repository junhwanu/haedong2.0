import abc
import inspect
import log_manager as Log

class ModuleClass:
    __metaclass__ = abc.ABCMeta

    log, res, err_log = None, None, None

    def __init__(self):
        super(ModuleClass, self).__init__()
        self.init_logger()

    @abc.abstractmethod
    def get_name(self):
        raise NotImplementedError(inspect.stack()[0][3] + ' is not impplemented.')

    @abc.abstractmethod
    def print_status(self):
        raise NotImplementedError(inspect.stack()[0][3] + ' is not impplemented.')

    def init_logger(self):
        self.log, self.res, self.err_log = Log.LogManager.__call__().get_logger()
