import hashlib
import importlib
class SarError:
    def __init__(self, error):
        self.error = error


def rscript_composit(_data):
    """

    :param data: json inpput['data']
    :return: params -> n0=1,basis=3,randomize=FALSE,alpha=1.68
    """
    if _data.get('params') is not None:
        data = _data['params']
        return _composite(data, '{}={},')
    if _data.get('exprs') is not None:
        data = _data['exprs']
        return _composite(data, '{}<-{};')

def _composite(data, string =None):
    _list = []
    for i in data.items():
        param = string.format(i[0], i[1])
        _list.append(param)
    return ''.join(_list)[:-1]





def hash_sha1(string):
    _hash = hashlib.sha1()
    _hash.update(string.encode('utf-8'))
    return _hash.hexdigest()

