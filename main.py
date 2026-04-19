import customtkinter as ctk
import os
from blinker import signal

from usermanager import UserManager,User
from languagemanager import LanguageManager

appdata_local = os.getenv('LOCALAPPDATA')
save_dir = os.path.join(appdata_local, "MyApp")


class Menu:
    def open_menu(self, root):
        pass

    def close_menu(self, root):
        pass


    
root = ctk.CTk()

class user_login_menu(Menu):
    def __init__(self):
        self.on_language_dropdown_value_changed = signal("on_language_dropdown_value_changed")
    def open_menu(self, root):
        self.languages = ["English", "አማርኛ"]
        self.language_dropdown = ctk.CTkOptionMenu(root,values=self.languages,)
        self.language_dropdown.pack(side = "top", anchor = "nw", pady = 20, padx = 20)

        self.choose_a_user_label = ctk.CTkLabel(root, text= "welcome, login or create a user",font=("Roboto",40))
        self.choose_a_user_label.pack(pady=40)
    
    def close_menu(self, root):
        return super().close_menu(root)


Current_open_menu:Menu = user_login_menu()
User_Manager:UserManager = UserManager()
language_manager:LanguageManager = LanguageManager(LanguageManager.AMHARIC_LANGUAGE_KEY)

print(language_manager.translate("welcome, login or create a user"))

if Current_open_menu is not None:
    Current_open_menu.open_menu(root)

root.geometry("1000x600")
ctk.set_appearance_mode("light")
root.mainloop()