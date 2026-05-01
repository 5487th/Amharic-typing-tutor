import customtkinter as ctk
from blinker import signal
import pathlib
import ctypes

from scripts.user_manager import UserManager
from scripts.language_manager import LanguageManager
from scripts.reusable_custom_widgets import *
from scripts.menus import UserloginSignupScreen


root = ctk.CTk()

#managers
User_Manager:UserManager = UserManager()
language_manager:LanguageManager = LanguageManager()

User_Manager.change_username("unlocked user", "locked user")
#menus
user_login_signup_screen=UserloginSignupScreen(root, language_manager, User_Manager)

user_login_signup_screen.open_menu()

root.geometry("1000x600")
root.minsize(1000, 600)
root.title("Amharic typing tutor")
ctk.set_appearance_mode("light")

#icon
app_id="Amharic.Typing.Tutor.Id"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

app_icon_path = pathlib.Path(__file__).parent/"assets"/"images"/"amharic typing tutor app icon.ico"
root.iconbitmap(app_icon_path)

try:
    root.mainloop()
except KeyboardInterrupt:
    print("Program interrupted by user.")