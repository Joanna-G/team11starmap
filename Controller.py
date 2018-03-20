import tkinter as tk
import Model
import View
import datetime

class Controller():
    def __init__(self):
        now = datetime.datetime.now()
        self.root = tk.Tk()
        self.model = Model.Model(now.year, now.month, now.day, now.hour, now.minute, 0, 0, 0)
        self.view = View.MainApplication(parent=self.root)
        self.view.menu_frame.button_generate_map.config(command=self.generate_map)

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
        # Clear Canvas
        self.view.star_map_frame.canvas.delete('all')
        try:
            year = int(self.view.menu_frame.entry_year.get())
            month = int(self.view.menu_frame.entry_month.get())
            day = int(self.view.menu_frame.entry_day.get())
            time = self.view.menu_frame.entry_time.get().split(':')
            hour = int(time[0])
            minute = int(time[1])
            utc_offset = int(self.view.menu_frame.entryval_utc_offset.get())
            latitude = float(self.view.menu_frame.entry_latitude.get())
            longitude = float(self.view.menu_frame.entry_longitude.get())

        except ValueError:
            print('wrong values')
            return
        except IndexError:
            print('wrong values')
            return

        # Update the Model's TimeCalculations class with the newly inputted times
        self.model.time_calc.update_times(year, month, day, hour, minute, utc_offset, latitude, longitude)

        # Calculate the Stars' positions
        self.model.Calculate_Star_Positions()

        # Draw each star
        for star in self.model.star_list:
            self.view.star_map_frame.draw_star(star, star.x, star.y)

        # Draw each constellation line
        for const in self.model.constellation_list:
            print(const.name)
            for index in const.star_list:
                star1 = None
                star2 = None
                for star in self.model.star_list:
                    if index[0] == star.hd_id:
                        star1 = star
                    elif index[1] == star.hd_id:
                        star2 = star
                if star1 is not None and star2 is not None:
                    self.view.star_map_frame.draw_constellation_line(star1, star2, const)


if __name__ == "__main__":
    c = Controller()
    c.run()