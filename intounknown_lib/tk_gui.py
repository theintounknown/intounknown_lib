import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import re


def install_default_styles():
    s = ttk.Style()

    s.configure('TableHeader.TLabel', font=('Arial', 10, 'bold'), borderwidth=1, relief='groove', background='#e0e0e0', padding=4, padx=1, pady=1)
    s.configure('TableField.TLabel', font=('Arial',10,'normal'), background='white', padding=4, padx=1, pady=1)


# Design for id field (where we want to keep an ID associated with a table row)
class HiddenField:
    def __init__(self, value, default=None):
        self.value = value
        self.default_value = default

    def set(self, value):
        self.value = value

    def get(self):
        return self.value

    def clear(self):
        self.value = self.default_value


class EnhancedButton(tk.Frame):
    # input_args={} should be be dict
    def __init__(self, parent, txt, command, input_args=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        input_args = input_args or {}
        self.config(padx=10, pady=10)
        btn_obj = ttk.Button(self, text=txt, command=command, **input_args)
        btn_obj.grid(row=0, column=0, sticky=tk.W)



class EnhancedLabel(tk.Frame):
    def __init__(self, parent, txt, input_args=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        input_args = input_args or {}
        self.variable = tk.StringVar()
        self.variable.set(txt)
        self.label_obj = ttk.Label(self, textvariable=self.variable, **input_args)
        self.label_obj.grid(row=0, column=0, sticky=tk.W)

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.variable.set(value)

    def clear(self):
        self.set('')


class EnhancedEntry(tk.Frame):
    def __init__(self, parent, txt, value='', label_args=None, input_args=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.config(padx=10, pady=10)
        self.variable = tk.StringVar()
        self.variable.set(value)

        col = 0
        if txt != None:
            label_obj = ttk.Label(self, text=txt, **label_args)
            label_obj.grid(row=0, column=col, sticky=tk.W)
            col += 1

        self.entry_obj = ttk.Entry(self, textvariable=self.variable, **input_args)
        self.entry_obj.grid(row=0, column=col, sticky=(tk.W, tk.E))

        self.columnconfigure(1, weight=0)

    def get(self):
        return self.variable.get()

    def set(self, value):
        return self.variable.set(value)

    def clear(self):
        self.set('')

    def focus(self):
        self.entry_obj.focus()



class EnhancedText(tk.Frame):
    ''' a multiple line textarea '''
    def __init__(self, parent, txt, value='', label_args=None, input_args=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        input_args = input_args or {}       # if input_args provided
        label_args = label_args or {}       # if label_args provided
        self.config(padx=10, pady=10)       # add some default padding

        # set a default for height if not provided
        if 'height' not in input_args:
            input_args['height'] = 4
        # set a default for width if not provided
        if 'width' not in input_args:
            input_args['width'] = 20

        self.yScroll = tk.Scrollbar(self, orient=tk.VERTICAL)   # create scrollbar for textarea

        col = 0
        # if requesting a label item
        if txt != None:
            label_obj = ttk.Label(self, text=txt, **label_args)
            label_obj.grid(row=0, column=col, sticky=(tk.W + tk.N))
            col += 1

        self.entry_obj = tk.Text(self, yscrollcommand=self.yScroll.set, **input_args)
        self.yScroll['command'] = self.entry_obj.yview      # call text's yview method

        self.entry_obj.grid(row=0, column=col, sticky=(tk.W + tk.E))
        col += 1
        self.yScroll.grid(row=0, column=col, sticky=(tk.N + tk.S))
        col += 1

        self.columnconfigure(1, weight=0)       # use all available spaces for column

    def get(self):
        val = self.entry_obj.get('1.0', tk.END)     # get all text in range
        return val.strip()      # remove trailing newline

    def set(self, value):
        self.clear()        # clear all characters
        self.entry_obj.insert('1.0', value)     # insert characters at beginning of field

    def clear(self):
        self.entry_obj.delete('1.0', tk.END)    # clear all characters in range


class EnhancedCheckbox(tk.Frame):
    ''' checkbox interface component '''
    def __init__(self, parent, txt, checked=False, input_args=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        input_args = input_args or {}
        self.config(padx=10, pady=10)
        self.variable = tk.BooleanVar()
        self.variable.set(checked)

        check_obj = ttk.Checkbutton(self, text=txt, variable=self.variable, **input_args)
        check_obj.grid(row=0, column=0, columnspan=3, sticky=(tk.W + tk.E))

        self.columnconfigure(0, weight=0)

    def get(self):
        return self.variable.get()

    def set(self, value):
        return self.variable.set(value)

    def clear(self):
        self.set(False)




class ScrollFrame(tk.Frame):
    '''
    Scrolling Frame for large content
    Note: you must attach widgets to the VIEWPORT and not the ScrollFrame directly
    Example:
        sframe = ScrollFrame(my_parent)
        EnhancedLabel(sframe.viewport, 'Hello')     # note the note ".viewport"
    This was helpful figuring out events and where I found the viewport technique:
        mp035 / tk_scroll_demo.py
        https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01
    '''
    def __init__(self, parent, hide_x=False, height=None, width=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.viewport = None        # the Frame content needs to be added to (not the parent object)

        self.canvas = tk.Canvas(self, highlightthickness=0)     # render the visible of the Frame
        # Setup dimensions
        if height != None:
            self.canvas.config(height=height)
        if width != None:
            self.canvas.config(width=width)

        # vertical scrollbar attached the canvas
        self.yScroll = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        # horizontal scrollbar attached the canvas
        self.xScroll = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)

        self.viewport = tk.Frame(self.canvas, borderwidth=0)    # create frame to use as the viewport
        # configure canvas to receive commands from scrollbars
        self.canvas.configure(yscrollcommand=self.yScroll.set, xscrollcommand=self.xScroll.set)

        self.canvas.grid(row=0, column=0, sticky=(tk.W + tk.E + tk.S + tk.N))
        # create window for canvas to show frame through
        self.canvas.create_window((0, 0), window=self.viewport, anchor='nw', tags="self.viewport")

        self.yScroll.grid(row=0, column=1, sticky=(tk.N + tk.S))
        if not hide_x:
            self.xScroll.grid(row=1, column=0, sticky=(tk.E + tk.W))

        self.viewport.bind('<Configure>', self._configure_frame)


    def _configure_frame(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))





class EnhancedCombobox(tk.Frame):
    '''
        Input:
            values : [(1, 'one'), (2, 'two'), (3, 'three)]

    '''
    def __init__(self, parent, txt, values=None, default_value=None, label_args=None, input_args=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        input_args = input_args or {}
        label_args = label_args or {}
        self.config(padx=10, pady=10)

        self.values = values
        self.default_value = default_value  # the value to initialize the combobox, but it doesn't have to be in the available list

        self.variable = tk.StringVar()
        col = 0
        if txt != None:
            label_obj = ttk.Label(self, text=txt, **label_args)
            label_obj.grid(row=0, column=0, sticky=tk.W)
            col += 1

        self.combo_obj = ttk.Combobox(self, textvariable=self.variable, **input_args)
        self.set_options(values)
        self.combo_obj.grid(row=0, column=col, sticky=(tk.E + tk.W))

        self.columnconfigure(1, weight=0)       # allow to use all available space

    def set_options(self, values, refresh_selection=True):
        old_value = self.get()      # need to get the old value before updating option values (indexes will change)
        self.values = values
        values_text = [a[1] for a in values]
        self.combo_obj.config(values=values_text)

        if refresh_selection:
            self.set(old_value)

    # get the selected option value
    def get(self):
        idx = self.combo_obj.current()
        if idx < 0:
            return self.default_value
        return self.values[idx][0]


    # get selected option title
    def get_title(self, lookup=None):
        # if lookup is not supplied, use value for current index
        if lookup is None:
            idx = self.combo_obj.current()
            # idx == -1, no option selected
            if idx < 0:
                lookup = self.default_value
            else:
                lookup = self.values[idx][0]


        for obj in self.values:
            if obj[0] == lookup:
                return obj[1]
        return None


    def set(self, value):
        self.default_value = value
        idx = -1
        counter = 0
        for pair in self.values:
            lookup, name = pair

            if lookup == value:
                idx = counter
                break
            counter += 1

        if idx < 0:
            return False

        self.combo_obj.current(idx)
        return True


    def clear(self):
        self.combo_obj.set('')

    def get_values(self):
        return self.values


# TK Listbox
class EnhancedListbox(tk.Frame):
    def __init__(self, parent, txt, values=None, onchange=None, label_args=None, inputs_args=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.onchange = onchange
        input_args = inputs_args or {}
        label_args = label_args or {}
        self.config(padx=10, pady=10)

        #self.variable = tk.StringVar()
        row = 0
        if txt != None:
            label_obj = ttk.Label(self, text=txt, **label_args)
            label_obj.grid(row=row, column=0, sticky=tk.W)
            row += 1

        self.yScroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.yScroll.grid(row=row, column=1, sticky=(tk.N + tk.S))
        self.xScroll = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.xScroll.grid(row=row+1, column=0, sticky=(tk.E + tk.W))

        self.list_var = tk.StringVar()
        self.listbox = tk.Listbox(
            self,
            xscrollcommand=self.xScroll.set,
            yscrollcommand=self.yScroll.set,
            listvariable=self.list_var,
            exportselection=False,
            **input_args
        )
        self.listbox.grid(row=row, column=0, sticky=(tk.N + tk.S + tk.E + tk.W))
        self.xScroll['command'] = self.listbox.xview
        self.yScroll['command'] = self.listbox.yview

        self.listbox.bind('<<ListboxSelect>>', self.on_select)

    def on_select(self, event):
        if self.onchange != None:
            self.onchange()

    def clear(self):
        size = self.listbox.size()
        if size > 0:
            self.listbox.select_clear(0, size)

    # Values will be a [(1,'one'),(2,'two')]
    def set_options(self, values):
        self.clear()

        match_quote_re = re.compile(r'[\"]')

        self.values = values
        text_vals = []

        for row in values:
            tmp = str(row[1])
            tmp = match_quote_re.sub("'",tmp)
            text_vals.append('"'+tmp+'"')

        text_val = ' '.join(text_vals)
        self.list_var.set(text_val)
        self.listbox.see(0)

    def set(self, value):
        self.clear()

        idx = -1
        counter = 0
        for pair in self.values:
            lookup, name = pair
            if lookup == value:
                idx = counter
                break
            counter += 1

        if idx < 0:
            return False

        self.listbox.selection_set(idx)
        return True

    def get(self):
        result = []
        indexes = self.listbox.curselection()
        for idx in indexes:
            result.append(self.values[idx][0])

        if len(result) < 1:
            return None
        elif len(result) == 1:
            return result[0]

        return result

    def get_title(self, lookup):
        for obj in self.values:
            if obj[0] == lookup:
                return obj[1]
        return None

    def get_values(self):
        return self.values



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

        # Track the max id insert into table to increment for the added row
        for obj in data:
            val = obj.get(self.id_field, 0)
            if not isinstance(val, int):
                continue
            self.last_id = max(self.last_id, val)

        self.initialize_data(data)

    def get(self):
        return self._collect_form()

    def set(self, data):
        return self.set_data(data)

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
        # this will require that at least one row remains in the table
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
        #print('last_id:', self.last_id)
        if self.id_field not in row or row[self.id_field] == 0:
            result = self._collect_form()

            self.last_id += 1
            row[self.id_field] = self.last_id
            result.append(row)
            self.set_data(result)
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
            ttk.Label(self.frame, text=title, style='TableHeader.TLabel').grid(row=0, column=col, sticky=(tk.N + tk.W + tk.E + tk.S))
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
