import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
from tkinter import Canvas
from PIL import ImageTk, Image, ImageDraw
from tkinter.filedialog import asksaveasfilename
import locale
from Celestial_Objects import *
#import ghostscript
import os
import sys


class MainApplication(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

        self.grid(column=0, row=0, sticky='nsew')
        self.columnconfigure(0, weight=1, minsize=360)
        self.columnconfigure(1, weight=2000)
        self.rowconfigure(0, weight=1)

        self.user_frame = UserFrame(self)
        self.star_map_frame = StarMapFrame(self)
        self.user_frame.grid(column=0, row=0, sticky='nsew')
        self.star_map_frame.grid(column=1, row=0, sticky='nsew')

    # I stole this code from below, no idea if this is actually how this should work.
    def create_error_dialog(self, error_message):
        modal_dlg = tk.Toplevel(master=self)
        modal_dlg.columnconfigure(0, weight=1)
        modal_dlg.resizable(False, False)

        tk.Label(modal_dlg, text=error_message).grid(column=0, row=0, columnspan=3, sticky='nw')

        # Don't know what this does or what it should be set to
        modal_dlg.geometry('+%d+%d' % (0, 0))
        modal_dlg.transient(self.parent)
        modal_dlg.focus_set()
        modal_dlg.grab_set()
        self.wait_window(modal_dlg)

    def display_help(self):
        pass


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
        self.padx = 8
        self.pady = 8

        # Set Label font based on platform
        if sys.platform == "win32" or sys.platform == "win64":
            self.font = 'Magneto'
            self.size = 18
        elif sys.platform == "darwin":
            self.font = 'Brush Script MT'
            self.size = 36
        elif sys.platform == "linux" or sys.platform == "linux2":
            self.font = 'URW Chancery L'
            self.size = 18

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
                                                    'padding': (8, 1),
                                                    }}}
                                )

        # ATTENTION: this applies the new style 'combostyle' to all ttk.Combobox
        combostyle.theme_use('combostyle')

        self.menu_frame = ttk.Frame(self, style='TFrame', border=3, relief='groove')
        self.menu_frame.grid(column=0, row=0, sticky='nsew')
        self.menu_frame.grid_propagate(False)
        self.menu_frame.columnconfigure(0, weight=1, minsize=125)
        self.menu_frame.columnconfigure(1, weight=1, minsize=90)
        self.menu_frame.columnconfigure(2, weight=1, minsize=125)
        self.menu_frame.rowconfigure(0, weight=0)               # Logo
        self.menu_frame.rowconfigure(1, weight=4)               # Date Label
        self.menu_frame.rowconfigure(2, weight=8, minsize=50)   # Date Comboboxes
        self.menu_frame.rowconfigure(3, weight=4)               # Time Label
        self.menu_frame.rowconfigure(4, weight=8, minsize=50)   # Time Comboboxes
        self.menu_frame.rowconfigure(5, weight=1, minsize=40)   # Daylight Savings Checkbox
        self.menu_frame.rowconfigure(6, weight=4)               # Location Label
        self.menu_frame.rowconfigure(7, weight=8, minsize=50)   # Location Comboboxes
        self.menu_frame.rowconfigure(8, weight=1, minsize=40)   # Show Constellations Checkbox
        self.menu_frame.rowconfigure(9, weight=1, minsize=40)   # Show Labels Checkbox
        self.menu_frame.rowconfigure(10, weight=8, minsize=40)  # Generate/Reset Buttons
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
        filename = os.path.join(directory, 'resources', 'Logo_L2.jpg')
        logo = ImageTk.PhotoImage(Image.open(filename))
        self.label_logo = tk.Label(self.menu_frame, image=logo, background=self.menu_color)
        self.label_logo.grid(column=0, row=0, sticky='w', columnspan=3)
        self.label_logo = logo

        # Date label, comboboxes, and daylight savings checkbox
        self.label_date = tk.Label(self.menu_frame, text='Date:', background=self.menu_color,
                                   foreground=self.text_color)
        self.label_date.grid(column=0, row=1, columnspan=3, padx=self.padx, pady=self.pady, sticky='nsw')
        self.label_date.config(font=(self.font, self.size))

        self.combobox_month = ttk.Combobox(self.menu_frame, textvariable=self.month_value, state='normal')
        self.combobox_month.grid(column=0, row=2, sticky='nsew', padx=(self.padx, 0), pady=self.pady)
        self.combobox_month.bind('<FocusIn>', lambda e: self.validate_combobox(self.combobox_month, e))
        self.combobox_month.bind('<FocusOut>', lambda e: self.validate_combobox(self.combobox_month, e))
        self.combobox_month.var = self.month_value
        self.combobox_month.range = (1, 12)
        self.validation_widgets.append(self.combobox_month)

        self.combobox_day = ttk.Combobox(self.menu_frame, textvariable=self.day_value, state='normal')
        self.combobox_day.grid(column=1, row=2, sticky='nsew', padx=(self.padx, 0), pady=self.pady)
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
        self.label_time = tk.Label(self.menu_frame, text='Time:', background=self.menu_color,
                                   foreground=self.text_color)
        self.label_time.grid(column=0, row=3, columnspan=3, sticky='nsw', padx=self.padx, pady=self.pady)
        self.label_time.config(font=(self.font, self.size))

        self.combobox_hour = ttk.Combobox(self.menu_frame, textvariable=self.hour_value, state='normal')
        self.combobox_hour.grid(column=0, row=4, sticky='nsew', padx=(self.padx, 0), pady=self.pady)
        self.combobox_hour.bind('<FocusIn>', lambda e: self.validate_combobox(self.combobox_hour, e))
        self.combobox_hour.bind('<FocusOut>', lambda e: self.validate_combobox(self.combobox_hour, e))
        self.combobox_hour.var = self.hour_value
        self.combobox_hour.range = (0, 23)
        self.validation_widgets.append(self.combobox_hour)
        self.combobox_minute = ttk.Combobox(self.menu_frame, textvariable=self.minute_value, state='normal')
        self.combobox_minute.grid(column=1, row=4, sticky='nsew', padx=(self.padx, 0), pady=self.pady)
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

        self.checkbox_daylight_savings = tk.Checkbutton(self.menu_frame, text='Daylight Savings',
                                                        background=self.menu_color, foreground=self.text_color,
                                                        variable=self.daylight_savings_value)
        self.checkbox_daylight_savings.grid(column=0, row=5, sticky='nsw', columnspan=3, padx=self.padx, pady=self.pady)

        # Location label and lat/lon comboboxes
        self.label_location = tk.Label(self.menu_frame, text='Location:', background=self.menu_color,
                                       foreground=self.text_color)
        self.label_location.grid(column=0, row=6, columnspan=3, sticky='nsw', padx=self.padx, pady=self.pady)
        self.label_location.config(font=(self.font, self.size))

        self.combobox_latitude = ttk.Combobox(self.menu_frame, textvariable=self.latitude_value, state='normal')
        self.combobox_latitude.grid(column=0, row=7, sticky='nsew', padx=(self.padx, 0), pady=self.pady)
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
        self.checkbox_show_constellations = tk.Checkbutton(self.menu_frame, text='Show Constellations',
                                                           background=self.menu_color,
                                                           variable=self.constellations_value,
                                                           foreground=self.text_color)
        self.checkbox_show_constellations.grid(column=0, row=8, sticky='nsw', columnspan=3, padx=self.padx,
                                               pady=self.pady)
        self.checkbox_show_labels = tk.Checkbutton(self.menu_frame, text='Show Labels', background=self.menu_color,
                                                   variable=self.labels_value, foreground=self.text_color)
        self.checkbox_show_labels.grid(column=0, row=9, sticky='nsw', columnspan=3, padx=self.padx, pady=self.pady)

        # Generate map and reset buttons
        self.button_generate_map = tk.Button(self.menu_frame, text='Generate Map')
        self.button_generate_map.grid(column=0, row=10, sticky='nsw', padx=self.padx, pady=self.pady)
        self.button_generate_map.config(background='white', foreground='black', highlightbackground='#262626', width=20)
        self.button_reset = tk.Button(self.menu_frame, text='Reset')
        self.button_reset.grid(column=1, row=10, sticky='nsw', padx=self.padx, pady=self.pady)
        self.button_reset.config(background='white', foreground='black', highlightbackground='#262626', width=10)

        # The real deal
        # self.set_combobox_values(self.combobox_month, 'Month', 1, 13)
        # self.set_combobox_values(self.combobox_day, 'Day', 1, 32)
        # self.set_combobox_values(self.combobox_year, 'Year', 1900, 2101)
        # self.set_combobox_values(self.combobox_hour, 'Hour', 0, 25)
        # self.set_combobox_values(self.combobox_minute, 'Minute', 0, 60)
        # self.set_combobox_values(self.combobox_utc, 'UTC Offset', -12, 15)
        # self.set_combobox_values(self.combobox_latitude, 'Lat', -90, 91)
        # self.set_combobox_values(self.combobox_longitude, 'Long', -180, 181)

        # Default values for testing purpose. April 10, 2018 8:30 AM, offset -6, 34.7 lat, 86.6 long
        self.set_combobox_values(self.combobox_month, 4, 1, 13)
        self.set_combobox_values(self.combobox_day, 22, 1, 32)
        self.set_combobox_values(self.combobox_year, 1985, 1900, 2101)
        self.set_combobox_values(self.combobox_hour, 18, 0, 25)
        self.set_combobox_values(self.combobox_minute, 30, 0, 60)
        self.set_combobox_values(self.combobox_utc, -6, -12, 15)
        self.set_combobox_values(self.combobox_latitude, 34.7, -90, 91)
        self.set_combobox_values(self.combobox_longitude, 86.6, -180, 181)

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

        self.multiplier = 1

        self.grid(column=0, row=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.label_widgets = []
        self.constellation_lines = []

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
                           scrollregion=(-4000, -4000, 4000, 4000), background='black', highlightbackground='black')

        # Click map, and move mouse to scroll
        self.canvas.bind("<ButtonPress-1>", self.scroll_start)
        self.canvas.bind("<B1-Motion>", self.scroll_move)


    def reset_values(self):
        self.multiplier = 1
        self.label_widgets.clear()
        self.constellation_lines.clear()

    def draw_background(self):
        # Draw a black rectangle for saving map purposes
        self.canvas.create_rectangle(-4000, -4000, 4000, 4000, fill='black', outline='black')

    # Canvas Movement Functions
    def scroll_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def draw_star(self, star, x, y):
        if star.magnitude <= 1.0:
            r = 5.5
        elif star.magnitude <= 2.0:
            r = 4.5
        elif star.magnitude <= 3.0:
            r = 3.5
        elif star.magnitude <= 4.0:
            r = 2.5
        elif star.magnitude <= 5.0:
            r = 1.5
        elif star.magnitude <= 6.0:
            r = 0.5
        else:
            r = 0
        star.canvas_id = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='#F6DC83', outline='#F6DC83')

        canvas_coords = self.canvas.coords(star.canvas_id)
        star.canvas_x = canvas_coords[0]
        star.canvas_y = canvas_coords[1]

        self.canvas.tag_bind(star.canvas_id, '<ButtonPress-1>', lambda e: self.display_star_info(e, star))

    def draw_constellation_line(self, star_1, star_2):
        const = self.canvas.create_line(star_1.canvas_x, star_1.canvas_y, star_2.canvas_x, star_2.canvas_y, fill='pink')

        # Redraw stars on top of constellation lines. Breaks with zooming because it
        # redraws stars that shouldn't be there.
        # self.draw_star(star_1, star_1.x, star_1.y)
        # self.draw_star(star_2, star_2.x, star_2.y)

        # Don't need to be able to click on constellations to see names. - Jo
        # self.canvas.tag_bind(const, '<ButtonPress-1>', lambda e: self.display_constellation_info(e, constellation))

        return const

    def draw_constellation(self, const, star_list):
        for index in const.line_stars:
            star1 = None
            star2 = None
            for star in star_list:
                if index[0] == star.hd_id:
                    star1 = star
                elif index[1] == star.hd_id:
                    star2 = star
            if star1 is not None and star2 is not None:
                self.constellation_lines.append(self.draw_constellation_line(star1, star2))

    def draw_moon(self, moon, phase, x, y):
        r = 12
        # If moon.phase is new, draw black circle with white outline
        if phase == 'New':
            moon.canvas_id = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='black', outline='white')
        # If moon.phase is first, draw a circle with the left half black, right half white, white outline
        elif phase == 'First Quarter':
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='black', outline='white')

            moon.canvas_id = self.canvas.create_arc(x - r, y - r, x + r, y + r, start=270, extent=180, fill='white',
                                                    outline='white',
                                                    style=tk.CHORD)
            x = self.canvas.create_arc(x - r, y - r, x + r, y + r, start=270, extent=180, fill='white', outline='white',
                                       style=tk.CHORD)

        # If moon.phase is full, draw a white circle with white outline
        elif phase == 'Full':
            moon.canvas_id = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='white', outline='white')
        # If moon.phase is last, draw a circle with the left half white, right half black, white outline
        else:
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='black', outline='white')
            moon.canvas_id = self.canvas.create_arc(x - r, y - r, x + r, y + r, start=90.0, extent=180.0,
                                                    style=tk.CHORD,
                                                    fill='white', outline='white')

        canvas_coords = self.canvas.coords(moon.canvas_id)
        moon.canvas_x = canvas_coords[0]
        moon.canvas_y = canvas_coords[1]

        self.canvas.tag_bind(moon.canvas_id, '<ButtonPress-1>', lambda e: self.display_moon_info(e, moon))

    def draw_planet(self, planet, x, y):
        r = 6
        planet.canvas_id = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='blue', outline='blue')

        canvas_coords = self.canvas.coords(planet.canvas_id)
        planet.canvas_x = canvas_coords[0]
        planet.canvas_y = canvas_coords[1]

        self.canvas.tag_bind(planet.canvas_id, '<ButtonPress-1>', lambda e: self.display_planet_info(e, planet))

    def draw_messier_object(self, messier, x, y):
        if messier.magnitude <= 1.0:
            r = 5.5
        elif messier.magnitude <= 2.0:
            r = 4.5
        elif messier.magnitude <= 3.0:
            r = 3.5
        elif messier.magnitude <= 4.0:
            r = 2.5
        elif messier.magnitude <= 5.0:
            r = 1.5
        elif messier.magnitude <= 6.0:
            r = 0.5
        else:
            r = 0
        messier.canvas_id = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='red', outline='red')
        canvas_coords = self.canvas.coords(messier.canvas_id)
        messier.canvas_x = canvas_coords[0]
        messier.canvas_y = canvas_coords[1]

        self.canvas.tag_bind(messier.canvas_id, '<ButtonPress-1>', lambda e: self.display_messier_info(e, messier))

    def display_star_info(self, e, star):
        x = self.parent.parent.winfo_pointerx()
        y = self.parent.parent.winfo_pointery()
        self.create_modal_dialog(star, x, y)

    # Don't really need to be able to click on constellation to get names - Jo
    # def display_constellation_info(self, e, constellation):
    #     x = self.parent.parent.winfo_pointerx()
    #     y = self.parent.parent.winfo_pointery()
    #     self.create_modal_dialog(constellation, x, y)

    def display_moon_info(self, e, moon):
        x = self.parent.parent.winfo_pointerx()
        y = self.parent.parent.winfo_pointery()
        self.create_modal_dialog(moon, x, y)

    def display_planet_info(self, e, planet):
        x = self.parent.parent.winfo_pointerx()
        y = self.parent.parent.winfo_pointery()
        self.create_modal_dialog(planet, x, y)

    def display_messier_info(self, e, messier):
        x = self.parent.parent.winfo_pointerx()
        y = self.parent.parent.winfo_pointery()
        self.create_modal_dialog(messier, x, y)

    def display_object_label(self, object):
        tag = "label"
        font = ""
        size = 0
        if isinstance(object, Star):
            if object.magnitude <= 2:
                offset = 13
            elif 2 < object.magnitude <= 6:
                offset = 10
            else:
                offset = 5
            fill = '#F6DC83'
            tag = 'label'
        elif isinstance(object, MessierObject):
            if object.magnitude <= 2:
                offset = 13
            elif 2 < object.magnitude <= 6:
                offset = 10
            else:
                offset = 5
            fill = 'red'
            tag = 'label'
        elif isinstance(object, Moon):
            offset = 30
            fill = 'white'
            tag = 'label'
        elif isinstance(object, Planet):
            offset = 30
            fill = 'blue'
            tag = 'label'
        elif isinstance(object, Constellation):
            offset = 0
            fill = 'white'
            tag = 'const_label'
            # Set Label font based on platform
            if sys.platform == "win32" or sys.platform == "win64":
                font = 'Magneto'
                size = 14
            elif sys.platform == "darwin":
                font = 'Brush Script MT'
                size = 28
            elif sys.platform == "linux" or sys.platform == "linux2":
                font = 'URW Chancery L'
                size = 14
        else:
            offset = 0
            fill = 'purple'
        if isinstance(object, Constellation):
            self.label_widgets.append((self.canvas.create_text(object.x, object.y, text=str(object.proper_name),
                                                               fill=fill, tag=tag, font=(font, size))))
        else:
            self.label_widgets.append(
                (self.canvas.create_text(object.canvas_x + (offset / 3 * self.multiplier), object.canvas_y +
                                (offset * self.multiplier), text=str(object.proper_name), fill=fill, tag=tag)))

    def create_modal_dialog(self, object, x, y):
        modal_dlg = tk.Toplevel(master=self)
        modal_dlg.columnconfigure(0, weight=1)
        modal_dlg.columnconfigure(1, weight=1)
        modal_dlg.columnconfigure(2, weight=1)
        modal_dlg.resizable(False, False)

        if isinstance(object, Star):
            if object.proper_name != '':
                tk.Label(modal_dlg, text='Star Name: ' + str(object.proper_name)).grid(column=0, row=0, columnspan=3,
                                                                                       sticky='nw')
            else:
                tk.Label(modal_dlg, text='Star HD ID: ' + str(object.hd_id)).grid(column=0, row=0, columnspan=3,
                                                                                  sticky='nw')
            tk.Label(modal_dlg, text='Star Altitude: ' + str(object.altitude)).grid(column=0, row=1, columnspan=3,
                                                                                    sticky='nw')
            tk.Label(modal_dlg, text='Star Azimuth: ' + str(object.azimuth)).grid(column=0, row=2, columnspan=3,
                                                                                  sticky='nw')
            tk.Label(modal_dlg, text='Star Magnitude: ' + str(object.magnitude)).grid(column=0, row=4, columnspan=3,
                                                                                      sticky='nw')

        # Don't really need to have dialog for constellations
        # elif isinstance(object, Constellation):
        #     tk.Label(modal_dlg, text='Constellation Name: ' + str(object.proper_name)).grid(column=0, row=0,
        #                   columnspan=3, sticky='nsew')

        elif isinstance(object, Moon):
            tk.Label(modal_dlg, text='Moon').grid(column=0, row=0, columnspan=3, sticky='nw')
            tk.Label(modal_dlg, text="Moon Altitude: " + str(object.alt)).grid(column=0, row=1, columnspan=3,
                                                                               sticky='nw')
            tk.Label(modal_dlg, text="Moon Azimuth: " + str(object.az)).grid(column=0, row=2, columnspan=3,
                                                                            sticky='nw')
            tk.Label(modal_dlg, text="Moon Phase: " + str(object.phase)).grid(column=0, row=4, columnspan=3,
                                                                            sticky='nw')
        elif isinstance(object, Planet):
            tk.Label(modal_dlg, text='Planet Name: ' + str(object.proper_name)).grid(column=0, row=0, columnspan=3,
                                                                            sticky='nw')
            tk.Label(modal_dlg, text="Planet Altitude: " + str(object.alt)).grid(column=0, row=1, columnspan=3,
                                                                            sticky='nw')
            tk.Label(modal_dlg, text="Planet Azimuth: " + str(object.az)).grid(column=0, row=2, columnspan=3,
                                                                            sticky='nw')
        elif isinstance(object, MessierObject):
            if object.proper_name != '':
                tk.Label(modal_dlg, text='Messier Object Name: ' + str(object.proper_name)).grid(column=0, row=0,
                                                                                columnspan=3, sticky='nw')
            else:
                tk.Label(modal_dlg, text='Messier Catalog ID: ' + str(object.messier_cat)).grid(column=0, row=0,
                                                                                columnspan=3, sticky='nw')
            tk.Label(modal_dlg, text='Messier Object Description: ' + str(object.description)).grid(column=0, row=1,
                                                                                columnspan=3, sticky='nw')
            tk.Label(modal_dlg, text='Messier Object Altitude: ' + str(object.altitude)).grid(column=0, row=2,
                                                                                columnspan=3, sticky='nw')
            tk.Label(modal_dlg, text='Messier Object Azimuth: ' + str(object.azimuth)).grid(column=0, row=3,
                                                                                columnspan=3, sticky='nw')
            tk.Label(modal_dlg, text='Messier Object Magnitude: ' + str(object.magnitude)).grid(column=0, row=4,
                                                                                columnspan=3, sticky='nw')

        modal_dlg.geometry('+%d+%d' % (x, y))
        modal_dlg.transient(self.parent)
        modal_dlg.focus_set()
        modal_dlg.grab_set()
        self.wait_window(modal_dlg)

    # Save the current canvas as a jpeg
    def save_canvas(self):
        save_file = asksaveasfilename(filetypes=[('', '.jpeg')], defaultextension='*.jpeg')
        # self.canvas.update()
        #
        # self.canvas.postscript(file='canvas.ps', x=-4000, y=-4000, width=8000, height=8000)

        if save_file != '':
            args = [
                "ps2jpg",
                "-dSAFER", "-dBATCH", "-dNOPAUSE",
                "-sDEVICE=jpeg",
                "-dEPSCrop",
                "-r150",
                "-sOutputFile=" + save_file,
                "canvas.ps"
            ]
            encoding = locale.getpreferredencoding()
            args = [a.encode(encoding) for a in args]
            ghostscript.Ghostscript(*args)

    def create_ps_file(self):
        self.canvas.update()
        self.canvas.postscript(file='canvas.ps', x=-4000, y=-4000, width=8000, height=8000)

    def on_mouse_wheel_scroll(self, e):
        if e.state == 8:
            self.canvas.yview_scroll(int(-1 * (e.delta / abs(e.delta))), 'units')
        elif e.state == 9:
            self.canvas.xview_scroll(int(-1 * (e.delta / abs(e.delta))), 'units')
