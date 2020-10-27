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



def start_worker(queues):
    work_queue_in = queues.get('work_in')
    work_queue_out = queues.get('work_out')
    cmd_queue_in = queues.get('in')
    cmd_queue_out = queues.get('out')

    printLine('worker starting')

    while True:
        if work_queue_in != None:
            msg = work_queue_in.read(1)     # read from the work and wait 1 second for message
            if msg != None:
                printLine('work:', msg)
                work_queue_out.write('worker received work: '+ msg)

        msg = cmd_queue_in.read()   # check queue but don't wait
        if msg != None:
            printLine('cmd_msg:', msg)
            cmd_queue_out.write('worker cmd received: '+ msg)
        if msg == 'shutdown':
            printLine('shutting down worker')
            break

    printLine('worker is shutdown')



class ProcessManagement:
    def __init__(self):
        self.queue_work_in = ThreadCom()
        self.queue_work_out = ThreadCom()

        self.worker_id = 0
        self.workers = {}

    def create_thread(self, target_func, *args, **kwargs):
        worker_id = self.worker_id

        in_com = ThreadCom()
        out_com = ThreadCom()

        t = Thread(target=target_func, *args, **kwargs)

        self.workers[worker_id] = {
            'type': 'thread',
            'object': t,
            'in_com': in_com,
            'out_com': out_com,
        }

        t.start()

        self.worker_id += 1

    # write to work input queue
    def write_work(self, msg):
        self.queue_work_in.write(msg)

    # read from work output queue
    def read_work(self, wait_time=0):
        return queue_work_out.read(wait_time)

    # write a worker's command input
    def write_in(self, worker_id, msg):
        worker = self.workers.get(worker_id, None)
        if worker == None:
            raise Exception('worker_id ['+worker_id+'] not found ')

        worker['in'].write(msg)

    # read from a worker's command output
    def read_out(self, worker_id, wait_time=0):
        worker = self.workers.get(worker_id, None)
        if worker == None:
            raise Exception('worker_id [' + worker_id + '] not found ')

        worker['out'].read(wait_time))

    # clear the queue and all memory before shutdown
    def drain_work_in_queue(self):
        pass

    # clear the queue and all memory before shutdown
    def drain_work_out_queue(self):
        pass

    # shutdown a worker
    def shutdown(self, worker_id):
        pass

    # shutdown all workers
    def shutdown_all(self):
        pass


t = Thread(target=start_worker, args=[queues])
t.start()
sleep(1)
queues['in'].write('some other message')
queues['in'].write('shutdown')

printLine(queues['out'].read(0.5))

while True:
    t.join(0.5)
    if not t.is_alive():
        break

printLine('done.')
