import importlib

from .util import SarError
from .parsers import BaseParser
from .rserve import BaseRserve

import os


# SarError = importlib.import_module('controller')
# print(getattr(SarError, 'SarError')('tr').error)

class BaseSarDesign:
    """
    SarDesign
    """

    def __init__(self, parser=None, rserve=None):
        if isinstance(parser, BaseDesignParser) and isinstance(rserve, BaseRserve):
            self.parser = parser  # DesignParser.instance(*args, **kwargs)
            self.rserve = rserve  # Rpy2()


    def run(self, _input):
        raise NotImplemented("no implement design method")


class BaseDesignParser:
    def parse(self, _input):
        raise NotImplemented()


class SarDesign(BaseSarDesign):
    """
        Singleton
        design = Sardesign.instance(*args, **kwargs)
    """

    design = None

    def __init__(self, *args, **kwargs):
        super(SarDesign, self).__init__(*args, **kwargs)

    @classmethod
    def instance(cls, *args, **kwargs):
        if SarDesign.design is None:
            SarDesign.design = SarDesign(*args, **kwargs)
        return SarDesign.design

    def set_parser(self, parser):
        if isinstance(parser, BaseDesignParser):
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
        return self.rserve.get_table(rscript)

        # input and output parser


class DesignParser(BaseDesignParser):

    def __init__(self):
        self.design_parser = importlib.import_module('sardesign.sar.parsers')

    def parse(self, _input):
        parser = self.get_parser(_input['name'])  # CCDParser etc..
        return parser.design_parse(_input['data'])

    def get_parser(self, name):
        _parser = getattr(self.design_parser, "{}Parser".format(name.upper()))()

        if isinstance(_parser, BaseParser):
            return _parser

