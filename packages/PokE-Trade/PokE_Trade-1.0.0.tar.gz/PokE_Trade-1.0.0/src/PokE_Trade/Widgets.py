import customtkinter as ctk
from PIL import Image
from tkinter import ttk
import csv
import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime

class SVar(ctk.StringVar):
    def __init__(self):
        pass

class Button(ctk.CTkButton):
    def __init__(self, parent, grid_x=0, grid_y=0, text=None, action=None, bg_color='#ffffff', corner=0, enabled=True, text_font=None, pad_x=0, pad_y=0):
        super().__init__(parent, text=text, command=action, fg_color=bg_color, corner_radius=corner, state=('disabled' if enabled == False else 'enabled'), font=text_font)
        self.grid(row=grid_x,column=grid_y, padx=pad_x, pady=pad_y)


class TextBox(ctk.CTkEntry):
    def __init__(self, parent, grid_x=0, grid_y=0, text=None, enabled=True, variable=None, pad_x=0, pad_y=0):
        super().__init__(parent, text=text, command=action, textvariable=variable, state=('disabled' if enabled == False else 'enabled'))
        self.grid(row=grid_x,column=grid_y)

class PopUp(ctk.CTkInputDialog):
    def __init__(self, text='Example Entry', title='Example'):
        super().__init__(text=text, title=title)

class Panel(ctk.CTkFrame):
    def __init__(self, parent, grid_x=0, grid_y=0, bg_color='transparent', outline_color='transparent', outline_width=0, pad_x=0, pad_y=0):
        super().__init__(parent, fg_color=bg_color, border_color=outline_color, border_width=outline_width)
        self.grid(row=grid_x,column=grid_y)


class Background(ctk.CTkLabel):
    def __init__(self, parent, img_path: str, img_size: tuple, pos_x=0, pos_y=0, scale_x=1, scale_y=1):
        self.image = ctk.CTkImage(light_image=Image.open(img_path),
                                  dark_image=Image.open(img_path),
                                  size=img_size)
        super().__init__(parent, image=self.image, text='')
        self.place(x=pos_x, y=pos_y, relwidth=scale_x, relheight=scale_y)


class Title(ctk.CTkLabel):
    def __init__(self, parent, text='Title Here', grid_x=0, grid_y=0, txt_color='#FFFFFF', corner=0, bg_color="transparent", text_font=None, pad_x=0, pad_y=0):
        super().__init__(parent, text=text, text_color=txt_color, fg_color=bg_color, corner_radius=corner, font=text_font)
        self.grid(row=grid_x, column=grid_y)


# class DatePopUp(ctk.CTkToplevel):
#     '''
#     Example Usage:

#             self.toplevel_window = None

#     def open_toplevel(self):
#         if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
#             self.toplevel_window = DatePopUp(self)  # create window if its None or destroyed
#         else:
#             self.toplevel_window.focus()  # if window exists focus it

#     '''
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.geometry("400x300")
#         self.selected_date = None
#         self.cal = Calendar(self, selectmode="day", year=2023, month=12, day=6)
#         self.submit = Button(self, text="Submit")
#         self.result_label = ctk.CTkLabel(root, text="Selected Date: None")

#     def submit_selected_date():
#         self.selected_date = cal.selection_get()
#         self.result_label.config(text=f"Selected Date: {self.selected_date}")
        

class DatePopUp(ctk.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.geometry("400x300")
        self.selected_date = None
        self.cal = Calendar(self, selectmode="day", year=2023, month=12, day=6)
        self.submit = ctk.CTkButton(self, text="Submit", command=self.submit_selected_date)
        self.result_label = tk.Label(self, text="Selected Date: None")

        # Pack widgets
        self.cal.pack(pady=10)
        self.submit.pack(pady=5)
        self.result_label.pack(pady=10)

    def submit_selected_date(self):
        self.selected_date = self.cal.selection_get()
        self.result_label.config(text=f"Selected Date: {self.selected_date}")
        # Call the method in the parent UI to handle the selected date
        self.master.set_date(self.selected_date)
        # Close the DatePopUp window
        self.destroy()


    def date_as_unix(self):
        if self.selected_date:
            # Convert the selected date to a Unix timestamp
            unix_timestamp = int(self.selected_date.timestamp())
            return unix_timestamp
        else:
            return None

    def date_as_ddmmyyyy(self):
        if self.selected_date:
            # Format the date as dd/mm/yyyy
            formatted_date = self.selected_date.strftime("%d/%m/%Y")
            return formatted_date
        else:
            return None


class CsvTable(ctk.CTkFrame):
    def __init__(self, parent, csv_filepath):
        super().__init__(parent)
        self.parent = parent
        self.csv_file = csv_filepath

        # Create Treeview widget
        self.tree = ttk.Treeview(self)
        self.tree["columns"] = ()
        self.tree["show"] = "headings"

        # Add vertical scrollbar
        yscrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.tree.yview)
        yscrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=yscrollbar.set)

        # Add horizontal scrollbar
        xscrollbar = ctk.CTkScrollbar(self, orientation="horizontal", command=self.tree.xview)
        xscrollbar.pack(side="bottom", fill="x")
        self.tree.configure(xscrollcommand=xscrollbar.set)

        # Load CSV file and populate the table
        self.load_csv(self.csv_file)

        # Pack the Treeview widget
        self.tree.pack(expand=True, fill="both")

    def load_csv(self, filename):
        try:
            with open(filename, "r", newline="") as file:
                reader = csv.reader(file)
                header = next(reader)

                # Configure Treeview columns
                self.tree["columns"] = header
                for col in header:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, anchor="center", width=100)

                # Populate the Treeview with data
                for row in reader:
                    self.tree.insert("", "end", values=row)
        except FileNotFoundError:
            print(f"File {filename} not found.")