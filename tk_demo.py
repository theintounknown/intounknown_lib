import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from intounknown_lib.tk_gui import EnhancedButton, EnhancedLabel, EnhancedEntry, EnhancedText, EnhancedCheckbox, ScrollFrame, EnhancedCombobox


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("TK Demo")
        self.geometry("700x400")

        # Setup content area
        self.main_menu = tk.Frame(self)
        content = ttk.LabelFrame(self.main_menu, text="Content Area")

        # Setup Notebook
        self.tabs = ttk.Notebook(self.main_menu)
        entry_frame = ScrollFrame(self.tabs)

        ### Entry Tab ###
        # Row 0
        self.process_input = EnhancedEntry(entry_frame.viewport, 'Input:',
            label_args={'width': 10})
        self.process_input.grid(row=0, column=0, sticky=(tk.W + tk.N))

        btn_process = EnhancedButton(entry_frame.viewport, "Process Input", command=self.process_user_input)
        btn_process.grid(row=0, column=1, sticky=(tk.W + tk.N))

        # Row 1
        self.process_status = EnhancedLabel(entry_frame.viewport, "Getting Ready...")
        # input_args={'foreground': 'red'}
        self.process_status.grid(row=1, column=0, sticky=tk.N)
        self.after(4000, lambda: self.set_loaded_status('Ready'))

        clear_process_status = EnhancedButton(entry_frame.viewport, "Clear Process Status", command=self.clear_process_status)
        clear_process_status.grid(row=1, column=1, sticky=(tk.W + tk.N))

        # Row 2
        btn_quit = EnhancedButton(entry_frame.viewport, "QUIT", self.destroy)
        btn_quit.grid(row=2, column=1, sticky=(tk.W + tk.N))

        ### End Entry Tab ###


        ### Start Text Tab ###
        text_frame = ScrollFrame(self.tabs)

        # Row 3 - textarea
        # Draw textarea
        self.input_textarea = EnhancedText(text_frame.viewport, 'Textarea', 'some text')
        self.input_textarea.grid(row=0, column=0, sticky=(tk.N + tk.W))

        # Row 4 - textarea text controls
        EnhancedButton(text_frame.viewport, "Get Text", self.click_get_textarea).grid(row=1, column=0, sticky=(tk.N + tk.W))

        self.textarea_entry = EnhancedEntry(text_frame.viewport, 'Input:', label_args={'width': 10})
        self.textarea_entry.grid(row=2, column=0, sticky=(tk.W + tk.N))

        EnhancedButton(text_frame.viewport, "Set Text", self.click_set_textarea).grid(row=3, column=0, sticky=(tk.N + tk.W))
        EnhancedButton(text_frame.viewport, "Clear Text", self.click_clear_textarea).grid(row=4, column=0, sticky=(tk.N + tk.W))

        ### End Text Tab ###


        ### Start Checkbox Tab ###
        checkbox_frame = ScrollFrame(self.tabs)

        # Row 5 - checkbox
        self.checkbox = EnhancedCheckbox(checkbox_frame.viewport, 'Checkbox', True)
        self.checkbox.grid(row=0, column=0, sticky=(tk.N + tk.W))

        EnhancedButton(checkbox_frame.viewport, "Set True", self.click_set_checkbox).grid(row=1, column=0, sticky=(tk.N + tk.W))
        EnhancedButton(checkbox_frame.viewport, "Clear", self.click_clear_checkbox).grid(row=2, column=0, sticky=(tk.N + tk.W))
        EnhancedButton(checkbox_frame.viewport, "Get Value", self.click_get_checkbox).grid(row=3, column=0, sticky=(tk.N + tk.W))

        ### End Checkbox Tab ###


        ### Start Scrolling Frame ###
        scrolling_frame = ScrollFrame(self.tabs, height=80)
        list_of_numbers = "\n".join([str(a) for a in range(0, 100)])
        EnhancedLabel(scrolling_frame.viewport, list_of_numbers).grid(row=0, column=0, sticky=(tk.N + tk.W))
        #scrolling_frame.grid(row=6, column=0, sticky=(tk.N + tk.W + tk.E + tk.S))

        ### End Scrolling Frame ###


        ### Start Combobox Frame ###

        combobox_frame = ScrollFrame(self.tabs)
        values = [
            (1, 'Orange'),
            (2, 'Purple'),
            (3, 'Green'),
            (4, 'Yellow'),
            (5, 'Blue'),
        ]
        self.combobox = EnhancedCombobox(combobox_frame.viewport, 'Combo Box', values=values)
        #self.combobox = EnhancedCombobox(combobox_frame.viewport, 'Combo Box', values=values, default_value=3)
        self.combobox.grid(row=0, column=0, sticky=(tk.N + tk.W))

        EnhancedButton(combobox_frame.viewport, 'Get', command=lambda: print(self.combobox.get()))\
            .grid(row=1, column=0, sticky=(tk.N + tk.W))

        EnhancedButton(combobox_frame.viewport, 'Set', command=lambda: print(self.combobox.set(4))) \
            .grid(row=2, column=0, sticky=(tk.N + tk.W))

        values = [
            (4, 'Yellow'),
            (1, 'Orange'),
            (3, 'Green'),
            (6, 'Pink'),
            (7, 'White'),
            (2, 'Purple'),
            (5, 'Blue'),
        ]

        EnhancedButton(combobox_frame.viewport, 'Update Options', command=lambda: print(self.combobox.set_options(values))) \
            .grid(row=3, column=0, sticky=(tk.N + tk.W))

        EnhancedButton(combobox_frame.viewport, 'Get Title', command=lambda: print(self.combobox.get_title())) \
            .grid(row=4, column=0, sticky=(tk.N + tk.W))

        EnhancedButton(combobox_frame.viewport, 'Clear', command=lambda: print(self.combobox.clear())) \
            .grid(row=5, column=0, sticky=(tk.N + tk.W))

        EnhancedButton(combobox_frame.viewport, 'Get Values', command=lambda: print(self.combobox.get_values())) \
            .grid(row=6, column=0, sticky=(tk.N + tk.W))


        self.tabs.grid(row=0, column=0, sticky=(tk.N, tk.W + tk.S + tk.E))
        self.tabs.add(entry_frame, text='Entry')
        self.tabs.add(text_frame, text='Text')
        self.tabs.add(checkbox_frame, text='Checkbox')
        self.tabs.add(scrolling_frame, text='Scrolling Frame')
        self.tabs.add(combobox_frame, text='Combobox')

        #content.grid(row=0, column=0, sticky=tk.W)
        self.main_menu.grid(row=0, column=0, sticky=(tk.N, tk.W))

        self.process_input.set('<your input here>')
        self.process_input.focus()



    def set_loaded_status(self, new_status):
        self.process_status.set(new_status)

    def clear_process_status(self):
        #self.process_status.clear()
        self.process_status.set('Ready')

    def process_user_input(self):
        status = self.process_status.get()
        self.process_status.set("Processing...")
        txt_to_process = self.process_input.get()
        def cb():
            self.set_loaded_status('Done ['+txt_to_process+']')
            self.process_input.clear()

        self.after(1000, cb)


    # Textarea text controls

    def click_set_textarea(self):
        val = self.textarea_entry.get()
        self.input_textarea.set(val)

    def click_get_textarea(self):
        print(self.input_textarea.get())

    def click_clear_textarea(self):
        self.input_textarea.clear()


    # Checkbox test controls

    def click_set_checkbox(self):
        self.checkbox.set(True)

    def click_get_checkbox(self):
        print(self.checkbox.get())

    def click_clear_checkbox(self):
        self.checkbox.clear()


if __name__ == '__main__':
    app = Application()
    app.mainloop()

