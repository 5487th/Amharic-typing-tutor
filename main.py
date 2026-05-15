import customtkinter as ctk
from blinker import signal
import pathlib
import ctypes

from scripts.user_manager import UserManager
from scripts.language_manager import LanguageManager
from scripts.menus import *
from scripts.menu_connectors import *

root = ctk.CTk()

# managers
user_manager: UserManager = UserManager()
language_manager: LanguageManager = LanguageManager()

# menus
login_menu = LoginMenu(root, language_manager, user_manager)
signup_menu = SignUpMenu(root, language_manager, user_manager)
settings_menu = SettingsMenu(root)
main_menu = MainMenu(root, user_manager, language_manager)

# menu connectors
login_to_signup_connector = LoginToSignupConnector(login_menu, signup_menu)
login_to_main_menu_connector = LoginToMainMenuConnector(
    root, login_menu, main_menu, language_manager, user_manager
)


login_menu.open_menu()


root.geometry("1000x600")
root.minsize(1000, 600)
root.title("Amharic typing tutor")
ctk.set_appearance_mode("light")

# icon
app_id = "Amharic.Typing.Tutor.Id"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

app_icon_path = (
    pathlib.Path(__file__).parent
    / "assets"
    / "images"
    / "amharic typing tutor app icon.ico"
)
root.iconbitmap(app_icon_path)

try:
    root.mainloop()
except KeyboardInterrupt:
    print("Program interrupted by user.")
