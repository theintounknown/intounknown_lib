from copy import deepcopy
from pprint import pprint
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from intounknown_lib.tk_gui import install_default_styles, EnhancedButton, EnhancedLabel, EnhancedEntry, EnhancedText, EnhancedCheckbox, ScrollFrame, EnhancedCombobox, EnhancedListbox, HiddenField, EnhancedTable
from intounknown_lib.lib_processing import ProcessManagement, start_worker, printLine

class Application(tk.Tk):
    def __init__(self, process_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.process_manager = process_manager
        self.job_id = 1

        self.title("TK Thread Demo")
        self.geometry("300x400")
        install_default_styles()        # load default style for EnhancedTable

        # Setup content area
        self.main_menu = tk.Frame(self)
        content = ttk.LabelFrame(self.main_menu, text="Thread Control")

        EnhancedButton(content, 'Add Job', command=self.add_job) \
            .grid(row=0, column=0, sticky=(tk.N + tk.W))

        EnhancedButton(content, 'Print Job Responses', command=self.print_response_queue) \
            .grid(row=1, column=0, sticky=(tk.N + tk.W))

        EnhancedButton(content, 'Shutdown', command=lambda: None) \
            .grid(row=2, column=0, sticky=(tk.N + tk.W))

        content.grid(row=0, column=0, sticky=(tk.N + tk.W))
        self.main_menu.grid(row=0, column=0, sticky=(tk.N + tk.W))

    def _queue_job(self, msg):
        worker_id = self.process_manager.get_random_worker()
        self.process_manager.write_work(worker_id, msg)
        self.job_id += 1

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

    p.create_thread(start_worker, worker_id=1)

    app = Application(p)
    app.mainloop()          # blocking

    #p.shutdown(worker_id)
    p.shutdown_all()

