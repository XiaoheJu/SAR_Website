from django.test import TestCase
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from rpy2.robjects import numpy2ri
from rpy2.robjects import pandas2ri
import pprint
import numpy as np
import pandas as pd

import pyRserve

# grdevices = importr('grDevices')
# grdevices.png(file="Rpy2Curve.png", width=512, height=512)
# # # persp(SO.model, x1~x2, at=xs(SO.model));
# # # Create your tests here.
# # rscript = "library(rsm);ccd(y~x1+x2+x3, n0=1,alpha=1.68,randomize=FALSE);"
rscript = "library('rsm');library('jsonlite');ccd_design <- ccd (3, n0 = 1, alpha = 1.68, inscribed = TRUE, coding = list (x1 ~ (Temp - 150)/10, x2 ~ (Pres - 50)/5, x3 ~ Feedrate - 4), oneblock=TRUE, randomize=FALSE);y <- c(334, " \
          "335, 333, 332, 336, 337, 334, 335, 332, 336, 335, 334, 332, 335, 336, 335);ccd_design" \
          # "ccd_design$y <- " \
          # "y;ccd_design;SO.model <- rsm(y ~ SO(x1, x2, x3), data = ccd_design);summary(glm(SO.model)) "x <- toJSON(ccd_design);cat(x)

pymodels = robjects.r(rscript)
base = importr('base')
# base.sink('tl.txt')
#
# robjects.r('print(summary(ccd_design))')

print(pandas2ri.ri2py(robjects.r('decode.data(ccd_design);')).to_json())
print(pandas2ri.ri2py(robjects.globalenv['ccd_design']))
# print(type(robjects.globalenv['ccd_design']))
# xx = robjects.globalenv['ccd_design'].cbind(robjects.globalenv['y'])# error
# print(xx)


# print(robjects.r('ccd_design$y <- y;ccd_design'))  --->>>> ok

# print(robjects.r.cbind(x, y=robjects.globalenv['y']))
# print(robjects.globalenv['ccd_design'])
# ccd_design = robjects.globalenv['y']
# robjects.globalenv['ccd_design']


# 最初 pymodels.names 获得有的 listvector name
# print(pymodels)
# df = pandas2ri.ri2py(pymodels)
#
# df[-1].replace(-2147483648, np.nan, inplace=True)
# df.drop(columns=['run.order', 'std.order'])
# print(df.drop(columns=['run.order', 'std.order']).to_json())
# # for x in pymodels.names:
#     di[x] = pymodels.rx(x)
#
# print(di)


# x = pymodels.rx('coefficients') # coefficients listvector
#
# matrix = list(x)[0] # coefficients Matrix
#
# print(matrix)
#
# df = pd.DataFrame(data=pandas2ri.ri2py(matrix), index=list(list((matrix.names))[0]),
#                    columns=list(list((matrix.names))[1]))
#
# print(df.to_json())

# di = {}
#
# for x in pymodels.names:
#     print('+++++++++++++{}+++++++'.format(x))
#     print(pymodels.rx(x))
# #
# # print(di)
# # for x in pymodels.names:
# #
#
# x = pymodels.rx('sigma') # coefficients listvector


# x = pymodels.rx('lof') # coefficients listvector
#
# matrix = list(x)[0] # coefficients Matrix
# df= pandas2ri.ri2py(matrix)
# print(type(matrix))
#
#
# # df = pd.DataFrame(data=pandas2ri.ri2py(matrix), index=list(list((matrix.names))[0]),
# #                   columns=list(list((matrix.names))[1]))
#
# print(df.to_json())





# print(type(li))
# print(list(li))
# xx = numpy2ri.ri2py(list(x)[0])
#
# print(xx)
# print(type(xx))
# print(list(matrix))
#
# data = list(matrix)
#

# arr = np.array(x)
# df = pd.DataFrame({'mean':arr.flatten()})
# print(df)


# x = {
#     "type": "design",
#     "name": "ccd",
#     "data": {
#         "basis": 3,
#         "n0": 1,
#         "alpha": 1.68,
#         "randomize": "FALSE",
#         "coding": [robjects.Formula('x1 ~ (Temp - 150)/10'), robjects.Formula('x2 ~ (Pres - 50)/5'),
#                    robjects.Formula('x3 ~ Feedrate - 4')]
#         # "coding": "list (x1 ~ (Temp - 150)/10, x2 ~ (Pres - 50)/5, x3 ~ Feedrate - 4)"
#     }
# }
#
# rsm = robjects.packages.importr('rsm')
# ccd_design = rsm.ccd(**x['data'])
#
#
# print(ccd_design)
# l = []
# for i in x['data'].items():
#     param = '{}={},'.format(i[0], i[1])
#     l.append(param)
#
# params = ''.join(l)[:-1]
# ccd = "ccd({});"
# library = 'library(rsm);'
# rscript = '{}{}'.format(library, ccd.format(params))
# print(rscript)
# pymodels = robjects.r(rscript)
# print(pymodels)
