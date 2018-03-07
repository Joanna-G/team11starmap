import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
from tkinter import Canvas
from PIL import ImageTk, Image, ImageDraw
from tkinter.filedialog import asksaveasfilename
import os
import sys
import locale
from Parsers import StarParser
import celestial_objects
import calculations
import ghostscript
import time


class MainApplication(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

        self.grid(column=0, row=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(1, weight=1)

        self.header_frame = HeaderFrame(self)
        self.menu_frame = MenuFrame(self)
        self.star_map_frame = StarMapFrame(self)
        self.header_frame.grid(column=0, row=0, columnspan=2)
        self.menu_frame.grid(column=0, row=1)
        self.star_map_frame.grid(column=1, row=1)

        self.header_frame.button_save.configure(command=self.star_map_frame.save_canvas)


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
        self.time_calc = None
        self.sp = None
        self.sp_list = []
        self.star_list = []

        self.widgets_list = []

        self.grid(column=0, row=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        style = ttk.Style()
        style.configure('Menu.TFrame', background='green')

        # self.menu_frame = ttk.Frame(self, style='Menu.TFrame')
        self.menu_frame = ttk.Frame(self)
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
        # self.menu_frame.rowconfigure(11, weight=1)

        self.entryval_month = StringVar(self.parent)
        self.entryval_month.set('Month (1-12)')
        self.entryval_day = StringVar(self.parent)
        self.entryval_day.set('Day (1-31)')
        self.entryval_year = StringVar(self.parent)
        self.entryval_year.set('Year (1900-2100)')
        self.entryval_time = StringVar(self.parent)
        self.entryval_time.set('00:00 (24 Hour Clock Local Time)')
        self.entryval_utc_offset = StringVar(self.parent)
        self.entryval_utc_offset.set('UTC Offset (-12-14)')
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
        # self.label_title.config(font=('Magneto', 22), anchor='s', background='green')
        self.label_title.config(font=('Magneto', 22), anchor='s')

        self.label_date_time = tk.Label(self.menu_frame, text='Date and Time')
        self.label_date_time.grid(column=0, row=1, sticky='nsew', padx=10, pady=10)
        # self.label_date_time.config(anchor='sw', background='green')
        self.label_date_time.config(anchor='sw')

        self.entry_month = tk.Entry(self.menu_frame, textvariable=self.entryval_month)
        self.entry_month.config(foreground='grey')
        self.entry_month.grid(column=0, row=2, sticky='nsew', padx=10)
        self.entry_month.bind('<FocusIn>', lambda e: self.clear_widget_text(e, 'Month'))
        self.entry_month.bind('<FocusOut>', lambda e: self.validate_widget_value(e, 'Month', 'Month (1-12)'))
        self.widgets_list.append(self.entry_month)

        self.entry_day = tk.Entry(self.menu_frame, textvariable=self.entryval_day)
        self.entry_day.config(foreground='grey')
        self.entry_day.grid(column=0, row=3, sticky='nsew', padx=10, pady=10)
        self.entry_day.bind('<FocusIn>', lambda e: self.clear_widget_text(e, 'Day'))
        self.entry_day.bind('<FocusOut>', lambda e: self.validate_widget_value(e, 'Day', 'Day (1-31)'))
        self.widgets_list.append(self.entry_day)

        self.entry_year = tk.Entry(self.menu_frame, textvariable=self.entryval_year)
        self.entry_year.config(foreground='grey')
        self.entry_year.grid(column=0, row=4, sticky='nsew', padx=10)
        self.entry_year.bind('<FocusIn>', lambda e: self.clear_widget_text(e, 'Year'))
        self.entry_year.bind('<FocusOut>', lambda e: self.validate_widget_value(e, 'Year', 'Year (1900-2100)'))
        self.widgets_list.append(self.entry_year)

        self.entry_time = tk.Entry(self.menu_frame, textvariable=self.entryval_time)
        self.entry_time.config(foreground='grey')
        self.entry_time.grid(column=0, row=5, sticky='nsew', padx=10, pady=10)
        self.entry_time.bind('<FocusIn>', lambda e: self.clear_widget_text(e, 'Time'))
        self.entry_time.bind('<FocusOut>', lambda e: self.validate_widget_value(e, 'Time', '00:00 (24 Hour Clock Local Time)'))
        self.widgets_list.append(self.entry_time)

        self.entry_utc_offset = tk.Entry(self.menu_frame, textvariable=self.entryval_utc_offset)
        self.entry_utc_offset.config(foreground='grey')
        self.entry_utc_offset.grid(column=0, row=6, sticky='nsew', padx=10, pady=10)
        self.entry_utc_offset.bind('<FocusIn>', lambda e: self.clear_widget_text(e, 'UTC Offset'))
        self.entry_utc_offset.bind('<FocusOut>', lambda e: self.validate_widget_value(e, 'UTC Offset', 'UTC Offset (-12-14)'))
        self.widgets_list.append(self.entry_utc_offset)

        self.label_location = tk.Label(self.menu_frame, text='Location')
        self.label_location.grid(column=0, row=7, sticky='nsew', padx=10, pady=10)
        self.label_location.config(anchor='sw')

        self.entry_latitude = tk.Entry(self.menu_frame, textvariable=self.entryval_latitude)
        self.entry_latitude.config(foreground='grey')
        self.entry_latitude.grid(column=0, row=8, sticky='nsew', padx=10)
        self.entry_latitude.bind('<FocusIn>', lambda e: self.clear_widget_text(e, 'Latitude'))
        self.entry_latitude.bind('<FocusOut>', lambda e: self.validate_widget_value(e, 'Latitude', 'Latitude (-90-90)'))
        self.widgets_list.append(self.entry_year)

        self.entry_longitude = tk.Entry(self.menu_frame, textvariable=self.entryval_longitude)
        self.entry_longitude.config(foreground='grey')
        self.entry_longitude.grid(column=0, row=9, sticky='nsew', padx=10, pady=10)
        self.entry_longitude.bind('<FocusIn>', lambda e: self.clear_widget_text(e, 'Longitude'))
        self.entry_longitude.bind('<FocusOut>', lambda e: self.validate_widget_value(e, 'Longitude', 'Longitude (-180-180)'))
        self.widgets_list.append(self.entry_year)

        self.button_generate_map = tk.Button(self.menu_frame, text='Generate Map')
        self.button_generate_map.grid(column=0, row=10, sticky='nsew', padx=10)
        self.button_generate_map.config(command=self.generate_map)

        self.init_celestial_list()

    def init_celestial_list(self):
        self.sp = StarParser.StarParser()
        self.sp = self.sp.parse_file()
        for sp_star in self.sp:
            star = celestial_objects.Star(sp_star[0], sp_star[1], sp_star[2], float(sp_star[3]), float(sp_star[4]), float(sp_star[5]))
            self.star_list.append(star)

    def generate_map(self):
        self.parent.star_map_frame.canvas.delete('all')
        try:
            year = int(self.entry_year.get())
            month = int(self.entry_month.get())
            day = int(self.entry_day.get())
            time = self.entry_time.get().split(':')
            hour = int(time[0])
            minute = int(time[1])
            utc_offset = int(self.entryval_utc_offset.get())
            latitude = float(self.entry_latitude.get())
            longitude = float(self.entry_longitude.get())
        except ValueError:
            print('wrong values')
            return
        except IndexError:
            print('wrong values')
            return

        self.time_calc = calculations.TimeCalculations(year, month, day, hour, utc_offset, minute, latitude, longitude)

        for star in self.star_list:
            star.ha_time = star.calculate_ha_time(self.time_calc.lst, star.right_ascension)
            star.ha_degrees = star.ha_time_to_degrees(star.ha_time)
            star.altitude = star.calculate_alt(star.declination, self.time_calc.lat, star.ha_degrees)
            star.azimuth = star.calculate_az(star.declination, self.time_calc.lat, star.ha_degrees, star.altitude)
            star.get_xy_coords(star.altitude, star.azimuth)

        for star in self.star_list:
            x = star.x * 2000
            y = star.y * 2000
            self.parent.star_map_frame.draw_star(star, x, y)

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
            if widget_value == '00:00 (24 Hour Clock Local Time)':
                event.widget.delete(0, tk.END)
                event.widget.config(foreground='black')
        elif tag == 'UTC Offset':
            if widget_value == 'UTC Offset (-12-14)':
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

    def validate_widget_value(self, event, tag, text):
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
            hour = None
            minute = None
            try:
                time = widget_value.split(':')
                hour = int(time[0])
                minute = int(time[1])
            except IndexError:
                widget_value = ''
            except ValueError:
                widget_value = ''
            if widget_value == '' or hour < 0 or hour > 24 or minute < 0 or minute > 60:
                event.widget.delete(0, tk.END)
                event.widget.config(foreground='grey')
                event.widget.insert(0, text)
        elif tag == 'UTC Offset':
            try:
                widget_value = int(widget_value)
            except ValueError:
                widget_value = ''
            if widget_value == '' or widget_value < -12 or widget_value > 14:
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

    def get_widget_values(self):
        pass


class StarMapFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

        self.grid(column=0, row=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.star_map_frame = ttk.Frame(self)
        self.star_map_frame.grid(column=0, row=0, sticky='nsew')
        self.star_map_frame.columnconfigure(0, weight=1)
        self.star_map_frame.rowconfigure(0, weight=1)
        # self.star_map_frame.bind('<Configure>', self.on_resize)

        self.max_width = 0
        self.max_height = 0

        directory = ''
        if getattr(sys, 'frozen', False):
            directory = os.path.dirname(sys.executable)
        elif __file__:
            directory = os.path.dirname(__file__)
        filename = os.path.join(directory, 'resources', 'mars.png')
        self.image = ImageTk.PhotoImage(Image.open(filename))
        self.im = Image.open(filename)

        self.canvas = Canvas(self.star_map_frame)
        self.canvas.grid(column=0, row=0, sticky='nsew')
        self.vsb_canvas = tk.Scrollbar(self.star_map_frame, orient=tk.VERTICAL)
        self.vsb_canvas.grid(column=1, row=0, sticky='ns')
        self.vsb_canvas.config(command=self.canvas.yview)
        self.hsb_canvas = tk.Scrollbar(self.star_map_frame, orient=tk.HORIZONTAL)
        self.hsb_canvas.grid(column=0, row=1, sticky='ew')
        self.hsb_canvas.config(command=self.canvas.xview)
        self.canvas.config(xscrollcommand=self.hsb_canvas.set, yscrollcommand=self.vsb_canvas.set, scrollregion=(-2000,-2000,2000,2000))
        # self.canvas.update()

    def draw_star(self, star, x, y):
        # self.canvas.create_image(x, y, image=self.image)
        # x = self.canvas.create_line(x, y, x+10, y)
        r = 2
        x = self.canvas.create_oval(x-r, y-r, x+r, y+r)
        self.canvas.tag_bind(x, '<ButtonPress-1>', lambda e: self.display_info(e, star)) #<ButtonPress-1> <Enter>

    def display_info(self, e, star):
        # print('star id: ' + str(star.star_id) + ' star altitude: ' + str(star.altitude))
        x = self.parent.parent.winfo_pointerx()
        y = self.parent.parent.winfo_pointery()
        self.create_modal_dialog(star, x, y)

    def create_modal_dialog(self, star, x, y):
        modal_dlg = tk.Toplevel(master=self)
        modal_dlg.columnconfigure(0, weight=1)
        modal_dlg.columnconfigure(1, weight=1)
        modal_dlg.columnconfigure(2, weight=1)
        modal_dlg.resizable(False, False)

        tk.Label(modal_dlg, text='Star ID: ' + str(star.star_id)).grid(column=0, row=0, columnspan=3, sticky='nsew')

        modal_dlg.geometry('+%d+%d' % (x, y))
        modal_dlg.transient(win)
        modal_dlg.focus_set()
        modal_dlg.grab_set()
        # modal_dlg.protocol('WM_DELETE_WINDOW', lambda: self.on_modal_dlg_close(modal_dlg))
        self.wait_window(modal_dlg)

    def on_modal_dlg_close(self, modal_dlg):
        modal_dlg.destroy()

    def save_canvas(self):
        save_file = asksaveasfilename(filetypes=[('', '.jpeg')])
        self.canvas.update()
        self.canvas.postscript(file='canvas.ps', x=-2000, y=-2000, width=4000, height=4000)

        args = [
            "ps2jpg",  # actual value doesn't matter
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


if __name__ == "__main__":
    win = tk.Tk()
    m = MainApplication(parent=win)
    m.pack(fill="both", expand=True)
    win.title("Lumarium")
    win.geometry("1100x700")
    win.mainloop()