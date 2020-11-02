# Import Threading Objects
from threading import Thread
from threading import RLock as ThreadLock
from queue import Queue as ThreadQueue
from queue import Empty as QueueEmpty

# Import Multiprocessing Objects
from multiprocessing import Process
from multiprocessing import RLock as ProcessLock
from multiprocessing import Queue as ProcessQueue

from time import time, sleep
from random import randint

print_lock = ThreadLock()
def printLine(*args, **kwargs):
    with print_lock:
        print(*args, **kwargs)

# ThreadCommunication
class ThreadCom:
    def __init__(self):
        self.com = ThreadQueue()

    # read and return immediately or wait and block for X seconds
    def read(self, timeout=0):
        block = False
        if timeout != 0:
            block = True
        try:
            return self.com.get(block, timeout)
        except QueueEmpty:
            return None

    # run size the queue
    def size(self):
        return self.com.qsize()

    # if queue is empty (has no work)
    def is_empty(self):
        return self.com.empty()

    # write a job to the queue
    def write(self, msg):
        self.com.put(msg)

    # block until queue is empty
    def join(self):
        self.com.join()


# Process communication via queues
class ProcessCom(ThreadCom):
    def __init__(self):
        self.com = ProcessQueue()


class ProcessManagement:
    def __init__(self):
        self.process_queue_work_in = None
        self.process_queue_work_out =  None

        self.thread_queue_work_in =  None
        self.thread_queue_work_out =  None

        self.worker_id = 0
        self.workers = {}
            # {
            # 'type': 'thread',
            # 'object': t,
            # 'in_com': in_com,
            # 'out_com': out_com,
            # }

    def _get_object(self, worker_id):
        worker = self.workers.get(worker_id, None)
        if not worker:
            raise Exception('worker_id ['+worker_id+'] not found ')
        return worker

    def create_thread(self, target_func, **kwargs):
        worker_id = self.worker_id
        self.worker_id += 1

        # initialize work in queue it not defined
        if not self.thread_queue_work_in:
            self.thread_queue_work_in = ThreadCom()

        # initialize work out queue it not defined
        if not self.thread_queue_work_out:
            self.thread_queue_work_out = ThreadCom()

        in_com = ThreadCom()
        out_com = ThreadCom()

        queues = {
            'work_in': self.thread_queue_work_in,
            'work_out': self.thread_queue_work_out,
            'in': in_com,
            'out': out_com,
        }

        input = kwargs
        input['queues'] = queues

        t = Thread(target=target_func, kwargs=input)

        self.workers[worker_id] = {
            'type': 'thread',
            'object': t,
            'in_com': in_com,
            'out_com': out_com,
            'work_in': self.thread_queue_work_in,
            'work_out':  self.thread_queue_work_out,
        }

        t.start()

        return worker_id


    def create_process(self, target_func, **kwargs):
        worker_id = self.worker_id
        self.worker_id += 1

        # initialize work in queue it not defined
        if not self.process_queue_work_in:
            self.process_queue_work_in = ProcessCom()

        # initialize work out queue it not defined
        if not self.process_queue_work_out:
            self.process_queue_work_out = ProcessCom()

        in_com = ProcessCom()
        out_com = ProcessCom()

        queues = {
            'work_in': self.process_queue_work_in,
            'work_out': self.process_queue_work_out,
            'in': in_com,
            'out': out_com,
        }

        input = kwargs
        input['queues'] = queues

        p = Process(target=target_func, kwargs=input)

        self.workers[worker_id] = {
            'type': 'process',
            'object': p,
            'in_com': in_com,
            'out_com': out_com,
            'work_in': self.process_queue_work_in,
            'work_out':  self.process_queue_work_out,
        }

        p.start()

        return worker_id



    # write to work input queue
    def write_work(self, worker_id, msg):
        worker = self._get_object(worker_id)
        #printLine('write_work:', worker)
        worker['work_in'].write(msg)

    # read from work output queue
    def read_work(self, worker_id, wait_time=0):
        worker = self._get_object(worker_id)
        return worker['work_out'].read(wait_time)

    # write a worker's command input
    def write_in(self, worker_id, msg):
        worker = self._get_object(worker_id)
        worker['in_com'].write(msg)

    # read from a worker's command output
    def read_out(self, worker_id, wait_time=0):
        worker = self._get_object(worker_id)
        worker['out_com'].read(wait_time)

    def get_queue_sizes(self, worker_id):
        worker = self._get_object(worker_id)
        return {
            'work_in' : worker['work_in'].size(),
            'work_out' : worker['work_out'].size(),
        }

    def _drain_queue(self, queue_obj):
        result = []
        if queue_obj is None:
            return result

        while True:
            msg = queue_obj.read()
            result.append(msg)
            if msg is None:
                break

        return result

    # clear the work queues and all memory before shutdown
    def drain_work_queues(self):
        self._drain_queue(self.process_queue_work_in)
        self._drain_queue(self.process_queue_work_out)
        self._drain_queue(self.thread_queue_work_in)
        self._drain_queue(self.thread_queue_work_out)


    # shutdown a worker
    def shutdown(self, worker_id):
        self.write_in(worker_id, 'shutdown')        # send the shutdown command to the process or thread
        worker = self._get_object(worker_id)
        process_or_thread = worker['object']

        while True:
            process_or_thread.join(0.5)
            if not process_or_thread.is_alive():
                break

    # shutdown all workers
    def shutdown_all(self):
        for worker_id in tuple(self.workers.keys()):
            self.shutdown(worker_id)


def start_worker(queues=None, worker_id=None):
    #printLine('start_worker', queues)
    work_queue_in = queues.get('work_in')
    work_queue_out = queues.get('work_out')
    cmd_queue_in = queues.get('in')
    cmd_queue_out = queues.get('out')

    printLine(f'worker [{worker_id}] starting')

    while True:
        if work_queue_in != None:
            msg = work_queue_in.read(0.5)     # read from the work and wait 1 second for message
            if msg != None:
                rand_sleep = randint(0, 1000) / 1000.0
                #rand_sleep = randint(0, 5)
                printLine(f'worker [{worker_id}]:', rand_sleep, msg)
                sleep(rand_sleep)
                work_queue_out.write('worker received work: '+ msg)

        msg = cmd_queue_in.read()   # check queue but don't wait
        if msg == 'shutdown':
            printLine('cmd: shutting down worker')
            break
        elif msg != None:
            printLine('cmd:', msg)
            cmd_queue_out.write('worker cmd received: '+ msg)
            printLine('cmd: message has been written: '+ msg)

    printLine('worker is shutdown')



if __name__ == '__main__':

    p = ProcessManagement()
    worker_ids = []
    for a in range(12):
        worker_ids.append(p.create_thread(start_worker, worker_id=a))
        #worker_ids.append(p.create_process(start_worker, worker_id=a))

    first_id = worker_ids[0]

    number_of_jobs = 100
    for a in range(number_of_jobs):
        txt = f'job {a}'
        p.write_work(first_id, txt)


    completed_jobs = 0

    # drain queues and force a shutdown
    #if True:
    #    sleep(1)
    #    printLine(p.get_queue_sizes(first_id))
    #    p.drain_work_queues()
    #    completed_jobs = number_of_jobs

    while True:
        result = p.read_work(first_id, 0.5)
        if result is not None:
            completed_jobs += 1

        if completed_jobs >= number_of_jobs:
            break

    p.shutdown_all()



    # p = ProcessManagement()
    # worker_id = p.create_thread(start_worker)
    # p.write_work(worker_id, 'work 1')
    # p.write_in(worker_id, 'cmd 1')
    # sleep(2)
    # printLine('output: work queue:', p.read_work(worker_id, 0.5))
    # p.shutdown_all()



# t = Thread(target=start_worker, args=[queues])
# t.start()
# sleep(1)
# queues['in'].write('some other message')
# queues['in'].write('shutdown')
#
# printLine(queues['out'].read(0.5))
#
# while True:
#     t.join(0.5)
#     if not t.is_alive():
#         break
#
# printLine('done.')


