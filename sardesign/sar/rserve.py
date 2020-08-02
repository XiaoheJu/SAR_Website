import os
import time

from rpy2 import robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
import numpy as np
import pandas as pd

from .util import hash_sha1



class BaseRserve:

    def get_object(self, rscript):
        raise NotImplemented('not implement get_object method')

    def get_table(self, rscript):
        raise NotImplemented('not implement get_table method')

    def get_analyze(self, rscript):
        raise NotImplemented('not implement get_analyze method')

    def get_view(self, rscript, views, suffix=None):
        raise NotImplemented('not implement get_view method')


class PyRserve(BaseRserve):
    pass


class Rpy2(BaseRserve):

    def __init__(self):
        self.dir_path = os.path.dirname(os.path.abspath(__file__))

    def get_object(self, rscript):
        robject = robjects
        robject.r(rscript)
        return robject


    def get_table(self, rscript):
        r_object = self.get_object(rscript)

        return self._get_table(r_object.r('decode.data(rsm.design)'))

    def _get_table(self, r_object):
        df = pandas2ri.ri2py(r_object)
        df['y'] = np.nan
        return df.drop(columns=['run.order','std.order', 'Block']).to_json() # 'run.order',

    def get_analyze(self, rscript):
        r_object = self.get_object(rscript)
        return self._get_analyze(r_object.globalenv['rsm.analyze'])

    def _get_analyze(self, r_object):
        lof = r_object.rx('coefficients')
        matrix = list(lof)[0]
        df = pd.DataFrame(data=pandas2ri.ri2py(matrix), index=list(list((matrix.names))[0]),
                          columns=list(list((matrix.names))[1]))
        return df.to_json()

    def get_view(self, rscript, views, suffix=None):
        grdevices = importr('grDevices')
        robject = self.get_object(rscript)
        _views = {}
        for key, view in views:
            _views[key] = (self._get_view(robject,view, grdevices, suffix=suffix))
        return _views

    def _get_view(self, robject, view, grdevices, suffix=None):
        filename = os.path.join(self.dir_path,
                                "../assets/images/{}.png").format(hash_sha1(str(time.time())))
        if suffix is not None:
            pass
        else:
            grdevices.png(file=filename, width=512, height=512)
        robject.r(view)
        return os.path.abspath(filename)

    # def get_view(self, rscript, suffix=None):
    #     filename = os.path.join(self.dir_path,
    #                             "../assets/images/{}.png").format(hash_sha1(str(time.time())))
    #     grdevices = importr('grDevices')
    #     if suffix is not None:
    #         pass
    #     else:
    #         grdevices.png(file=filename, width=512, height=512)
    #     self.get_object(rscript)
    #     return os.path.abspath(filename)



# rscript = "library(rsm);ccd_design <- ccd (3, n0 = 1, alpha = 1.68, inscribed = TRUE, " \
#           "coding = list (x1 ~ (Temp - " \
#           "150)/10, x2 ~ (Pres - 50)/5, x3 ~ Feedrate - 4), oneblock=TRUE, randomize=FALSE);" \
#           "y <- c(334, 335, 333, 332, 336, 337, 334, 335, 332, 336, 335, 334, 332, 335, 336, 335);" \
#           "ccd_design$y <- y;SO.model <- rsm(y ~ SO(x1, x2, x3), data = ccd_design);summary(glm(SO.model));" \
#           "persp(SO.model, x1~x2, at=xs(SO.model));"

