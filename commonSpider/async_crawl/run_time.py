def run_time(func):
    import time
    def wrapper(*args, **kwargs):
        t0 = time.time()
        print('start time: %s'% time.strftime('%Y-%m-%d %H:%M:%s', time.localtime()))
        back = func(*args, **kwargs)
        print('end time: %s' %time.strftime('%Y-%m-%d %H:%M:%s', time.localtime()))
        waste = time.time() - t0
        print('waste: %s s'%waste)
        return back
    return wrapper