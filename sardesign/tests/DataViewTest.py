from sar.sar import controller, ccd_data_view_in_deal, ccd_data_view_out_deal
from collections import OrderedDict

# expression is odered, params is not.
expres = OrderedDict()
expres['y'] = 'c(334,335, 333, 332, 336, 337, 334, 335, 332, 336, 335, 334, 332, 335, 336, 335)'
expres['rsm.design$y'] = 'y'
expres['SO.model'] = "rsm(y ~ SO(x1, x2, x3), data = rsm.design)"

ccd_data_view = {
    "type": "data_view",
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
        "data_view": {
            'exprs': expres,
            'views': {
                'view1': 'persp(SO.model, x1 ~ x2, at=xs(SO.model));',
                'view2': 'persp(SO.model, x1 ~ x3, at=xs(SO.model));',

            }
        }
    }
}

print(controller.get_output(ccd_data_view, ccd_data_view_in_deal,
                            ccd_data_view_out_deal))