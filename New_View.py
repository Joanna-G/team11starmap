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
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1000)
        self.rowconfigure(0, weight=1)

        self.user_frame = UserFrame(self)
        self.star_map_frame = StarMapFrame(self)
        self.user_frame.grid(column=0, row=0, sticky='nsw')
        self.star_map_frame.grid(column=1, row=0, sticky='nsew')


class UserFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.widgets_list = []

        self.grid(column=0, row=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.background_color = '#393a3d'
        self.padx = 10
        self.pady = 10

        menu_style = ttk.Style()
        menu_style.configure('TFrame', background=self.background_color)

        self.menu_frame = ttk.Frame(self, style='TFrame')
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
        self.utc_value.set('UTC')
        self.latitude_value = StringVar()
        self.latitude_value.set('Lat')
        self.longitude_value = StringVar()
        self.longitude_value.set('Long')

        directory = ''
        if getattr(sys, 'frozen', False):
            directory = os.path.dirname(sys.executable)
        elif __file__:
            directory = os.path.dirname(__file__)
        filename = os.path.join(directory, 'resources', 'Logo_100x100.png')
        logo = ImageTk.PhotoImage(Image.open(filename))
        self.label_logo = tk.Label(self.menu_frame, image=logo, background=self.background_color)
        self.label_logo.grid(column=0, row=0, sticky='w')
        self.label_logo = logo

        self.label_title = tk.Label(self.menu_frame, text='Lumarium', background=self.background_color)
        self.label_title.grid(column=1, row=0, sticky='w')
        self.label_title.config(font=('Magneto', 22))

        # Date label, comboboxes, and daylight savings checkbox
        self.label_date = tk.Label(self.menu_frame, text='Date', background=self.background_color)
        self.label_date.grid(column=0, row=1, padx=self.padx, pady=self.pady, sticky='nsw')
        self.combobox_month = ttk.Combobox(self.menu_frame, textvariable=self.month_value, state='readonly')
        self.combobox_month.grid(column=0, row=2, sticky='nsew', padx=(self.padx,0), pady=self.pady)
        # self.combobox_month.bind('<Leave>', lambda e: self.validate_combobox(e, 'Month', 1, 12))
        self.combobox_day = ttk.Combobox(self.menu_frame, textvariable=self.day_value, state='readonly')
        self.combobox_day.grid(column=1, row=2, sticky='nsew', padx=(self.padx,0), pady=self.pady)
        self.combobox_year = ttk.Combobox(self.menu_frame, textvariable=self.year_value, state='readonly')
        self.combobox_year.grid(column=2, row=2, sticky='nsew', padx=self.padx, pady=self.pady)

        # Time label and comboboxes
        self.label_time = tk.Label(self.menu_frame, text='Date', background=self.background_color)
        self.label_time.grid(column=0, row=3, sticky='nsw', padx=self.padx, pady=self.pady)
        self.combobox_hour = ttk.Combobox(self.menu_frame, textvariable=self.hour_value, state='readonly')
        self.combobox_hour.grid(column=0, row=4, sticky='nsew', padx=(self.padx,0), pady=self.pady)
        self.combobox_minute = ttk.Combobox(self.menu_frame, textvariable=self.minute_value, state='readonly')
        self.combobox_minute.grid(column=1, row=4, sticky='nsew', padx=(self.padx,0), pady=self.pady)
        self.combobox_utc = ttk.Combobox(self.menu_frame, textvariable=self.utc_value, state='readonly')
        self.combobox_utc.grid(column=2, row=4, sticky='nsew', padx=self.padx, pady=self.pady)
        self.checkbox_daylight_savings = tk.Checkbutton(self.menu_frame, text='Daylight Savings', background=self.background_color)
        self.checkbox_daylight_savings.grid(column=0, row=5, sticky='nsw', padx=self.padx, pady=self.pady)

        # Location label and lat/lon comboboxes
        self.label_location = tk.Label(self.menu_frame, text='Location', background=self.background_color)
        self.label_location.grid(column=0, row=6, sticky='nsw', padx=self.padx, pady=self.pady)
        self.combobox_latitude = ttk.Combobox(self.menu_frame, textvariable=self.latitude_value, state='readonly')
        self.combobox_latitude.grid(column=0, row=7, sticky='nsew', padx=(self.padx,0), pady=self.pady)
        self.combobox_longitude = ttk.Combobox(self.menu_frame, textvariable=self.longitude_value, state='readonly')
        self.combobox_longitude.grid(column=1, row=7, sticky='nsew', padx=self.padx, pady=self.pady)

        # Show/Hide checkboxes and labels
        self.checkbox_show_constellations = tk.Checkbutton(self.menu_frame, text='Show Constellations', background=self.background_color)
        self.checkbox_show_constellations.grid(column=0, row=8, sticky='nsw', padx=self.padx, pady=self.pady)
        self.checkbox_show_labels = tk.Checkbutton(self.menu_frame, text='Show Labels', background=self.background_color)
        self.checkbox_show_labels.grid(column=0, row=9, sticky='nsw', padx=self.padx, pady=self.pady)

        # Generate map and reset buttons
        self.button_generate_map = tk.Button(self.menu_frame, text='Generate Map')
        self.button_generate_map.grid(column=0, row=10, sticky='nsw', padx=self.padx, pady=self.pady)
        self.button_reset = tk.Button(self.menu_frame, text='Reset')
        self.button_reset.grid(column=0, row=11, sticky='nsw', padx=self.padx, pady=self.pady)

        self.set_combobox_values(self.combobox_month, 1, 13)
        self.set_combobox_values(self.combobox_day, 1, 32)
        self.set_combobox_values(self.combobox_year, 1900, 2101)
        self.set_combobox_values(self.combobox_hour, 0, 25)
        self.set_combobox_values(self.combobox_minute, 0, 60)
        self.set_combobox_values(self.combobox_utc, -12, 15)
        self.set_combobox_values(self.combobox_latitude, -90, 91)
        self.set_combobox_values(self.combobox_longitude, -180, 181)


    def set_combobox_values(self, combobox, first, last):
        values = []
        for i in range(first, last):
            values.append(i)
        combobox['values'] = values

    # def validate_combobox(self, e, tag, lower_bound, upper_bound):
    #     pass


class StarMapFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

        self.grid(column=0, row=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.background_color = '#393a3d'
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
                           scrollregion=(-4000, -4000, 4000, 4000), background='navy') # highlightthickness=10
        self.canvas.bind('<MouseWheel>', lambda e: self.on_mouse_wheel_scrool(e))
        self.canvas.bind('<Shift-MouseWheel>', lambda e: self.on_mouse_wheel_scrool(e))

    def draw_star(self, star, x, y):
        r = 2
        x = self.canvas.create_oval(x - r, y - r, x + r, y + r)
        self.canvas.tag_bind(x, '<ButtonPress-1>', lambda e: self.display_star_info(e, star))

    def draw_constellation_line(self, star_1, star_2, constellation):
        const = self.canvas.create_line(star_1.x, star_1.y, star_2.x, star_2.y)
        self.canvas.tag_bind(const, '<ButtonPress-1>', lambda e: self.display_constellation_info(e, constellation))

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
            tk.Label(modal_dlg, text='Star Hour Angle: ' + str(object.ha_time)).grid(column=0, row=4, columnspan=3,
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





