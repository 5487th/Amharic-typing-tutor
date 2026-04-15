import customtkinter as ctk

root = ctk.CTk()

Current_open_menu:Menu = None

if Current_open_menu is not None:
    Current_open_menu.open_menu(root)

root.mainloop()

class Menu:
    def open_menu(self, root):
        pass
    def close_menu(self, root):
        pass


