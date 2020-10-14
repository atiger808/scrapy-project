

from scrapy import cmdline
import threading
import multiprocessing
from run_time import run_time

def work(x):
    print(x)
    cmdline.execute('scrapy crawl femdom_novel_slaver'.split())

@run_time
def run():
    processes = [multiprocessing.Process(target=work, args=(t, )) for t in range(10)]
    for t in processes:
        t.start()
    for t in processes:
        t.join()

run()