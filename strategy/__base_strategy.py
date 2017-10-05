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

        #
        # def is_it_ok(subject_code, current_price):
        #     try:
        #         if subject.info[subject_code]['?��?��'] == ?��?��:
        #             return para.is_it_ok(subject_code, current_price)
        #         else:
        #             err_log.error('%s 종목, ?��?�� ?��?�� ?��?��' % subject_code)
        #             return {'?��규주�?': False}
        #
        #     except Exception as err:
        #         err_log.error(log_manager.get_error_msg(err))
        #
        # def is_it_sell(subject_code, current_price):
        #     try:
        #         if subject.info[subject_code]['?��?��'] == ?��?��:
        #             return para.is_it_sell(subject_code, current_price)
        #         else:
        #             err_log.error('%s 종목, ?��?�� ?��?�� ?��?��' % subject_code)
        #             return {'?��규주�?': False}
        #
        #     except Exception as err:
        #         err_log.error(log_manager.get_error_msg(err))

        # def set_strategy_var(stv):
        #     try:
        #         # ?��?�� �??�� Config 불러?���?
        #         config = configparser.RawConfigParser()
        #         config.read(CONFIG_PATH + '/strategy_var.cfg')
        #
        #         for subject_code in subject.info.keys():
        #             subject_symbol = subject_code[:2]
        #
        #             if subject_symbol not in stv.info:
        #                 stv.info[subject_symbol] = {}
        #
        #             strategy = config.get(ST_CONFIG, subject_symbol)
        #             stv.info[subject_symbol][strategy] = {}
        #
        #             stv.info[subject_symbol][strategy][차트] = []
        #             stv.info[subject_symbol][strategy][차트�??��] = {}
        #             stv.info[subject_symbol][strategy][차트�??��][?��차트] = {}
        #             stv.info[subject_symbol][strategy][차트�??��][분차?��] = {}
        #
        #             if strategy == ?��?��:
        #                 stv.info[subject_symbol][strategy][차트�??��][매매불�??��?��?��] = config.get(subject_symbol, 매매불�??��?��?��)
        #                 stv.info[subject_symbol][strategy][차트�??��][�??��?��계별?��리블?��] = json.loads(config.get(subject_symbol, �??��?��계별?��리블?��))
        #
        #             ## subject_symbol?�� config 불러?��
        #             chart_types = json.loads(config.get(subject_symbol, CHART_TYPE))
        #
        #             for chart_type in chart_types:
        #                 type = chart_type.split('_')[0]
        #                 time_unit = chart_type.split('_')[1]
        #
        #                 section_str = subject_symbol + '_' + chart_type
        #                 stv.info[subject_symbol][strategy][차트�??��][type][time_unit] = {}
        #                 stv.info[subject_symbol][strategy][차트].append( [ str(type), str(time_unit) ] )
        #                 if strategy == ?��?��:
        #                     stv.info[subject_symbol][strategy][차트�??��][type][time_unit][?��?��?��균선] = json.loads(config.get(section_str, ?��?��?��균선))
        #                     stv.info[subject_symbol][strategy][차트�??��][type][time_unit][INIT_AF] = config.getfloat(section_str, INIT_AF)
        #                     stv.info[subject_symbol][strategy][차트�??��][type][time_unit][MAX_AF] = config.getfloat(section_str, MAX_AF)
        #                     stv.info[subject_symbol][strategy][차트�??��][type][time_unit][초기캔들?��] = config.getint(section_str, 초기캔들?��)
        #
        #
        #     except Exception as err:
        #         err_log.error(log_manager.get_error_msg(err))

        # def check_contract_in_candle(subject_code, candle, index):
        #     try:
        #         if subject.info[subject_code]['?��?��'] == ?��?��:
        #             pass
        #         else:
        #             err_log.error('%s 종목, ?��?�� ?��?�� ?��?��' % subject_code)
        #             return {'?��규주�?': False}
        #
        #     except Exception as err:
        #         err_log.error(log_manager.get_error_msg(err))
        #
        # def check_contract_in_tick(subject_code, current_price):
        #     pass

    def init_logger(self):
        self.log, self.res, self.err_log = log_manager().LogManager.__call__().get_logger()