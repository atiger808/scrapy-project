import time

def run_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        print('start time； %s' %(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start))))
        back = func(*args, **kwargs)
        end = time.time()
        print('end time: %s' %(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end))))
        print('waste time: %s'%(end - start))
        return back
    return wrapper