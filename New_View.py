import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
from tkinter import Canvas
from PIL import ImageTk, Image, ImageDraw
from tkinter.filedialog import asksaveasfilename
import locale
from Celestial_Objects import *
import ghostscript
import os
import sys

class MainApplication(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

        self.grid(column=0, row=0, sticky='nsew')
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)

        self.user_frame = UserFrame(self)
        self.star_map_frame = StarMapFrame(self)
        self.user_frame.grid(column=0, row=0, sticky='nsew')
        self.star_map_frame.grid(column=1, row=0, sticky='nsew')


class UserFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.validation_widgets = []

        self.grid(column=0, row=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.menu_color = '#262626'
        self.text_color = '#ccb144'

        self.background_color = '#404040'
        self.padx = 10
        self.pady = 10

        menu_style = ttk.Style()
        menu_style.configure('TFrame', background=self.background_color)

        combostyle = ttk.Style()

        combostyle.theme_create('combostyle', parent='alt',
                                settings={'TCombobox':
                                              {'configure':
                                                   {'selectbackground': '#3a3d72',
                                                    'fieldbackground': self.background_color,
                                                    'background': 'grey',
                                                    'bordercolor': 'black',
                                                    'foreground': self.text_color,
                                                    'padding': 8,
                                                    }}}
                                )
        # ATTENTION: this applies the new style 'combostyle' to all ttk.Combobox
        combostyle.theme_use('combostyle')

        self.menu_frame = ttk.Frame(self, style='TFrame')
        self.menu_frame.grid(column=0, row=0, sticky='nsew')
        self.menu_frame.grid_propagate(False)
        self.menu_frame.columnconfigure(0, weight=1)
        self.menu_frame.columnconfigure(1, weight=1)
        self.menu_frame.columnconfigure(2, weight=1)
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

        self.month_value = StringVar()
        self.month_value.set('Month')
        self.day_value = StringVar()
        self.day_value.set('Day')
        self.year_value = StringVar()
        self.year_value.set('Year')
        self.hour_value = StringVar()
        self.hour_value.set('Hour')
        self.minute_value = StringVar()
        self.minute_value.set('Minute')
        self.utc_value = StringVar()
        self.utc_value.set('UTC Offset')
        self.daylight_savings_value = tk.IntVar()
        self.latitude_value = StringVar()
        self.latitude_value.set('Lat')
        self.longitude_value = StringVar()
        self.longitude_value.set('Long')
        self.constellations_value = tk.IntVar()
        self.labels_value = tk.IntVar()

        directory = ''
        if getattr(sys, 'frozen', False):
            directory = os.path.dirname(sys.executable)
        elif __file__:
            directory = os.path.dirname(__file__)
        filename = os.path.join(directory, 'resources', 'Logo_100x100.png')
        logo = ImageTk.PhotoImage(Image.open(filename))
        self.label_logo = tk.Label(self.menu_frame, image=logo, background=self.menu_color)
        self.label_logo.grid(column=0, row=0, sticky='w')
        self.label_logo = logo

        self.label_title = tk.Label(self.menu_frame, text='Lumarium', background=self.menu_color, foreground=self.text_color)
        self.label_title.grid(column=1, row=0, sticky='w')
        self.label_title.config(font=('Magneto', 22))

        # Date label, comboboxes, and daylight savings checkbox
        self.label_date = tk.Label(self.menu_frame, text='Date:', background=self.menu_color, foreground=self.text_color)
        self.label_date.grid(column=0, row=1, padx=self.padx, pady=self.pady, sticky='nsw')
        self.label_date.config(font=('Magneto', 18))
        self.combobox_month = ttk.Combobox(self.menu_frame, textvariable=self.month_value, state='normal')
        self.combobox_month.grid(column=0, row=2, sticky='nsew', padx=(self.padx,0), pady=self.pady)
        self.combobox_month.bind('<FocusIn>', lambda e: self.validate_combobox(self.combobox_month, e))
        self.combobox_month.bind('<FocusOut>', lambda e: self.validate_combobox(self.combobox_month, e))
        self.combobox_month.var = self.month_value
        self.combobox_month.range = (1, 12)
        self.validation_widgets.append(self.combobox_month)
        self.combobox_day = ttk.Combobox(self.menu_frame, textvariable=self.day_value, state='normal')
        self.combobox_day.grid(column=1, row=2, sticky='nsew', padx=(self.padx,0), pady=self.pady)
        self.combobox_day.bind('<FocusIn>', lambda e: self.validate_combobox(self.combobox_day, e))
        self.combobox_day.bind('<FocusOut>', lambda e: self.validate_combobox(self.combobox_day, e))
        self.combobox_day.var = self.day_value
        self.combobox_day.range = (1, 31)
        self.validation_widgets.append(self.combobox_day)
        self.combobox_year = ttk.Combobox(self.menu_frame, textvariable=self.year_value, state='normal')
        self.combobox_year.grid(column=2, row=2, sticky='nsew', padx=self.padx, pady=self.pady)
        self.combobox_year.bind('<FocusIn>', lambda e: self.validate_combobox(self.combobox_year, e))
        self.combobox_year.bind('<FocusOut>', lambda e: self.validate_combobox(self.combobox_year, e))
        self.combobox_year.var = self.year_value
        self.combobox_year.range = (1900, 2100)
        self.validation_widgets.append(self.combobox_year)

        # Time label and comboboxes
        self.label_time = tk.Label(self.menu_frame, text='Time:', background=self.menu_color, foreground=self.text_color)
        self.label_time.grid(column=0, row=3, sticky='nsw', padx=self.padx, pady=self.pady)
        self.label_time.config(font=('Magneto', 18))
        self.combobox_hour = ttk.Combobox(self.menu_frame, textvariable=self.hour_value, state='normal')
        self.combobox_hour.grid(column=0, row=4, sticky='nsew', padx=(self.padx,0), pady=self.pady)
        self.combobox_hour.bind('<FocusIn>', lambda e: self.validate_combobox(self.combobox_hour, e))
        self.combobox_hour.bind('<FocusOut>', lambda e: self.validate_combobox(self.combobox_hour, e))
        self.combobox_hour.var = self.hour_value
        self.combobox_hour.range = (0, 23)
        self.validation_widgets.append(self.combobox_hour)
        self.combobox_minute = ttk.Combobox(self.menu_frame, textvariable=self.minute_value, state='normal')
        self.combobox_minute.grid(column=1, row=4, sticky='nsew', padx=(self.padx,0), pady=self.pady)
        self.combobox_minute.bind('<FocusIn>', lambda e: self.validate_combobox(self.combobox_minute, e))
        self.combobox_minute.bind('<FocusOut>', lambda e: self.validate_combobox(self.combobox_minute, e))
        self.combobox_minute.var = self.minute_value
        self.combobox_minute.range = (0, 59)
        self.validation_widgets.append(self.combobox_minute)
        self.combobox_utc = ttk.Combobox(self.menu_frame, textvariable=self.utc_value, state='normal')
        self.combobox_utc.grid(column=2, row=4, sticky='nsew', padx=self.padx, pady=self.pady)
        self.combobox_utc.bind('<FocusIn>', lambda e: self.validate_combobox(self.combobox_utc, e))
        self.combobox_utc.bind('<FocusOut>', lambda e: self.validate_combobox(self.combobox_utc, e))
        self.combobox_utc.var = self.utc_value
        self.combobox_utc.range = (-12, 14)
        self.validation_widgets.append(self.combobox_utc)

        self.checkbox_daylight_savings = tk.Checkbutton(self.menu_frame, text='Daylight Savings', background=self.menu_color, foreground=self.text_color, variable=self.daylight_savings_value)
        self.checkbox_daylight_savings.grid(column=0, row=5, sticky='nsw', padx=self.padx, pady=self.pady)

        # Location label and lat/lon comboboxes
        self.label_location = tk.Label(self.menu_frame, text='Location:', background=self.menu_color, foreground=self.text_color)
        self.label_location.grid(column=0, row=6, sticky='nsw', padx=self.padx, pady=self.pady)
        self.label_location.config(font=('Magneto', 18))
        self.combobox_latitude = ttk.Combobox(self.menu_frame, textvariable=self.latitude_value, state='normal')
        self.combobox_latitude.grid(column=0, row=7, sticky='nsew', padx=(self.padx,0), pady=self.pady)
        self.combobox_latitude.bind('<FocusIn>', lambda e: self.validate_combobox(self.combobox_latitude, e))
        self.combobox_latitude.bind('<FocusOut>', lambda e: self.validate_combobox(self.combobox_latitude, e))
        self.combobox_latitude.var = self.latitude_value
        self.combobox_latitude.range = (-90, 90)
        self.validation_widgets.append(self.combobox_latitude)
        self.combobox_longitude = ttk.Combobox(self.menu_frame, textvariable=self.longitude_value, state='normal')
        self.combobox_longitude.grid(column=1, row=7, sticky='nsew', padx=self.padx, pady=self.pady)
        self.combobox_longitude.bind('<FocusIn>', lambda e: self.validate_combobox(self.combobox_longitude, e))
        self.combobox_longitude.bind('<FocusOut>', lambda e: self.validate_combobox(self.combobox_longitude, e))
        self.combobox_longitude.var = self.longitude_value
        self.combobox_longitude.range = (-180, 180)
        self.validation_widgets.append(self.combobox_longitude)

        # Show/Hide checkboxes and labels
        self.checkbox_show_constellations = tk.Checkbutton(self.menu_frame, text='Show Constellations', background=self.menu_color, variable=self.constellations_value, foreground=self.text_color)
        self.checkbox_show_constellations.grid(column=0, row=8, sticky='nsw', padx=self.padx, pady=self.pady)
        self.checkbox_show_labels = tk.Checkbutton(self.menu_frame, text='Show Labels', background=self.menu_color, variable=self.labels_value, foreground=self.text_color)
        self.checkbox_show_labels.grid(column=0, row=9, sticky='nsw', padx=self.padx, pady=self.pady)

        # Generate map and reset buttons
        self.button_generate_map = tk.Button(self.menu_frame, text='Generate Map')
        self.button_generate_map.grid(column=0, row=10, sticky='nsw', padx=self.padx, pady=self.pady)
        self.button_generate_map.config(background='#404040', foreground='#ccb144', highlightbackground='black', width=20)
        self.button_reset = tk.Button(self.menu_frame, text='Reset')
        self.button_reset.grid(column=1, row=10, sticky='nsw', padx=self.padx, pady=self.pady)
        self.button_reset.config(background='#404040', foreground='#ccb144', highlightbackground='black', width=10)

        self.set_combobox_values(self.combobox_month, 'Month', 1, 13)
        self.set_combobox_values(self.combobox_day, 'Day', 1, 32)
        self.set_combobox_values(self.combobox_year, 'Year', 1900, 2101)
        self.set_combobox_values(self.combobox_hour, 'Hour', 0, 25)
        self.set_combobox_values(self.combobox_minute, 'Minute', 0, 60)
        self.set_combobox_values(self.combobox_utc, 'UTC Offset', -12, 15)
        self.set_combobox_values(self.combobox_latitude, 'Lat', -90, 91)
        self.set_combobox_values(self.combobox_longitude, 'Long', -180, 181)


    def set_combobox_values(self, combobox, default, first, last):
        combobox.set(default)
        values = []
        values.append(default)
        for i in range(first, last):
            values.append(i)
        combobox['values'] = values
        combobox.values = values

    def validate_combobox(self, combobox, e=None):
        try:
            value = float(combobox.var.get())
        except ValueError:
            value = combobox.var.get()
            if value == combobox.values[0]:
                combobox.set('')
            else:
                combobox.set(combobox.values[0])
            return False
        if combobox.range[0] <= value <= combobox.range[1]:
            return True
        else:
            combobox.set(combobox.values[0])
            return False

class StarMapFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

        self.grid(column=0, row=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.background_color = '#262626'
        frame_style = ttk.Style()
        frame_style.configure('TFrame', background=self.background_color)

        self.star_map_frame = ttk.Frame(self, style='TFrame')
        self.star_map_frame.grid(column=0, row=0, sticky='nsew')
        self.star_map_frame.columnconfigure(0, weight=1)
        self.star_map_frame.rowconfigure(0, weight=1)

        self.canvas = Canvas(self.star_map_frame)
        self.canvas.grid(column=0, row=0, sticky='nsew')
        self.vsb_canvas = tk.Scrollbar(self.star_map_frame, orient=tk.VERTICAL)
        self.vsb_canvas.grid(column=1, row=0, sticky='ns')
        self.vsb_canvas.config(command=self.canvas.yview)
        self.hsb_canvas = tk.Scrollbar(self.star_map_frame, orient=tk.HORIZONTAL)
        self.hsb_canvas.grid(column=0, row=1, sticky='ew')
        self.hsb_canvas.config(command=self.canvas.xview)
        self.canvas.config(xscrollcommand=self.hsb_canvas.set, yscrollcommand=self.vsb_canvas.set,
                           scrollregion=(-4000, -4000, 4000, 4000), background='black', highlightbackground='black') # highlightthickness=10
        self.canvas.bind('<MouseWheel>', lambda e: self.on_mouse_wheel_scrool(e))
        self.canvas.bind('<Shift-MouseWheel>', lambda e: self.on_mouse_wheel_scrool(e))

    def draw_star(self, star, x, y):
        if star.magnitude <= 1.0:
            r = 4
        elif star.magnitude <= 2.0:
            r = 3.5
        elif star.magnitude <= 3.0:
            r = 3
        elif star.magnitude <= 4.0:
            r = 2.5
        elif star.magnitude <= 5.0:
            r = 2
        elif star.magnitude <= 6.0:
            r = 1.5
        else:
            r = 1
        x = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='#ccb144', outline='#ccb144')
        self.canvas.tag_bind(x, '<ButtonPress-1>', lambda e: self.display_star_info(e, star))

    def draw_constellation_line(self, star_1, star_2, constellation):
        const = self.canvas.create_line(star_1.x, star_1.y, star_2.x, star_2.y, fill='#ccb144')
        self.canvas.tag_bind(const, '<ButtonPress-1>', lambda e: self.display_constellation_info(e, constellation))
        return const

    def display_star_info(self, e, star):
        x = self.parent.parent.winfo_pointerx()
        y = self.parent.parent.winfo_pointery()
        self.create_modal_dialog(star, x, y)

    def display_constellation_info(self, e, constellation):
        x = self.parent.parent.winfo_pointerx()
        y = self.parent.parent.winfo_pointery()
        self.create_modal_dialog(constellation, x, y)

    def create_modal_dialog(self, object, x, y):
        modal_dlg = tk.Toplevel(master=self)
        modal_dlg.columnconfigure(0, weight=1)
        modal_dlg.columnconfigure(1, weight=1)
        modal_dlg.columnconfigure(2, weight=1)
        modal_dlg.resizable(False, False)

        if isinstance(object, Star):
            tk.Label(modal_dlg, text='Star HD ID: ' + str(object.hd_id)).grid(column=0, row=0, columnspan=3,
                                                                              sticky='nsew')
            tk.Label(modal_dlg, text='Star Alt: ' + str(object.altitude)).grid(column=0, row=1, columnspan=3,
                                                                               sticky='nsew')
            tk.Label(modal_dlg, text='Star Azi: ' + str(object.azimuth)).grid(column=0, row=2, columnspan=3,
                                                                              sticky='nsew')
            tk.Label(modal_dlg, text='Star Magnitude: ' + str(object.magnitude)).grid(column=0, row=4, columnspan=3,
                                                                                     sticky='nsew')

        elif isinstance(object, Constellation):
            tk.Label(modal_dlg, text='Constellation Name: ' + str(object.name)).grid(column=0, row=0, columnspan=3,
                                                                                     sticky='nsew')

        modal_dlg.geometry('+%d+%d' % (x, y))
        modal_dlg.transient(self.parent)
        modal_dlg.focus_set()
        modal_dlg.grab_set()
        self.wait_window(modal_dlg)

    # Save the current canvas as a jpeg
    def save_canvas(self):
        save_file = asksaveasfilename(filetypes=[('', '.jpeg')], defaultextension='*.jpeg')
        self.canvas.update()
        self.canvas.postscript(file='canvas.ps', x=-4000, y=-4000, width=8000, height=8000)

        if save_file != '':
            args = [
                "ps2jpg",
                "-dSAFER", "-dBATCH", "-dNOPAUSE",
                "-sDEVICE=jpeg",
                "-dEPSCrop",
                "-r300",
                "-sOutputFile=" + save_file,
                "canvas.ps"
            ]
            encoding = locale.getpreferredencoding()
            args = [a.encode(encoding) for a in args]
            ghostscript.Ghostscript(*args)

    def on_mouse_wheel_scrool(self, e):
        if e.state == 8:
            self.canvas.yview_scroll(int(-1 * (e.delta / abs(e.delta))), 'units')
        elif e.state == 9:
            self.canvas.xview_scroll(int(-1 * (e.delta / abs(e.delta))), 'units')





