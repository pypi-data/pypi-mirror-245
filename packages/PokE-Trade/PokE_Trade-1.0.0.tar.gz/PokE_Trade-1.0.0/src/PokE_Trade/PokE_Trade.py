import customtkinter as ctk 
from PIL import Image
import pkg_resources
import tkinter as tk

dev = True
if dev:
    import API
    from Widgets import *
if not dev:
    from . import API
    from .Widgets import *





class DataTracker:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title('PokeMMO Hub API')
        self.colors = {
            'red':'#d82b2b', 
            'black':'#000000', 
            'white':'#ffffff'
            }
        self.size_x = 600           # 457*1.5
        self.size_y = 600           # 586*1.5
        self.app.geometry(f'{self.size_x}x{self.size_y}')

        # Custom Fonts
        self.large_font = ctk.CTkFont('Comic Sans MS', 55)
        self.med_font = ctk.CTkFont('Comic Sans MS', 35)
        self.small_font = ctk.CTkFont('Comic Sans MS', 12)

        # Setting Up Main Window Layout
        self.bg = Background(self.app, 'bg.png', (self.size_x, self.size_y))

        self.main_frame = ctk.CTkFrame(self.app)
        self.main_frame.grid(padx=100, pady=200)


        # Adding Tabs for easy switching between menus
        self.tabs = ctk.CTkTabview(self.main_frame)
        self.tabs.grid(padx=20, pady=20)
        self.tabs.add("Price Checking")  # add tab at the end
        self.tabs.add("Item Id's")  # add tab at the end
        self.tabs.set("Price Checking")  # set currently visible tab

        # self.btn_frame = Panel(self.app, grid_x=0, grid_y=35, bg_color='transparent', outline_color=self.colors['black'], outline_width=5)
        self.btn1 = Button(self.tabs.tab("Price Checking"), grid_x=2, grid_y=3, text="Select Date", corner=6, bg_color=self.colors['black'], action=self.date_entry, text_font=self.small_font)
        self.btn2 = Button(self.tabs.tab("Price Checking"), grid_x=3, grid_y=3, text='Select Item', corner=6, bg_color=self.colors['black'], action=self.enter_id, text_font=self.small_font)
        self.btn3 = Button(self.tabs.tab("Price Checking"), grid_x=4, grid_y=3, text='Help', corner=6, bg_color=self.colors['black'], action=None, text_font=self.small_font)


        self.id_table = CsvTable(self.tabs.tab("Item Id's"), 'ItemID.csv')
        self.id_table.grid(row=0, column=0, padx=20, pady=10)


        self.calendar_window = None
        self.date_input = None
        self.item_name = None
        self.item_id = None


    def open_calendar(self):
        self.calendar_window = DatePopUp(self.root)

    def date_entry(self):
        self.date_popup = PopUp(text="Enter Date (Ex: dd/mm/yyy ):", title="Date")
        print("User Entered Date: ", self.date_popup.get_input())
        self.date_input = self.date_popup.get_input()

    def enter_id(self):
        self.id_popup = PopUp(text="Enter Item ID:", title="Item ID")
        print("User Entered Item ID: ", self.id_popup.get_input())
        self.item_id = self.id_popup.get_input()


    def start(self):
        self.app.mainloop()

if __name__ == '__main__':
    api = DataTracker()
    api.start()