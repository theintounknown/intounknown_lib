from copy import deepcopy
from pprint import pprint
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from intounknown_lib.tk_gui import install_default_styles, EnhancedButton, EnhancedLabel, EnhancedEntry, EnhancedText, EnhancedCheckbox, ScrollFrame, EnhancedCombobox, EnhancedListbox, HiddenField, EnhancedTable
from intounknown_lib.lib_processing import ProcessManagement, start_worker, printLine, BackgroundManager, start_background_worker

class Application(tk.Tk):
    def __init__(self, process_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.protocol('WM_DELETE_WINDOW', self._quit)
        self.process_manager = process_manager
        self.job_id = 1

        #self.after(1000, lambda: print('after method'))
        self.bg_mgt = BackgroundManager(process_manager, self.after)
        self.bg_mgt.set_notify_subscriber(self._evt_update_job_queue)


        self.title("TK Thread Demo")
        self.geometry("400x500")
        install_default_styles()        # load default style for EnhancedTable

        # Setup content area
        self.main_menu = tk.Frame(self)
        content = ttk.LabelFrame(self.main_menu, text="Thread Control")

        self.inputs = {}

        #jobs = [(1, 'One'), (2, 'Two'), (3, 'Three')]
        self.inputs['jobs'] = EnhancedListbox(content, 'Jobs')
        #self.inputs['jobs'].set_options(jobs)
        self.inputs['jobs'].grid(row=0, column=0, sticky=(tk.N + tk.W))

        EnhancedLabel(content, 'Responses').grid(row=1, column=0, sticky=(tk.N + tk.W))
        self.inputs['responses'] = EnhancedText(content, None, 'some text')
        self.inputs['responses'].grid(row=2, column=0, sticky=(tk.N + tk.W))


        EnhancedButton(content, 'Add Job', command=self.add_job) \
            .grid(row=3, column=0, sticky=(tk.N + tk.W))

        EnhancedButton(content, 'Print Job Responses', command=self.print_response_queue) \
            .grid(row=4, column=0, sticky=(tk.N + tk.W))

        #EnhancedButton(content, 'Update Form', command=self.update_form) \
        #    .grid(row=5, column=0, sticky=(tk.N + tk.W))

        EnhancedButton(content, 'Shutdown', command=lambda: None) \
            .grid(row=5, column=0, sticky=(tk.N + tk.W))

        content.grid(row=0, column=0, sticky=(tk.N + tk.W))
        self.main_menu.grid(row=0, column=0, sticky=(tk.N + tk.W))

    def _quit(self, event=None):
        self.bg_mgt.shutdown()
        self.destroy()

    def _queue_job(self, msg):
        request_job_msg = f"Job {self.job_id}"
        self.bg_mgt.add_job(request_job_msg, self._evt_update_form)
        self.job_id += 1

    def _evt_update_job_queue(self, jobs):
        #if len(jobs) < 1:
        #    return

        options = []
        for job in jobs:
            options.append((job, job))

        self.inputs['jobs'].set_options(options)


    def _evt_update_form(self, response):
        text = self.inputs['responses'].get()
        lines = text.split('\n')
        lines.insert(0, response)   # insert text at the top

        # remove trailing lines after ten items
        while len(lines) > 10:
            lines.pop()

        output = '\n'.join(lines)

        self.inputs['responses'].set(output)  # assuming text for testing
        #self.inputs['responses'].set(response)  # assuming text for testing

    def update_formXXXX(self):
        msg = {
            'jobs': [(1, 'One'), (2, 'Two'), (3, 'Three')],
            #'jobs' : 1,
            'responses': 'One\nTwo\n',
        }

        for key, val in msg.items():
            if key == 'jobs':
                self.inputs[key].set_options(val)
                continue

            self.inputs[key].set(val)

    def add_job(self):
        printLine('add_job called')
        txt = f'job {self.job_id}'
        self._queue_job(txt)

    def print_response_queue(self):
        worker_id = self.process_manager.get_random_worker()
        result = self.process_manager.slurp_work_out(worker_id)
        printLine(result)


if __name__ == '__main__':
    p = ProcessManagement()

    #p.create_thread(start_worker, worker_id=1)
    for i in range(1, 5):
        p.create_thread(start_background_worker, worker_id=i)
        #p.create_thread(start_background_worker, worker_id=1)

    app = Application(p)
    app.mainloop()          # blocking

    #p.shutdown(worker_id)
    p.shutdown_all()

