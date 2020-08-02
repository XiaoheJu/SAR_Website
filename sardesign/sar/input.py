import json
from collections import OrderedDict

expres = OrderedDict()
expres['rsm.design'] = 'decode.data(rsm.design)'
expres['y'] = 'c(334,335, 333, 332, 336, 337, 334, 335, 332, 336, 335, 334, 332, 335, 336, 335)'
expres['rsm.design$y'] = 'y'
expres['SO.model'] = "rsm(y ~ SO(Temp, Pres, Feedrate), data = rsm.design)"
expres['rsm.analyze'] = "summary(glm(SO.model))"

class BaseInput:

    def get_input(self, input_deal, data):

        raise NotImplemented()


class InputDesignDeal:

    def deal(self, data):
        raise NotImplemented()


class DjangoInput(BaseInput):

    def get_input(self, input_deal, data):
        """

        :param input_deal: InputDesignDeal
        :param data:
        :return:
        """
        if isinstance(input_deal, InputDesignDeal):
            return input_deal.deal(data)


class DjangoInputDesignDeal(InputDesignDeal):
    pass


class CCDInputDesignDeal(DjangoInputDesignDeal):

    def __init__(self):
        self.design = {
            "type": "design",
            "name": "ccd",
            "data": {
                "design": {
                    "params": {
                        "basis": 3,
                        "n0": 1,
                        "alpha": 1.68,
                        "randomize": "FALSE",
                        "coding": "list (x1 ~ (Temp - 150)/10, x2 ~ (Pres - 50)/5, x3 ~ Feedrate - 4)",
                    }

                }
            }
        }

    def deal(self, data):
        # return format
        # {
        #     "type": "design",
        #     "name": "ccd",
        #     "data": {
        #         "basis": 3, # int
        #         "n0": 1, # int
        #         "alpha": 1.68, # int
        #         "randomize": "FALSE",
        #         "coding": "list (x1 ~ (Temp - 150)/10, x2 ~ (Pres - 50)/5, x3 ~ Feedrate - 4)"
        #         ...
        #     }
        # }
        datas = json.loads(data['data'])
        script = {}
        script["basis"] = len(datas)
        code = []
        for i, j in enumerate(datas):
            code.append('x{} ~ ({} - {})/{},'.format(str(i+1), j['code'], j['numc'], j['numa']))
        script['coding'] = 'list ({})'.format(''.join(code)[:-1])
        self.design['data']["design"]["params"].update(script)
        self.design['cookies'] = data['cookies']
        return self.design

class CCDInputDataViewDeal(DjangoInputDesignDeal):

    def deal(self, data):

        return data

class CCDInputAnalyzeDeal(DjangoInputDesignDeal):

    def __init__(self):
        self.analyze = {
            "type": "analyze",
            "name": "ccd",
            "data": {
                "design": {
                    "params": {
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
            }
        }

    def deal(self, data):
        datas = json.loads(data['data'])
        script = {}
        y = []
        for _data in datas:
            if _data == '':
                raise Exception
            y.append('{},'.format(_data))
        script['y'] = 'c({})'.format(''.join(y)[:-1])
        x = self.analyze["data"]["analyze"]['exprs']
        x.update(script)
        self.analyze['data']['data_access'] = data['cookies']
        return self.analyze


# import queue
#
# class BaseTaskQueue:
#
#     def get_task(self):
#         """
#         get task from queue
#         :return: type dict
#         """
#         raise ImportError('not implement get_task')
#
#     def is_empty(self):
#         """
#         queue is empty ?
#         :return:
#         """
#         raise ImportError('not implement is_empty')
#
# class TestQueue(BaseTaskQueue):
#
#     def __init__(self):
#         self.queue = queue.Queue()
#
#     def get_task(self):
#         """
#         get task from queue
#         :return: dict
#         """
#
#         return self.queue.get()
#
#     def is_empty(self):
#
#         return self.queue.empty()
#
#

#
# """
# q = TestQueue()
# for i in range(5):
#     q.queue.put(i)
# print(q.get_task())
# print(q.get_task())
# """
