import customtkinter as ctk
from blinker import signal
from usermanager import UserManager,User

class Menu:
    def open_menu(self, root):
        pass

    def close_menu(self, root):
        pass

root = ctk.CTk()

Current_open_menu:Menu = None
User_Manager:UserManager = UserManager()

if Current_open_menu is not None:
    Current_open_menu.open_menu(root)

root.geometry("1000x600")
root.mainloop()