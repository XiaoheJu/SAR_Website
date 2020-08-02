from .util import rscript_composit


class BaseParser:

    def design_parse(self, data):

        raise NotImplemented()

    def data_view_parse(self, data):
        raise NotImplemented()

    def analyze_parse(self, data):
        raise NotImplemented()


class CCDParser(BaseParser):

    def __init__(self):
        self.library = 'library(rsm);'
        self.design = 'rsm.design<-ccd({});'
        self.data_view = '{}{};'
        self.analyze = '{}{};'

    def design_parse(self, data):
        params = rscript_composit(data['design'])
        design = self.design.format(params)
        return '{}{}'.format(self.library, design)

    def data_view_parse(self, data):
        _design = self.design_parse(data)
        _data = data['data_view']
        _data_view = rscript_composit(_data)
        views = []
        for i in _data['views'].items():
            views.append(i)
        return self.data_view.format(_design, _data_view), views

    def analyze_parse(self, data):
        _design = self.design_parse(data)
        _data = data['analyze']
        _data_view = rscript_composit(_data)
        return self.analyze.format(_design, _data_view)







"""
ccd.design <- ccd.design(3, n0=3,alpha="rotatable", coding=list(x1~(B-30)))

ccd (3, n0 = c(4,6), alpha = "rotatable", inscribed = TRUE, coding = list (x1 ~ (Temp - 150)/10, x2 ~ (Pres - 50)/5, x3 ~ Feedrate - 4))


ccd(y~x1+x2+x3, n0=1,alpha=1.68,randomize=FALSE)


ccd_design <- ccd (3, n0 = 1, alpha = 1.68, inscribed = TRUE, coding = list (x1 ~ (Temp - 150)/10, x2 ~ (Pres - 50)/5, x3 ~ Feedrate - 4), oneblock=TRUE, randomize=FALSE)

y <- c(334, 335, 333, 332, 336, 337, 334, 335, 332, 336, 335, 334, 332, 335, 336, 335)

ccd_design$y <- y;ccd_design




"""
