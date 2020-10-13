import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

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
