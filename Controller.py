import tkinter as tk
import Model
import New_View
import datetime


class Controller():
    def __init__(self):
        now = datetime.datetime.now()
        self.root = tk.Tk()

        self.model = Model.Model(now.year, now.month, now.day, now.hour, now.minute, 0, 0, 0)
        self.view = New_View.MainApplication(parent=self.root)
        self.view.user_frame.button_generate_map.config(command=self.generate_map)
        self.view.user_frame.checkbox_show_constellations.config(command=self.toggle_constellations)
        self.view.user_frame.checkbox_show_labels.config(command=self.toggle_labels)
        self.view.user_frame.button_reset.config(command=self.reset_app)
        self.view.star_map_frame.canvas.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        self.view.star_map_frame.canvas.bind('<Button-5>', self.wheelup)  # only with Linux, wheel scroll down
        self.view.star_map_frame.canvas.bind('<Button-4>', self.wheeldown)  # only with Linux, wheel scroll up

        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Save Map', command=self.view.star_map_frame.save_canvas)
        self.filemenu.add_command(label='Help', command=self.view.display_help())
        self.filemenu.add_command(label='Exit')
        self.menubar.add_cascade(label='File', menu=self.filemenu)
        self.root.config(menu=self.menubar)

        self.root.attributes("-fullscreen", False)
        self.state = True
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)

        self.empty_map = True

        # store the center of the canvas
        self.centerX = self.view.star_map_frame.canvas.xview()[0]
        self.centerY = self.view.star_map_frame.canvas.yview()[0]

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.root.attributes("-fullscreen", self.state)
        return

    def end_fullscreen(self, event=None):
        self.state = False
        self.root.attributes("-fullscreen", False)
        return

    def run(self):
        self.view.pack(fill="both", expand=True)
        self.root.title("Lumarium")
        self.root.geometry("1100x700")
        self.root.mainloop()

    # Onclick event for when the "Generate Map" button is pushed
    # Tells View to clear current canvas
    # Gets user inputted values -- error is values inputted incorrectly
    # Updates the Model's TimeCalculations class with user inputted values
    # Has Model calculate celestial objects locations
    # Tells View to draw objects
    def generate_map(self):
        self.view.star_map_frame.multiplier = 1
        ready = True
        for widget in self.view.user_frame.validation_widgets:
            ready = self.view.user_frame.validate_combobox(widget)
            if ready is False:
                print('validate_widget: wrong values')
                # self.view.create_error_dialog('validate_widget: wrong values')
                return

        # Clear Canvas
        self.view.star_map_frame.canvas.delete('all')
        self.view.star_map_frame.reset_values()
        self.model.reset_values()

        try:
            month = int(self.view.user_frame.month_value.get())
            day = int(self.view.user_frame.day_value.get())
            year = int(self.view.user_frame.year_value.get())
            hour = int(self.view.user_frame.hour_value.get())
            minute = int(self.view.user_frame.minute_value.get())
            utc_offset = int(self.view.user_frame.utc_value.get())
            latitude = float(self.view.user_frame.latitude_value.get())
            longitude = float(self.view.user_frame.longitude_value.get())
            dst = int(self.view.user_frame.daylight_savings_value.get())
        except ValueError:
            # self.view.create_error_dialog('wrong values')
            print('wrong values')
            return

        self.empty_map = False

        # Update the Model's TimeCalculations class with the newly inputted times
        self.model.time_calc.update_times(year, month, day, hour, minute, utc_offset, latitude, longitude, dst)

        # Draw a black rectangle for saving map purposes
        self.view.star_map_frame.draw_background()

        # Calculate the Stars' positions
        self.model.Calculate_Star_Positions()

        # Draw each star
        for star in self.model.star_list:
            self.view.star_map_frame.draw_star(star, star.x, star.y)
            # if star.proper_name is not None:
            #     print(star.proper_name)

        # Calculate Moon Position and Phase
        self.model.Calculate_Moon_Position()

        # Draw Moon
        self.view.star_map_frame.draw_moon(self.model.moon, self.model.moon.phase, self.model.moon.x, self.model.moon.y)

        # Calculate Planets' Positions
        self.model.Calculate_Planet_Positions()

        # Draw Each Planet
        for planet in self.model.planet_list:
            if planet.proper_name != 'Earth/Sun':
                self.view.star_map_frame.draw_planet(planet, planet.x, planet.y)

        # Calculate Messier Object's Positions
        self.model.Calculate_Messier_Positions()

        # Draw Each Messier Objects
        for messier in self.model.messier_list:
            self.view.star_map_frame.draw_messier_object(messier, messier.x, messier.y)

        # Toggle Constellations
        if self.view.user_frame.constellations_value.get() == 1:
            self.toggle_constellations()

        if self.view.user_frame.labels_value.get() == 1:
            self.toggle_labels()

        self.view.star_map_frame.create_ps_file()

    def toggle_constellations(self):
        if self.empty_map is False:
            if self.view.user_frame.constellations_value.get() == 1:
                for const in self.model.constellation_list:
                    const.set_center()
                    self.view.star_map_frame.draw_constellation(const, self.model.star_list)
                    if self.view.user_frame.labels_value.get() == 1:
                        self.view.star_map_frame.display_object_label(const)
                    elif self.view.user_frame.labels_value.get() == 0:
                        self.view.star_map_frame.canvas.delete('const_label')
            elif self.view.user_frame.constellations_value.get() == 0:
                for line in self.view.star_map_frame.constellation_lines:
                    self.view.star_map_frame.canvas.delete(line)
                    self.view.star_map_frame.constellation_lines = []
                self.view.star_map_frame.canvas.delete('const_label')

    def toggle_labels(self):
        if self.empty_map is False:
            if self.view.user_frame.labels_value.get() == 1:
                for star in self.model.star_list:
                    if star.proper_name != '':
                        self.view.star_map_frame.display_object_label(star)
                for planet in self.model.planet_list:
                    if planet.proper_name != 'Earth/Sun':       # Don't need a label to show up for Earth
                        self.view.star_map_frame.display_object_label(planet)

                self.view.star_map_frame.display_object_label(self.model.moon)

                # Constellation labels need special treatment because they're divas.
                for const in self.model.constellation_list:
                    if self.view.user_frame.constellations_value.get() == 1:
                        self.view.star_map_frame.display_object_label(const)

                for messier in self.model.messier_list:
                    self.view.star_map_frame.display_object_label(messier)
            else:
                self.view.star_map_frame.canvas.delete('label')
                self.view.star_map_frame.canvas.delete('const_label')

    # Somehow, the reset needs to reset the x, y coordinates of the map back to the center. As it is, at least on a Mac,
    # when you zoom and pan and then reset and re-generate the map, it draws it where you left off panning instead of
    # where it was originally.
    def reset_app(self):
        self.view.star_map_frame.multiplier = 1
        self.view.star_map_frame.canvas.delete('all')
        self.view.star_map_frame.reset_values()
        self.model.reset_values()

        # Recenter the canvas
        self.view.star_map_frame.canvas.xview_moveto(self.centerX)
        self.view.star_map_frame.canvas.yview_moveto(self.centerY)
        self.view.star_map_frame.canvas.scale("all", self.centerX, self.centerY, 1.0, 1.0)

    '''def reset_app(self):
        self.view.star_map_frame.constellation_lines = []
        self.empty_map = True
        self.view.star_map_frame.canvas.delete('all')
        for widget in self.view.user_frame.validation_widgets:
            widget.set(widget.values[0])
        self.view.user_frame.daylight_savings_value.set(0)
        self.view.user_frame.constellations_value.set(0)
        self.view.user_frame.labels_value.set(0)

        # Clear Label stuff
        self.view.star_map_frame.canvas.delete('label')
        self.view.star_map_frame.canvas.delete('const_label')
        self.view.star_map_frame.label_widgets.clear()

        # Recenter the canvas
        #self.view.star_map_frame.canvas.scale("all", self.centerX, self.centerY, 1, 1)
        self.view.star_map_frame.canvas.xview_moveto(self.centerX)
        self.view.star_map_frame.canvas.yview_moveto(self.centerY)'''

    def wheel(self, event):
        true_x = self.view.star_map_frame.canvas.canvasx(event.x)
        true_y = self.view.star_map_frame.canvas.canvasy(event.y)
        scale = 1
        if event.delta > 0:
            scale = 1.1
            self.view.star_map_frame.canvas.scale("all", true_x, true_y, 1.1, 1.1)
        elif event.delta < 0:
            scale = 0.9
            self.view.star_map_frame.canvas.scale("all", true_x, true_y, 0.9, 0.9)
        self.view.star_map_frame.canvas.configure(scrollregion=self.view.star_map_frame.canvas.bbox("all"))

        self.view.star_map_frame.multiplier *= scale
        self.update_canvas_coords()

    # linux zoom
    def wheelup(self, event):
        self.view.star_map_frame.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        self.view.star_map_frame.canvas.configure(scrollregion=self.view.star_map_frame.canvas.bbox("all"))
        self.view.star_map_frame.multiplier *= 1.1
        self.view.star_map_frame.update_canvas_coords()

    def wheeldown(self, event):
        self.view.star_map_frame.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.view.star_map_frame.canvas.configure(scrollregion=self.view.star_map_frame.canvas.bbox("all"))
        self.view.star_map_frame.multiplier *= 0.9
        self.view.star_map_frame.update_canvas_coords()

    def update_canvas_coords(self):
        # Update canvas x, y coordinates
        for star in self.model.star_list:
            canvas_coords = self.view.star_map_frame.canvas.coords(star.canvas_id)
            star.canvas_x = canvas_coords[0]
            star.canvas_y = canvas_coords[1]

        for messier in self.model.messier_list:
            canvas_coords = self.view.star_map_frame.canvas.coords(messier.canvas_id)
            messier.canvas_x = canvas_coords[0]
            messier.canvas_y = canvas_coords[1]

        for planet in self.model.planet_list:
            if planet.proper_name != 'Earth/Sun':
                canvas_coords = self.view.star_map_frame.canvas.coords(planet.canvas_id)
                planet.canvas_x = canvas_coords[0]
                planet.canvas_y = canvas_coords[1]

        canvas_coords = self.view.star_map_frame.canvas.coords(self.model.moon.canvas_id)
        self.model.moon.canvas_x = canvas_coords[0]
        self.model.moon.canvas_y = canvas_coords[1]

        for constellation in self.model.constellation_list:
            constellation.set_center()

        #self.true_x = self.canvas.canvasx(event.x)
        #self.true_y = self.canvas.canvasy(event.y)

        # self.view.star_map_frame.canvas.scale("all", 0, 0, 1.0, 1.0)


if __name__ == "__main__":
    c = Controller()
    c.run()
