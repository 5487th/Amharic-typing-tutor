import customtkinter as ctk
from blinker import signal

from scripts.user_manager import UserManager
from scripts.language_manager import LanguageManager
from scripts.reusable_custom_widgets import *
from scripts.menus import UserloginSignupScreen


root = ctk.CTk()

#managers
User_Manager:UserManager = UserManager()
language_manager:LanguageManager = LanguageManager()

#menus
user_login_signup_screen=UserloginSignupScreen(root, language_manager, User_Manager)

root.geometry("1000x600")
root.minsize(1000,600)
ctk.set_appearance_mode("light")

user_login_signup_screen.open_menu()

try:
    root.mainloop()
except KeyboardInterrupt:
    print("Program interrupted by user.")