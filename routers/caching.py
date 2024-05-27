import os
import pickle
from functools import wraps

def exportable_cache(func):
    func.cache = {}
    if os.path.exists('factorial_cache.pkl'):
        with open('factorial_cache.pkl', 'rb') as f:
            func.cache = pickle.load(f)
    
    @wraps(func)
    def wrapper(*args):
        if args in func.cache.keys():
            return func.cache[args]
        else:
            result = func(*args)
            func.cache[args] = result
            return result
    return wrapper