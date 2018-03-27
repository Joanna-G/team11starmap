import tkinter as tk
import Model
import View
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

        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Save Map', command=self.view.star_map_frame.save_canvas)
        self.filemenu.add_command(label='Help')
        self.filemenu.add_command(label='Exit')
        self.menubar.add_cascade(label='File', menu=self.filemenu)
        self.root.config(menu=self.menubar)

        self.root.attributes("-fullscreen", True)
        self.state = True
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)

        self.constellation_lines = []
        self.empty_map = True

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
        ready = True
        for widget in self.view.user_frame.validation_widgets:
            ready =  self.view.user_frame.validate_combobox(widget)
            if ready is False:
                print('validate_widget: wrong values')
                return

        # Clear Canvas
        self.view.star_map_frame.canvas.delete('all')
        self.constellation_lines = []
        try:
            month = int(self.view.user_frame.month_value.get())
            day = int(self.view.user_frame.day_value.get())
            year = int(self.view.user_frame.year_value.get())
            hour = int(self.view.user_frame.hour_value.get())
            minute = int(self.view.user_frame.minute_value.get())
            utc_offset = int(self.view.user_frame.utc_value.get())
            latitude = float(self.view.user_frame.latitude_value.get())
            longitude = float(self.view.user_frame.longitude_value.get())
        except ValueError:
            print('wrong values')
            return

        self.empty_map = False

        # Update the Model's TimeCalculations class with the newly inputted times
        self.model.time_calc.update_times(year, month, day, hour, minute, utc_offset, latitude, longitude)

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
            self.view.star_map_frame.draw_messier_object()

        self.toggle_constellations()

    def toggle_constellations(self):
        if self.empty_map is False:
            if self.view.user_frame.constellations_value.get() == 1:
                for const in self.model.constellation_list:
                    for index in const.star_list:
                        star1 = None
                        star2 = None
                        for star in self.model.star_list:
                            if index[0] == star.hd_id:
                                star1 = star
                            elif index[1] == star.hd_id:
                                star2 = star
                        if star1 is not None and star2 is not None:
                            self.constellation_lines.append(self.view.star_map_frame.draw_constellation_line(star1,
                                                                                            star2, const))
            elif self.view.user_frame.constellations_value.get() == 0:
                for line in self.constellation_lines:
                    self.view.star_map_frame.canvas.delete(line)
                self.constellation_lines = []

    def toggle_labels(self):
        if self.empty_map is False:
            if self.view.user_frame.labels_value.get() == 1:
                for star in self.model.star_list:
                    if star.proper_name != '':
                        # print(star.proper_name)
                        self.view.star_map_frame.display_object_label(star)
                for planet in self.model.planet_list:
                    if planet.proper_name != 'Earth/Sun':
                        self.view.star_map_frame.display_object_label(planet)
                self.view.star_map_frame.display_object_label(self.model.moon)
                for const in self.model.constellation_list:
                    self.view.star_map_frame.display_object_label(const)
            else:
                self.view.star_map_frame.canvas.delete('label')

    def reset_app(self):
        self.constellation_lines = []
        self.empty_map = True
        self.view.star_map_frame.canvas.delete('all')
        for widget in self.view.user_frame.validation_widgets:
            widget.set(widget.values[0])
        self.view.user_frame.daylight_savings_value.set(0)
        self.view.user_frame.constellations_value.set(0)
        self.view.user_frame.labels_value.set(0)

        # Clear Label stuff
        self.view.star_map_frame.canvas.delete('label')
        self.view.star_map_frame.label_widgets.clear()


if __name__ == "__main__":
    c = Controller()
    c.run()