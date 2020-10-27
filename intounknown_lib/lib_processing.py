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


queue_work_in = ThreadCom()
queue_work_out = ThreadCom()

queues = {
    'work_in': queue_work_in,
    'work_out': queue_work_out,
    'in': ThreadCom(),
    'out': ThreadCom(),
}


t = Thread(target=start_worker, args=[queues])
t.start()
queue_work_in.write('first job')
sleep(1)
queues['in'].write('some other message')
queues['in'].write('shutdown')

printLine('from work out: '+queue_work_out.read(0.5))
printLine(queues['out'].read(0.5))

while True:
    t.join(0.5)
    if not t.is_alive():
        break

printLine('done.')
