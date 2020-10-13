from copy import deepcopy

class Consts:
    STATE_KEY_EVENT1 = 'state_key.event1'
    STATE_KEY_EVENT2 = 'state_key.event2'


class StateStore:
    def __init__(self):
        self.state = {}
        self.callbacks = {}
        self.sub_id = 0
        # {'<sub_id>' : {'cb': <cb>, 'key': <key>}}

    # Get key a key in a state (returns None if does not exist)
    def get(self, key):
        if key in self.state:
            new_value = self.state[key]
            return deepcopy(new_value)

        return None

    # Notify subscribers of a data change if they are subscribed to the key
    def _notifySubscribers(self, key, new_value):
        for sub_id, obj in self.callbacks.items():
            cb = obj['cb']      # get subscriber callback
            # if a subscriber is subscribed to this key, notify them

            if obj['key'] == key:
                new_value_copy = deepcopy(new_value)
                cb(key, new_value_copy)       # call subscriber callback


    # Set a value in the state by key
    def set(self, key, new_value):
        dirty = False       # if value has changed from the previous value
        old_value = self.state.get(key, None)

        if old_value != new_value:
            dirty = True    # make dirty if value has changed
        self.state[key] = new_value     # update the state

        # Notify subscribers if the state has changed
        if dirty:
            self._notifySubscribers(key, new_value)


    # Clear the contents of the a key
    def clear(self, key=None):
        if key in self.state:
            del self.state[key]     # deallocate key in state
            self._notifySubscribers(key, None)


    # Bind a listening function (callback) to a key's state change
    def subscribe(self, key, cb):
        self.callbacks[self.sub_id] = {
            'cb': cb,
            'key': key,
        }

        new_sub_id = self.sub_id
        self.sub_id += 1       # increment subscription id
        cb(key, self.get(key))   # send stored

        return new_sub_id   # return new subscription id

    # Cancel a subscription
    def unsubscribe(self, sub_id):
        if sub_id in self.callbacks:
            del self.callbacks[sub_id]


if __name__ == '__main__':
    from core_lib.ioloop_wrapper import Loop
    from random import randint, choice
    from pprint import pprint

    #loop = Loop()
    #from time import sleep
    # try:
    #     print('started')
    #     #sleep(2)
    #     print('done sleeping')
    #     loop.run(lambda: print('test 0'))
    #     loop.run(lambda: print('test 1'), cb_delay=1)
    #     loop.run(lambda: print('test 2'), cb_delay=2)
    #     loop.run(lambda: print('test 3'))
    #     loop.run(lambda: loop.stop(), cb_delay=4)
    #     loop.start()        # start ioloop, this is blocking
    # except:
    #     pass
    # print('stopped')
    # quit()

    # import tornado.ioloop
    # import platform
    #
    # # Configure selector event loop (run this step only for Windows)
    # if platform.system() == 'Windows':
    #     print('running Windows only configuration step')
    #     import asyncio
    #     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # python-3.8.0a4
    #
    # loop = tornado.ioloop.IOLoop.current()

    class TestListeners:
        def __init__(self, ioloop, store):
            self.ioloop = ioloop
            self.store = store

            self.job_id = 0         # id incrementer for our fake jobs
            self.work_queue = []    # a little fake work queue

        # receive the incoming key that changed and the state
        def _lister_test1(self, key, state):
            print('lister_test1', key, state)

        def _lister_test2(self, key, state):
            print('lister_test2', key, state)

        def _bind(self):
            self.store.subscribe(Consts.STATE_KEY_EVENT1, self._lister_test1)
            self.store.subscribe(Consts.STATE_KEY_EVENT1, self._lister_test2)
            self.store.subscribe(Consts.STATE_KEY_EVENT2, self._lister_test2)

        def _create_fake_job(self, category='test', fake_duration=1):
            obj = {
                'fake_duration': fake_duration,
                'category': category,
                'job_id': self.job_id,
            }
            self.job_id += 1
            return obj


        def _generate_fake_jobs(self, num_of_jobs=10, max_duration=5):
            for i in range(0, num_of_jobs):
                fake_job_exec_time = randint(1, max_duration)
                category = choice(['saveRecord', 'executeNotepad', 'getCoffee', 'someElse'])
                job = self._create_fake_job(category=category, fake_duration=fake_job_exec_time)
                self.work_queue.append(job)


        def _display_fake_jobs(self):
            tmp = deepcopy(self.work_queue)
            tmp = sorted(tmp, key=lambda a: a['fake_duration'])
            print('Fake Jobs in execution order')
            pprint(tmp)


        # def _do_work(self):
        #     self.ioloop.run(
        #         lambda: self.store.set(
        #             Consts.STATE_KEY_EVENT1,
        #             {'id': 1, 'msg': 'The first message'}
        #         )
        #     )
        #
        #     self.ioloop.run(lambda: self.ioloop.stop(), cb_delay=1)

        def _process_jobs_in_queue(self):
            while True:
                try:
                    obj = self.work_queue.pop()
                except IndexError:
                    break

                print(obj)
                duration = obj['fake_duration']
                category = obj['category']
                job_id = obj['job_id']

                self.ioloop.run(
                    lambda: self.store.set(
                        Consts.STATE_KEY_EVENT1,
                        {'id': job_id, 'msg': 'Did work: '+category+' it took '+str(duration)+' execute'}
                    )
                    #cb_delay=duration
                )


        def start(self):
            self._bind()
            #self._do_work()
            self._generate_fake_jobs(num_of_jobs=10, max_duration=5)
            self._create_fake_job(category='shutdown', fake_duration=7)
            self._process_jobs_in_queue()



    #     loop.run(lambda: print('test 0'))


    loop = Loop()           # async loop
    store = StateStore()    # state store
    demo = TestListeners(loop, store)   # demo listener / events
    #demo._display_fake_jobs()

    #pprint(demo.work_queue)
    #quit()

    loop.run(demo.start)    # queue the listener class to start
    loop.start()            # start the tornado ioloop
    print('finished')


    quit()


    def lister_test1(key, state):
        print('lister_test1', key, state)


    def lister_test2(key, state):
        print('lister_test2', key, state)


    store = StateStore()
    lister1_id = store.subscribe(Consts.STATE_KEY_EVENT1, lister_test1)
    print(lister1_id)
    lister2_id = store.subscribe(Consts.STATE_KEY_EVENT1, lister_test2)
    lister2_b_id = store.subscribe(Consts.STATE_KEY_EVENT2, lister_test2)
    print(lister2_id)

    print('*** end initialization phase')
    print()
    store.set(Consts.STATE_KEY_EVENT1, {'id': 1, 'msg': 'hello world`'})
    store.set(Consts.STATE_KEY_EVENT2, {'id': 2, 'msg': 'good bye world`'})
    print('get:', store.get(Consts.STATE_KEY_EVENT1))
    store.clear(Consts.STATE_KEY_EVENT2)    # deletes the key from the state
    store.clear(Consts.STATE_KEY_EVENT2)    # does nothing because key already deleted
    store.unsubscribe(lister2_b_id)         # unsubscribe here
    store.set(Consts.STATE_KEY_EVENT2, 'some text')     # so it does not recieve this message


