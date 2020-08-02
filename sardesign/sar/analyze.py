import importlib

from .util import SarError
from .parsers import BaseParser
from .rserve import BaseRserve


# SarError = importlib.import_module('controller')
# print(getattr(SarError, 'SarError')('tr').error)

class BaseSarAnalyze:
    """
    SarDesign
    """

    def __init__(self, parser=None, rserve=None):
        if isinstance(parser, BaseAnalyzeParser) and isinstance(rserve, BaseRserve):
            self.parser = parser  # DesignParser.instance(*args, **kwargs)
            self.rserve = rserve  # Rpy2()

    def run(self, _input):
        raise NotImplemented("no implement design method")


class BaseAnalyzeParser:
    def parse(self, _input):
        raise NotImplemented()


class SarAnalyze(BaseSarAnalyze):
    """
        Singleton
        design = Sardesign.instance(*args, **kwargs)
    """

    analyze = None

    def __init__(self, *args, **kwargs):
        super(SarAnalyze, self).__init__(*args, **kwargs)

    @classmethod
    def instance(cls, *args, **kwargs):
        if SarAnalyze.analyze is None:
            SarAnalyze.analyze = SarAnalyze(*args, **kwargs)
        return SarAnalyze.analyze

    def set_parser(self, parser):
        if isinstance(parser, BaseAnalyzeParser):
            self.parser = parser

    def set_serve(self, rserve):
        if isinstance(rserve, BaseRserve):
            self.rserve = rserve

    def run(self, _input):
        """

        :param _input:
        :return:
        """
        rscript = self.parser.parse(_input)
        return self.rserve.get_analyze(rscript)

        # input and output parser


class AnalyzeParser(BaseAnalyzeParser):

    def __init__(self):
        self.design_parser = importlib.import_module('sardesign.sar.parsers')

    def parse(self, _input):
        parser = self.get_parser(_input['name'])  # CCDParser etc..
        return parser.analyze_parse(_input['data'])

    def get_parser(self, name):
        _parser = getattr(self.design_parser, "{}Parser".format(name.upper()))()

        if isinstance(_parser, BaseParser):
            return _parser