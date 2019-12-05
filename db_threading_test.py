from threading import Condition, Lock, Thread
import time
import random
import sys

class UpdateLock:
    def __init__(self):
        self.lock = Lock()
        self.updating_cond = Condition()
        self.is_updating = False
        
    def wait_for_clearance(self):
        if self.is_updating:
            with self.updating_cond:
                self.updating_cond.wait_for(lambda: self.is_updating == False)

    def start_update(self):
        self.lock.acquire()
        self.is_updating = True
    
    def finish_update(self):
        self.lock.release()
        self.is_updating = False
        with self.updating_cond:
            self.updating_cond.notify_all()
    
    def __enter__(self):
        self.start_update()
    
    def __exit__(self, type, value, traceback):
        self.finish_update()

class QueryLock:
    def __init__(self):
        self.lock = Lock()
        self.counter_lock = Lock()
        self.query_cond = Condition()
        self.counter = 0
        
    def wait_for_clearance(self):
        if self.counter > 0:
            with self.query_cond:
                self.query_cond.wait_for(lambda: self.counter == 0)

    def change_counter(self, value):
        self.counter_lock.acquire()
        self.counter += value
        self.counter_lock.release()

    def start_query(self):
        self.change_counter(+1)
    
    def finish_query(self):
        self.change_counter(-1)
        if self.counter == 0:
            with self.query_cond:
                self.query_cond.notify_all()

    def __enter__(self):
        self.start_query()
    
    def __exit__(self, type, value, traceback):
        self.finish_query()

class DbSim:
    deleted = False
    query_lock = QueryLock()
    update_lock = UpdateLock()
    counter_mutex = Lock()
    error_count = 0
    didnt_get_data_count = 0
    def get_data(self):
        with self.counter_mutex:
            self.didnt_get_data_count += 1
        self.update_lock.wait_for_clearance()
        with self.query_lock:
            time.sleep(0.5)

            if self.deleted:
                print('ERROR tried to pull data while data is deleted')
                self.error_count += 1
            else:
                print(f'Got data. Concurrent requests: {self.query_lock.counter}')
        with self.counter_mutex:
            self.didnt_get_data_count -= 1

    def put_data(self):
        with self.update_lock:
            self.query_lock.wait_for_clearance()
            
            self.deleted = True
            time.sleep(1)
            print('Data deleted')
            time.sleep(1)
            print('New data added')
            time.sleep(1)
            self.deleted = False
            
            self.isUpdating = False
            
 
class Putter(Thread):
    def __init__(self, db_sim):
        Thread.__init__(self)
        self.db_sim = db_sim

    def run(self):
        self.db_sim.put_data()


class Getter(Thread):
    def __init__(self, db_sim):
        Thread.__init__(self)
        self.db_sim = db_sim

    def run(self):
        self.db_sim.get_data()

def start_pthread(db_sim):
    putters = [Putter(db_sim) for i in range(10)]
    for p in putters:
        p.start()
        p.join()
        time.sleep(random.randrange(1, 5))

def start_gthread(db_sim):
    getters = [Getter(db_sim) for i in range(1000)]
    for g in getters:
        g.start()
        if (random.random() > .8):
            time.sleep(random.random())
    for g in getters:
        g.join()

def main():
    db_sim = DbSim()
    
    p_thread = Thread(target=lambda: start_pthread(db_sim))
    g_thread = Thread(target=lambda: start_gthread(db_sim))
    
    p_thread.start()
    g_thread.start()
    p_thread.join()
    g_thread.join()
    
    print(f'Errors: {db_sim.error_count}')
    print(f"Didn't get data count: {db_sim.didnt_get_data_count}")
main()