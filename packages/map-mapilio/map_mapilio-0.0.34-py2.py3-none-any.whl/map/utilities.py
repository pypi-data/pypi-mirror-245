from json import JSONEncoder
import numpy as np
import decimal


class JSON_ENCODER_FIX(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, np.int64):
            return  int(obj)
        return JSONEncoder.default(self, obj)
