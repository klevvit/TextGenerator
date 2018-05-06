import time


def time_measure(func):
    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print(func.__name__ + ':', time.clock() - t)
        return res

    return wrapper
