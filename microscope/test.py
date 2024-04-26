from multiprocessing.managers import Namespace
from multiprocessing import Process, Manager
import time


def runner(ns):
    while True:
        print(f'minor: {ns.val}')
        time.sleep(0.1)
        

def run():
    
    manager = Manager()
    ns = manager.Namespace()
    ns.val = 0
    process = Process(
        target=runner,
        kwargs=dict(ns=ns)
    )
    process.start()
    
    while True:
        ns.val = abs(ns.val-1)
        time.sleep(1)
        print(f'     : {ns.val}')
    
if __name__ == '__main__':
    run()
        
