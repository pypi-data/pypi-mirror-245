from .constants import *
from typing import Union, Callable
import requests
import datetime
import pandas as pd
from functools import wraps

tdf: Callable[[dict], pd.DataFrame] = lambda j: pd.DataFrame(data=j)

gd: Callable[[Union[set, list]], dict] = lambda ks, d: {k: d[k] for k in list(ks) if k in d}


def get(url: str = "") -> requests.Response: # Union[dict, str]:
    r = requests.get(url=url, headers={
        "Referer": f"{MAIN_URL}"
    })
    return r


def post(url: str = "", p: Union[dict, None] = None) -> requests.Response:
    r = requests.post(url=url, headers={
        "Referer": f"{MAIN_URL}"
    }, data=p)
    return r


def outputFormat(method):
    @wraps(method)
    def _w(self, *method_args, **method_kwargs):
        outType: Output = getattr(self, 'outputType', Output.DICT)
        if not isinstance(outType, Output):
            raise Exception(f"The method output type is not ")
        res = method(self, *method_args, **method_kwargs)
        if outType == Output.DATAFRAME:
            return tdf(res)
        elif outType == Output.DICT:
            return res
    return _w


def addFunc(attrName: str = "", funcName: str = "") -> Callable:
    def wrapper(K):
        setattr(K, attrName, eval(funcName))
        return K
    return wrapper


def setOutputFormat(self, out: Output) -> None:
    self.outputType = out
