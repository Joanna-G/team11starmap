import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
from PIL import ImageTk, Image
import os
import sys


class MainApplication(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

        self.grid(column=0, row=0, sticky='nsew')
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(1, weight=1)

        self.header_frame = HeaderFrame(self)
        self.menu_frame = MenuFrame(self)
        self.star_map_frame = StarMapFrame(self)
        self.header_frame.grid(column=0, row=0, columnspan=2)
        self.menu_frame.grid(column=0, row=1)
        self.star_map_frame.grid(column=1, row=1)

        # self.header_frame = HeaderFrame(self)
        # self.header_frame.pack(expand=True, fill='both')
        # self.menu_frame = MenuFrame(self)
        # self.menu_frame.pack(expand=True, fill='both')
        # self.star_map_frame = StarMapFrame(self)
        # self.star_map_frame.pack(expand=True, fill='both')


class HeaderFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

        self.grid(column=0, row=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.header_frame = ttk.Frame(self)
        self.header_frame.grid(column=0, row=0, sticky='nsew')
        self.header_frame.columnconfigure(0, weight=1)
        self.header_frame.columnconfigure(1, weight=1)
        self.header_frame.columnconfigure(1, weight=1)
        self.header_frame.columnconfigure(2, weight=1)
        self.header_frame.columnconfigure(3, weight=1)
        self.header_frame.columnconfigure(4, weight=1)
        self.header_frame.columnconfigure(5, weight=1)

        self.button_print = tk.Button(self.header_frame, text='Print')
        self.button_print.grid(column=0, row=0, sticky='nsew')
        self.button_save = tk.Button(self.header_frame, text='Save')
        self.button_save.grid(column=1, row=0, sticky='nsew')
        self.button_help = tk.Button(self.header_frame, text='Help')
        self.button_help.grid(column=2, row=0, sticky='nsew')
        self.button_show_hide_labels = tk.Button(self.header_frame, text='Show/Hide Labels')
        self.button_show_hide_labels.grid(column=3, row=0, columnspan=2, sticky='nsew')
        self.button_show_hide_constellations = tk.Button(self.header_frame, text='Show/Hide Constellations')
        self.button_show_hide_constellations.grid(column=5, row=0, columnspan=2, sticky='nsew')


class MenuFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

        self.widgets_list = []

        self.grid(column=0, row=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        style = ttk.Style()
        style.configure('Menu.TFrame', background='green')

        self.menu_frame = ttk.Frame(self, style='Menu.TFrame')
        self.menu_frame.grid(column=0, row=0, sticky='nsew')
        self.menu_frame.columnconfigure(0, weight=1)
        self.menu_frame.rowconfigure(0, weight=1)
        self.menu_frame.rowconfigure(1, weight=1)
        self.menu_frame.rowconfigure(2, weight=1)
        self.menu_frame.rowconfigure(3, weight=1)
        self.menu_frame.rowconfigure(4, weight=1)
        self.menu_frame.rowconfigure(5, weight=1)
        self.menu_frame.rowconfigure(6, weight=1)
        self.menu_frame.rowconfigure(7, weight=1)
        self.menu_frame.rowconfigure(8, weight=1)
        self.menu_frame.rowconfigure(9, weight=1)
        self.menu_frame.rowconfigure(10, weight=1)
        self.menu_frame.rowconfigure(11, weight=1)

        self.entryval_month = StringVar(self.parent)
        self.entryval_month.set('Month (1-12)')
        self.entryval_day = StringVar(self.parent)
        self.entryval_day.set('Day (1-31)')
        self.entryval_year = StringVar(self.parent)
        self.entryval_year.set('Year (1900-2100)')
        self.entryval_time = StringVar(self.parent)
        self.entryval_time.set('00:00 (Military Time)')
        self.optionval_timezone = StringVar(self.parent)
        self.optionval_timezone.set('Timezone')
        self.entryval_latitude = StringVar(self.parent)
        self.entryval_latitude.set('Latitude (-90-90)')
        self.entryval_longitude = StringVar(self.parent)
        self.entryval_longitude.set('Longitude (-180-180)')
        self.optionval_city = StringVar(self.parent)
        self.optionval_city.set('City')

        self.label_title = tk.Label(self.menu_frame, text='Lumarium')
        self.label_title.grid(column=0, row=0, sticky='nsew')
        self.label_title.config(font=('Magneto', 22), anchor='s', background='green')

        self.label_date_time = tk.Label(self.menu_frame, text='Date and Time')
        self.label_date_time.grid(column=0, row=1, sticky='nsew', padx=10, pady=10)
        self.label_date_time.config(anchor='sw', background='green')

        self.entry_month = tk.Entry(self.menu_frame, textvariable=self.entryval_month)
        self.entry_month.config(foreground='grey')
        self.entry_month.grid(column=0, row=2, sticky='nsew', padx=10)
        self.entry_month.bind('<FocusIn>', lambda e: self.clear_widget_text(e, 'Month'))
        self.entry_month.bind('<FocusOut>', lambda e: self.check_widget_text(e, 'Month', 'Month (1-12)'))
        self.widgets_list.append(self.entry_month)

        self.entry_day = tk.Entry(self.menu_frame, textvariable=self.entryval_day)
        self.entry_day.config(foreground='grey')
        self.entry_day.grid(column=0, row=3, sticky='nsew', padx=10, pady=10)
        self.entry_day.bind('<FocusIn>', lambda e: self.clear_widget_text(e, 'Day'))
        self.entry_day.bind('<FocusOut>', lambda e: self.check_widget_text(e, 'Day', 'Day (1-31)'))
        self.widgets_list.append(self.entry_day)

        self.entry_year = tk.Entry(self.menu_frame, textvariable=self.entryval_year)
        self.entry_year.config(foreground='grey')
        self.entry_year.grid(column=0, row=4, sticky='nsew', padx=10)
        self.entry_year.bind('<FocusIn>', lambda e: self.clear_widget_text(e, 'Year'))
        self.entry_year.bind('<FocusOut>', lambda e: self.check_widget_text(e, 'Year', 'Year (1900-2100)'))
        self.widgets_list.append(self.entry_year)

        self.entry_time = tk.Entry(self.menu_frame, textvariable=self.entryval_time)
        self.entry_time.config(foreground='grey')
        self.entry_time.grid(column=0, row=5, sticky='nsew', padx=10, pady=10)
        self.entry_time.bind('<FocusIn>', lambda e: self.clear_widget_text(e, 'Time'))
        self.entry_time.bind('<FocusOut>', lambda e: self.check_widget_text(e, 'Time', '00:00 (Military Time)'))
        self.widgets_list.append(self.entry_time)

        self.optionmenu_timezone = tk.OptionMenu(self.menu_frame, self.optionval_timezone, 'Timezone', 'Timezone One', 'Timezone Two', 'Timezone Three')
        self.optionmenu_timezone.grid(column=0, row=6, sticky='nsew', padx=10)

        self.label_location = tk.Label(self.menu_frame, text='Location')
        self.label_location.grid(column=0, row=7, sticky='nsew', padx=10, pady=10)
        self.label_location.config(anchor='sw', background='green')

        self.entry_latitude = tk.Entry(self.menu_frame, textvariable=self.entryval_latitude)
        self.entry_latitude.config(foreground='grey')
        self.entry_latitude.grid(column=0, row=8, sticky='nsew', padx=10)
        self.entry_latitude.bind('<FocusIn>', lambda e: self.clear_widget_text(e, 'Latitude'))
        self.entry_latitude.bind('<FocusOut>', lambda e: self.check_widget_text(e, 'Latitude', 'Latitude (-90-90)'))
        self.widgets_list.append(self.entry_year)

        self.entry_longitude = tk.Entry(self.menu_frame, textvariable=self.entryval_longitude)
        self.entry_longitude.config(foreground='grey')
        self.entry_longitude.grid(column=0, row=9, sticky='nsew', padx=10, pady=10)
        self.entry_longitude.bind('<FocusIn>', lambda e: self.clear_widget_text(e, 'Longitude'))
        self.entry_longitude.bind('<FocusOut>', lambda e: self.check_widget_text(e, 'Longitude', 'Longitude (-180-180)'))
        self.widgets_list.append(self.entry_year)

        self.label_or = tk.Label(self.menu_frame, text='OR')
        self.label_or.grid(column=0, row=10, sticky='nsew')
        self.label_or.config(anchor='s', background='green')
        self.optionmenu_city = tk.OptionMenu(self.menu_frame, self.optionval_city, 'City', 'City One', 'City Two', 'City Three')
        self.optionmenu_city.grid(column=0, row=11, sticky='nsew', padx=10, pady=10)

    def clear_widget_text(self, event, tag):
        widget_value = event.widget.get()
        if tag == 'Month':
            if widget_value == 'Month (1-12)':
                event.widget.delete(0, tk.END)
                event.widget.config(foreground='black')
        elif tag == 'Day':
            if widget_value == 'Day (1-31)':
                event.widget.delete(0, tk.END)
                event.widget.config(foreground='black')
        elif tag == 'Year':
            if widget_value == 'Year (1900-2100)':
                event.widget.delete(0, tk.END)
                event.widget.config(foreground='black')
        elif tag == 'Time':
            if widget_value == '00:00 (Military Time)':
                event.widget.delete(0, tk.END)
                event.widget.config(foreground='black')
        elif tag == 'Latitude':
            if widget_value == 'Latitude (-90-90)':
                event.widget.delete(0, tk.END)
                event.widget.config(foreground='black')
        elif tag == 'Longitude':
            if widget_value == 'Longitude (-180-180)':
                event.widget.delete(0, tk.END)
                event.widget.config(foreground='black')

    def check_widget_text(self, event, tag, text):
        widget_value = event.widget.get()
        if tag == 'Month':
            try:
                widget_value = int(widget_value)
            except ValueError:
                widget_value = ''
            if widget_value == '' or widget_value < 1 or widget_value > 12:
                event.widget.delete(0, tk.END)
                event.widget.config(foreground='grey')
                event.widget.insert(0, text)
        elif tag == 'Day':
            try:
                widget_value = int(widget_value)
            except ValueError:
                widget_value = ''
            if widget_value == '' or widget_value < 1 or widget_value > 31:
                event.widget.delete(0, tk.END)
                event.widget.config(foreground='grey')
                event.widget.insert(0, text)
        elif tag == 'Year':
            try:
                widget_value = int(widget_value)
            except ValueError:
                widget_value = ''
            if widget_value == '' or widget_value < 1900 or widget_value > 2100:
                event.widget.delete(0, tk.END)
                event.widget.config(foreground='grey')
                event.widget.insert(0, text)
        elif tag == 'Time':
            try:
                widget_value = int(widget_value)
            except ValueError:
                widget_value = ''
            if widget_value == '':
                event.widget.delete(0, tk.END)
                event.widget.config(foreground='grey')
                event.widget.insert(0, text)
        elif tag == 'Latitude':
            try:
                widget_value = float(widget_value)
            except ValueError:
                widget_value = ''
            if widget_value == '' or widget_value < -90 or widget_value > 90:
                event.widget.delete(0, tk.END)
                event.widget.config(foreground='grey')
                event.widget.insert(0, text)
        elif tag == 'Longitude':
            try:
                widget_value = float(widget_value)
            except ValueError:
                widget_value = ''
            if widget_value == '' or widget_value < -180 or widget_value > 180:
                event.widget.delete(0, tk.END)
                event.widget.config(foreground='grey')
                event.widget.insert(0, text)


class StarMapFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

        self.grid(column=0, row=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        style = ttk.Style()
        style.configure('StarMap.TFrame', background='black')

        self.star_map_frame = ttk.Frame(self, style='StarMap.TFrame')
        self.star_map_frame.grid(column=0, row=0, sticky='nsew')
        self.star_map_frame.columnconfigure(0, weight=1)
        self.star_map_frame.rowconfigure(0, weight=1)
        # self.star_map_frame.bind('<Configure>', self.on_resize)

        directory = ''
        if getattr(sys, 'frozen', False):
            directory = os.path.dirname(sys.executable)
        elif __file__:
            directory = os.path.dirname(__file__)
        filename = os.path.join(directory, 'resources', 'star_map_background.jpg')

        self.image = Image.open(filename)
        dimmensions = (self.star_map_frame.winfo_width(), self.star_map_frame.winfo_height())
        self.image.resize(dimmensions)
        self.converted_image = ImageTk.PhotoImage(self.image)



        # self.converted_image = ImageTk.PhotoImage(Image.open(filename))

        self.panel = tk.Label(self.star_map_frame, image=self.converted_image)
        self.panel.grid(column=0, row=0, sticky='nsew')

    #     self.button_print = tk.Button(self.star_map_frame, text='Print', command=self.print_stuff)
    #     self.button_print.config(height=1, width=100)
    #     self.button_print.grid(column=0, row=0, sticky='nsew')
    #
    # def print_stuff(self):
    #     print(self.star_map_frame.winfo_height())
    #     print(self.star_map_frame.winfo_width())
    #
    # def on_resize(self, event):
    #     print("here")


if __name__ == "__main__":
    win = tk.Tk()
    m = MainApplication(parent=win)
    m.pack(fill="both", expand=True)
    win.title("Lumarium")
    win.geometry("1100x700")
    win.mainloop()