from collections import OrderedDict
from sar.sar import controller, ccd_analyze_in_deal, ccd_analyze_out_deal

expres = OrderedDict()
expres['rsm.design'] = 'decode.data(rsm.design)'
expres['y'] = 'c(334,335, 333, 332, 336, 337, 334, 335, 332, 336, 335, 334, 332, 335, 336, 335)'
expres['rsm.design$y'] = 'y'
expres['SO.model'] = "rsm(y ~ SO(Temp, Pres, Feedrate), data = rsm.design)"
expres['rsm.analyze'] = "summary(glm(SO.model))"

ccd_analyze = {
    "type": "analyze",
    "name": "ccd",
    "data": {
        "design": {
            'params': {
                "basis": 3,
                "n0": 1,
                "alpha": 1.68,
                "randomize": "FALSE",
                "coding": "list (x1 ~ (Temp - 150)/10, x2 ~ (Pres - 50)/5, x3 ~ Feedrate - 4)",
            }
        },
        "analyze": {
            'exprs': expres
        }
    },
}

print(controller.get_output(ccd_analyze, ccd_analyze_in_deal, ccd_analyze_out_deal))