from sar.controller import CentralController
from sar.input import DjangoInput, CCDInputDesignDeal
from sar.design import SarDesign, DesignParser
from sar.rserve import Rpy2
from sar.output import DjangoOutput, CCDOutDesignDeal, CCDOutDataViewDeal
from sar.data_view import SarDataView, DataViewParser

#
# in1 = CentralController.instance(1, 2, 3, 4)
# in2 = CentralController.instance(11, 2, 3, 4)
#
# in1.set_controller()
# in2.set_controller()
# print(id(in1))
#
# print(id(in2))



# rscript = "library(rsm);ccd.design <- ccd (3, n0 = 1, alpha = 1.68, inscribed = TRUE, " \
#           "coding = list (x1 ~ (Temp - " \
#           "150)/10, x2 ~ (Pres - 50)/5, x3 ~ Feedrate - 4), oneblock=TRUE, randomize=FALSE);" \
#           "y <- c(334, 335, 333, 332, 336, 337, 334, 335, 332, 336, 335, 334, 332, 335, 336, 335);" \
#           "ccd_design$y <- y;SO.model <- rsm(y ~ SO(x1, x2, x3), data = ccd_design);summary(glm(SO.model));" \
#           "persp(SO.model, x1~x2, at=xs(SO.model));"

x = {
    "type": "data_view",
    "name": "ccd",
    "data": {
        "basis": 3,
        "n0": 1,
        "alpha": 1.68,
        "randomize": "FALSE",
        "coding": "list (x1 ~ (Temp - 150)/10, x2 ~ (Pres - 50)/5, x3 ~ Feedrate - 4)",
    }

}

in_deal = CCDInputDesignDeal()
in_put = DjangoInput()
rserve = Rpy2()

out_deal = CCDOutDataViewDeal()
out_put = DjangoOutput()
design_parser = DesignParser()
design = SarDesign.instance(parser=design_parser, rserve=rserve)

data_view_parser = DataViewParser()
data_view = SarDataView.instance(parser=data_view_parser, rserve=rserve)
controller = CentralController.instance(base_design=design, base_data_view=data_view,
                                        )

controller.set_input_output(base_input=in_put, base_output=out_put)

print(controller.get_output(x, in_deal, out_deal))
