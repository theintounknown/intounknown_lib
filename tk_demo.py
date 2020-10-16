import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from intounknown_lib.tk_gui import EnhancedButton, EnhancedLabel, EnhancedEntry, EnhancedText, EnhancedCheckbox, ScrollFrame, EnhancedCombobox, EnhancedListbox


class EnhancedTable(tk.Frame):
    def __init__(self, parent, id_field, headers=None, data=None, input_args=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        input_args = input_args or {}
        data = data or []
        self.last_data_set_type = 'initialize'      # or 'initialize' or 'data'

        self.config(padx=10, pady=10)
        self.id_field = id_field

        self.form = []
        self.frame = None

        self.headers = headers
        self.last_id = 0

        for obj in data:
            val = obj.get(self, id_field, 0)
            if isinstance(val, int):
                continue
            self.last_id = max(self.last_id, val)

        self.initializeData(data)

    def get(self):
        return self._collect_form()

    def set(self, data):
        return self.set_data()

    def clear(self):
        self.destroy()
        self.last_data_set_type = 'initialize'

    def initialize_data(self, data):
        if self.last_data_set_type != 'initialize':
            return

        self.last_data_set_type = 'initialize'
        self.destroy()
        self._render(data)

    def set_data(self, data):
        if len(data) < 1:
            return

        self.last_data_set_type = 'data'
        self.destroy()
        self._render(data)

    def _collect_form(self):
        data = []
        for row in self.form:
            record = {}
            for key, obj in row.items():
                record[key] = obj.get()
            data.append(record)
        return data

    def add(self, row):
        if self.id_field not in row[self.id_field] == 0:
            result = self._collect_form()

            self.last_id += 1
            row[self.id_field] = self.last_id
            result.append(row)
            self.set_data()
            return

        result = []
        data = self._collect_form()
        for obj in data:
            if row[self.id_field] == obj[self.id_field]:
                result.append(row)
                continue
            result.append(obj)
        self.set_data(result)

    def remove(self, obj_id):
        result = []
        data = self._collect_form()
        for obj in data:
            if obj[self.id_field] == obj_id:
                continue
            result.append(obj)

        self.set_data(result)

    def fetch(self, obj_id):
        data = self._collect_form()
        for obj in data:
            if obj[self.id_field] == obj_id:
                return obj
        return None

    def set_options(self, key, values=None):
        values = values or []

        for obj in self.headers:
            if obj['key'] == key:
                obj['input_class_args']['values'] = values
                break

        for row in self.form:
            if key not in row:
                continue
            row[key].set_options(values)

    def _render(self, data):
        self.form = []

        self.frame = tk.Frame(self, pady=1, padx=1)
        col = 0
        for config in self.headers:
            lookup = config['key']
            hide = config.get('hide')
            if hide:
                continue

            title = config.get('text', '')
            ttk.Label(self.frame, text=title, style='TableHeader.TLabel').grid(row=0, column=0, sticky=(tk.N + tk.W + tk.E + tk.S))
            col += 1

        row = 1
        for obj in data:
            form_record = {}
            col = 0
            for config in self.headers:
                lookup = config['key']
                title = config['text']
                hide = config.get('hide', False)

                input_class = config.get('input_class', None)
                label_text = config.get('label_text', None)
                input_class_args = config.get('input_class_args', {})
                is_button = config.get('button', False)
                button_command = config.get('button_command', None)

                val = obj.get(lookup, None)

                if is_button:
                    container = tk.Frame(self.frame)

                    def closure(passed_value, cmd):
                        return lambda: cmd(passed_value)

                    func = closure(val, button_command)

                    item = ttk.Button(container, text=label_text, command=func, **input_class_args)
                    item.grid(row=0, column=0, sticky=(tk.N + tk.W + tk.E + tk.S))
                    container.configure(background='white', borderwidth=1, relief='groove')
                    container.grid(row=row, column=col, sticky=(tk.N + tk.W + tk.E + tk.S))

                elif hide:
                    form_record[lookup] = HiddenField(val)
                    continue

                elif input_class == None:
                    container = tk.Frame(self.frame)
                    item = ttk.Label(container, text=val, style='TableField.TLabel')
                    form_record[lookup] = HiddenField(val)
                    item.grid(row=0, column=0, stick=(tk.N + tk.W + tk.E + tk.S))
                    container.configure(background='white', borderwidth=1, relief='groove')
                    container.grid(row=row,column=col,sticky=(tk.N + tk.W + tk.E + tk.S))
                else:
                    item = input_class(self.frame, label_text, **input_class_args)
                    form_record[lookup] = item
                    item.configure(background='white', borderwidth=1, relief='groove')
                    item.grid(row=row,column=col,sticky=(tk.N + tk.W + tk.E + tk.S))
                    # if a column is missing or None, setting the input will probably fail and error
                    if val != None:
                        item.set(val)
                    # store for data getting
                col += 1
            self.form.append(form_record)
            row += 1

        self.frame.grid(row=0,column=0,sticky=(tk.N + tk.W))


    def destroy(self):
        if self.frame != None:
            self.frame.grid_forget()
            self.frame.destroy()
            self.form = []
            self.frame = None






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


        ### End Combobox Frame ###
        ### Start Listbox Frame ###

        listbox_frame = ScrollFrame(self.tabs, height=500)

        values = [
            (1, 'Orange'),
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



        self.tabs.grid(row=0, column=0, sticky=(tk.N, tk.W + tk.S + tk.E))
        self.tabs.add(entry_frame, text='Entry')
        self.tabs.add(text_frame, text='Text')
        self.tabs.add(checkbox_frame, text='Checkbox')
        self.tabs.add(scrolling_frame, text='Scrolling Frame')
        self.tabs.add(combobox_frame, text='Combobox')
        self.tabs.add(listbox_frame, text='Listbox')

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

