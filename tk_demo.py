from copy import deepcopy
from pprint import pprint
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from intounknown_lib.tk_gui import install_default_styles, EnhancedButton, EnhancedLabel, EnhancedEntry, EnhancedText, EnhancedCheckbox, ScrollFrame, EnhancedCombobox, EnhancedListbox, HiddenField, EnhancedTable


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("TK Demo")
        self.geometry("700x600")

        install_default_styles()        # load default style for EnhancedTable

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


        ### End Combobox Frame ###
        ### Start Listbox Frame ###

        listbox_frame = ScrollFrame(self.tabs, height=500)

        values = [
            ('orange', 'Orange'),
            (2, 'Purple'),
            (3, 'Green'),
            (4, 'Yellow'),
            (5, 'Blue'),
        ]

        self.listbox = EnhancedListbox(listbox_frame.viewport, 'ListBox', values)
        self.listbox.set_options(values)
        self.listbox.grid(row=0, column=0, sticky=(tk.N + tk.W))

        values = [
            (4, 'Yellow'),
            (1, 'Orange'),
            (3, 'Green'),
            (6, 'Pink'),
            (7, 'White'),
            (2, 'Purple'),
            (5, 'Blue'),
        ]

        EnhancedButton(listbox_frame.viewport, 'Get', command=lambda: print(self.listbox.get())) \
            .grid(row=1, column=0, sticky=(tk.N + tk.W))

        EnhancedButton(listbox_frame.viewport, 'Clear', command=lambda: print(self.listbox.clear())) \
            .grid(row=2, column=0, sticky=(tk.N + tk.W))

        EnhancedButton(listbox_frame.viewport, 'Set to Yellow', command=lambda: print(self.listbox.set(4))) \
            .grid(row=3, column=0, sticky=(tk.N + tk.W))

        EnhancedButton(listbox_frame.viewport, 'Get Title', command=lambda: print(self.listbox.get_title(4))) \
            .grid(row=4, column=0, sticky=(tk.N + tk.W))

        EnhancedButton(listbox_frame.viewport, 'Get Values', command=lambda: print(self.listbox.get_values())) \
            .grid(row=5, column=0, sticky=(tk.N + tk.W))

        EnhancedButton(listbox_frame.viewport, 'Set Options', command=lambda: print(self.listbox.set_options(values))) \
            .grid(row=6, column=0, sticky=(tk.N + tk.W))


        ### Table Frame testing ###

        table_frame = ScrollFrame(self.tabs, height=500, width=500)
        self.table = None

        def cb_click_fetch(obj_id):
            print('btn_cb.fetch.id', obj_id)
            print('cb_click_fetch:', self.table.fetch(obj_id))

        def cb_click_remove(obj_id):
            print('cb_click_remove', obj_id)
            self.table.remove(obj_id)

        categories = [
            ('one', 'One'),
            ('two', 'Two'),
            ('three', 'Three'),
            ('four', 'Four'),
        ]

        headers = [
            {'key': 'id', 'text': 'ID', 'hide': False},
            {'key': 'name', 'text': 'Name'},
            {'key': 'category', 'text': 'Category', 'input_class': EnhancedCombobox, 'input_class_args': {'values': categories}, 'hide': False},
            {'key': 'id', 'button': True, 'text': 'Fetch', 'label_text': 'Fetch', 'button_command': cb_click_fetch},
            {'key': 'id', 'button': True, 'text': 'Remove', 'label_text': 'Remove', 'button_command': cb_click_remove},
        ]

        data = [
            {'id': 1, 'name': 'Orange', 'category': 'one', },
            {'id': 2, 'name': 'Blue', 'category': 'one', },
            {'id': 3, 'name': 'Green', 'category': 'two', },
            {'id': 4, 'name': 'Red', 'category': 'two', },
        ]

        data2 = deepcopy(data)
        data2.append({'id': 5, 'name': 'Yellow', 'category': 'three'})
        data2.append({'id': 6, 'name': 'Purple', 'category': 'three'})
        data2.append({'id': 7, 'name': 'white', 'category': 'three'})


        self.table = EnhancedTable(table_frame.viewport, 'id', headers=headers, data=data)
        #self.table.set_options('categories', values=categories)
        self.table.grid(row=0, column=0, sticky=(tk.N + tk.S, tk.E, tk.W))
        self.table.rowconfigure(0, weight=3)
        self.table.columnconfigure(0, weight=3)


        EnhancedButton(table_frame.viewport, 'Serialize Table', command=lambda: print(self.table.get())) \
            .grid(row=1, column=0, sticky=(tk.N + tk.W))

        EnhancedButton(table_frame.viewport, 'Update Table Data', command=lambda: self.table.set(data2)) \
            .grid(row=2, column=0, sticky=(tk.N + tk.W))




        self.new_table_entry = EnhancedEntry(table_frame.viewport, 'Input:', label_args={'width': 10})
        self.new_table_entry.grid(row=3, column=0, sticky=(tk.W + tk.N))

        def create_new_table_row():
            val = self.new_table_entry.get()
            self.table.add(
                {'id': 0, 'name': val, 'category': 'four'},
            )

        EnhancedButton(table_frame.viewport, 'Add New Record', command=create_new_table_row) \
            .grid(row=4, column=0, sticky=(tk.N + tk.W))


        self.tabs.grid(row=0, column=0, sticky=(tk.N, tk.W + tk.S + tk.E))
        self.tabs.add(entry_frame, text='Entry')
        self.tabs.add(text_frame, text='Text')
        self.tabs.add(checkbox_frame, text='Checkbox')
        self.tabs.add(scrolling_frame, text='Scrolling Frame')
        self.tabs.add(combobox_frame, text='Combobox')
        self.tabs.add(listbox_frame, text='Listbox')
        self.tabs.add(table_frame, text='Table')

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

