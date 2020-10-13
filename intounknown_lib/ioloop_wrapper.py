import tornado.ioloop
import platform
import asyncio

# Tornado IOLoop wrapper
class Loop:
    def __init__(self):
        # Configure selector event loop (run this step only for Windows)
        if platform.system() == 'Windows':
            #print('running Windows only configuration step')
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # python-3.8.0a4

        self.ioloop = tornado.ioloop.IOLoop.instance()

    # Set special parameter cb_delay to add_timeout in seconds (0.5 is a half second)
    #   l.run(func,arg,..)  # run func with args directly passed to callback
    #   l.run(func,arg,...,cb_delay=1,...) # special param for delay (striped from actual callback call)
    def run(self, callback, *args, **kwargs):
        # Get delay param from kwargs and delete it
        delay = kwargs.get('cb_delay', None)
        if delay != None:
            del kwargs['cb_delay']

        # Create scoped callback wrapper
        outer_args = args
        outer_kwargs = kwargs
        def cb():
            callback(*outer_args, **outer_kwargs)

        # Add function enclosure call to ioloop
        if delay == None:
            self.ioloop.add_callback(cb)    # no delay
        else:
            deadline = self.ioloop.time() + delay
            self.ioloop.add_timeout(deadline, cb)    # with delay


    def start(self):
        if self.ioloop != None:
            self.ioloop.start()


    def stop(self):
        if self.ioloop != None:
            self.ioloop.stop()

    def get_time(self):
        return self.ioloop.time()

