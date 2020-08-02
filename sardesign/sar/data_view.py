import importlib

from .util import SarError
from .parsers import BaseParser
from .rserve import BaseRserve


class BaseSarDataView:
    """
    SarDesign
    """

    def __init__(self, parser=None, rserve=None, view=None):
        if isinstance(parser, BaseDataViewParser) and isinstance(rserve, BaseRserve):
            self.parser = parser  # DesignParser.instance(*args, **kwargs)
            self.rserve = rserve  # Rpy2()
            self.view = view

    def run(self, _input):
        raise NotImplemented("no implement design method")


class BaseDataViewParser:
    def parse(self, _input):
        raise NotImplemented()


class SarDataView(BaseSarDataView):
    """
        Singleton
        design = SarDataView.instance(*args, **kwargs)
    """

    data_view = None

    def __init__(self, *args, **kwargs):
        super(SarDataView, self).__init__(*args, **kwargs)

    @classmethod
    def instance(cls, *args, **kwargs):
        if SarDataView.data_view is None:
            SarDataView.data_view = SarDataView(*args, **kwargs)
        return SarDataView.data_view

    def set_parser(self, parser):
        if isinstance(parser, BaseDataViewParser):
            self.parser = parser

    def set_serve(self, rserve):
        if isinstance(rserve, BaseRserve):
            self.rserve = rserve

    def run(self, _input):
        """

        :param _input:
        :return:
        """
        rscript, views = self.parser.parse(_input)
        return self.rserve.get_view(rscript, views)

        # input and output parser


class DataViewParser(BaseDataViewParser):

    def __init__(self):
        self.data_view_parser = importlib.import_module('parser')

    def parse(self, _input):
        parser = self.get_parser(_input['name'])  # CCDParser etc..
        return parser.data_view_parse(_input['data'])

    def get_parser(self, name):
        _parser = getattr(self.data_view_parser, "{}Parser".format(name.upper()))()

        if isinstance(_parser, BaseParser):
            return _parser


class BaseView:
    pass
