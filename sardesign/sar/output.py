import json
from collections import OrderedDict

class BaseOutput:

    def get_out(self, output_deal, data):

        raise NotImplemented()


class OutDesignDeal:

    def deal(self, output):

        raise NotImplemented()


class DjangoOutput(BaseOutput):

    def get_out(self, output_deal, data):
        """

        :param output_deal: OutDesignDeal
        :param data:
        :return:
        """

        if isinstance(output_deal, OutDesignDeal):
            return output_deal.deal(data)


class DjangoOutDesignDeal(OutDesignDeal):

    def deal(self, output):
        """
        convert output to django format
        :param output: standard dict like in _deal()
        :return: data to Django
        """


class CCDOutDesignDeal(DjangoOutDesignDeal):

    def deal(self, output):

        _result = self._deal(output)
        return _result['data']

    def _deal(self, output):
        """

        :param output:
        :return: standard dict in sardesign
        """
        _output = {
            "type": "design",
            "name": "ccd",
            "data": json.JSONDecoder(object_pairs_hook=OrderedDict)
                .decode(output)
        }
        return _output
class CCDOutDataViewDeal(DjangoOutDesignDeal):

    def deal(self, output):

        _result = self._deal(output)
        return _result['data']

    def _deal(self, output):
        """

        :param output:
        :return: standard dict in sardesign
        """
        _output = {
            "type": "data_view",
            "name": "ccd",
            "data": {
                'filepath': output
            }
        }
        return _output

class CCDOutAnalyzeDeal(DjangoOutDesignDeal):

    def deal(self, output):

        _result = self._deal(output)
        return _result['data']

    def _deal(self, output):
        """

        :param output:
        :return: standard dict in sardesign
        """
        _output = {
            "type": "analyze",
            "name": "ccd",
            "data": {
                'analyze': json.JSONDecoder(object_pairs_hook=OrderedDict)
                .decode(output)
            }
        }
        return _output