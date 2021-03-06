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
    from intounknown_lib.ioloop_wrapper import Loop
    from random import randint, choice
    from pprint import pprint

    # Async test of state management's event subscriptions
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
                category = choice(['getRecord', 'saveRecord', 'deleteRecord', 'findCoffee'])
                job = self._create_fake_job(category=category, fake_duration=fake_job_exec_time)
                self.work_queue.append(job)


        def _display_fake_jobs(self):
            tmp = deepcopy(self.work_queue)
            tmp = sorted(tmp, key=lambda a: a['fake_duration'])
            print('Fake Jobs in execution order:')
            pprint(tmp)
            print('--- end of fake jobs ---')


        def _process_jobs_in_queue(self):
            while True:
                try:
                    obj = self.work_queue.pop(0)       # get first item in  list (unshift)
                except IndexError:
                    break

                duration = obj['fake_duration']
                category = obj['category']
                job_id = obj['job_id']

                if category == 'shutdown':
                    self.ioloop.run(self.ioloop.stop, cb_delay=duration)
                else:
                    # Create a closure to keep to obj in the scope of the callback
                    def make_cb(obj):
                        # the function return that will be wrapped in the scope where obj was set
                        def run():
                            duration = obj['fake_duration']
                            category = obj['category']
                            job_id = obj['job_id']

                            self.store.set(
                                Consts.STATE_KEY_EVENT1,
                                {'job_id': job_id, 'msg': 'Did work: '+category+' it took '+str(duration)+' execute'}
                            )
                        return run
                    cb = make_cb(obj)   # execute the function and get the closure callback

                    self.ioloop.run(cb, cb_delay=duration)      # run the fake job with the provided delay


        def start(self):
            self._bind()
            self._generate_fake_jobs(num_of_jobs=10, max_duration=5)
            shutdown_job = self._create_fake_job(category='shutdown', fake_duration=7)
            self.work_queue.append(shutdown_job)

            self._display_fake_jobs()
            self._process_jobs_in_queue()

    loop = Loop()           # async loop
    store = StateStore()    # state store
    demo = TestListeners(loop, store)   # demo listener / events
    loop.run(demo.start)    # queue the listener class to start
    loop.start()            # start the tornado ioloop
    print('finished')

    quit()

    # Non async demo below

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


