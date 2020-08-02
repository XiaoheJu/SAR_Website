from .util import SarError
from .design import BaseSarDesign
from .input import BaseInput
from .output import BaseOutput
"""

data structure

{"type": "design",
 "design": "ccd",
 "ccd"

}
"""


class BaseSarController:

    def __init__(self, base_design=None, base_data_view=None, base_analyze=None,
                 base_data_access=None):
        if isinstance(base_design, BaseSarDesign):
            self.design = base_design
            self.data_view = base_data_view
            self.analyze = base_analyze
            self.data_access = base_data_access


    @classmethod
    def instance(cls, *args, **kwargs):
        raise ImportError("not implement instance")


class CentralController(BaseSarController):
    """

    Singleton
    controller = CentralController.instance(*args, **kwargs)

    """

    controller = None

    def __init__(self, *args, **kwargs):
        super(CentralController, self).__init__(*args, **kwargs)

    @classmethod
    def instance(cls, *args, **kwargs):
        if CentralController.controller is None:
            CentralController.controller = CentralController(*args, **kwargs)
        return CentralController.controller

    def set_controller(self):
        """
        set base_design ...
        :return:
        """
        pass

    def set_input_output(self, base_input, base_output):
        if isinstance(base_input, BaseInput) and isinstance(base_output, BaseOutput):
            self.base_input = base_input
            self.base_output = base_output


    def get_output(self, in_put, in_deal, out_deal):
        _input = self.base_input.get_input(in_deal, in_put)  # BaseInput
        # BaseSarDesign, base_data_view, base_analyze, base_data_access

        out_put = self.deal(_input['type'], _input)
        return self.base_output.get_out(out_deal, out_put)  #

    def deal(self, _type, _input):
        """

        :param _type: str -> 'design', 'data_view', 'analyze', 'data_access'
        :param _input: dict
        :return:
        """
        return getattr(self, _type).run(_input)
        # if _type == 'design':
        #     return self.base_design.design(_input)
        # elif _type == 'data_view':
        #     return self.base_data_view.view(_input)
        # elif _type == 'analyze':
        #     return self.base_analyze.analyze(_input)
        # elif _type == 'data_access':
        #     return self.base_data_access.access(_input)
        # else:
        #     return ControlDealError('CentralController deal type error')




class ControlDealError(SarError):
    pass
