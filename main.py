import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import customtkinter as ctk
from blinker import signal
import pathlib
import ctypes

from scripts.user_manager import UserManager
from scripts.language_manager import LanguageManager
from scripts.menus import *
from scripts.games import *
from scripts.menu_connectors import *

root = ctk.CTk()

# managers
user_manager: UserManager = UserManager()
language_manager: LanguageManager = LanguageManager()

# menus
login_menu = LoginMenu(root, language_manager, user_manager)
signup_menu = SignUpMenu(root, language_manager, user_manager)
main_menu = MainMenu(root, user_manager, language_manager)
manual_menu = ManualMenu(root, language_manager)
typing_test_menu = TypingTestMenu(root, language_manager)
user_settings_menu = UserSettingsMenu(root, user_manager, language_manager)

# games
amharic_word_bank = pathlib.Path(__file__).parent / "assets" / "amharic_word_bank.json"
amharic_name_bank = pathlib.Path(__file__).parent / "assets" / "amharic_name_bank.json"

amharic_rain_game_menu = AmharicRainMenu()
amharic_rain_game_menu.load_word_bank(amharic_word_bank)

amharic_typing_race = AmharicTypingRaceMenu(root, language_manager.current_lang)
amharic_typing_race.load_word_bank(str(amharic_word_bank))

# entry menu
login_menu.open_menu()

# menu connectors
login_to_signup_connector = LoginToSignupConnector(login_menu, signup_menu)
login_to_main_menu_connector = LoginToMainMenuConnector(
    root, login_menu, main_menu, language_manager, user_manager
)
main_menu_to_manual_menu = MainMenuToManualMenuConnector(main_menu, manual_menu)
main_menu_to_typing_test = MainMenuToTypingTestMenu(main_menu, typing_test_menu)
main_menu_to_amharic_rain_menu = MainMenuToAmharicRainGameMenu(
    root, main_menu, amharic_rain_game_menu
)
main_menu_to_amharic_race_menu = MainMenuToAmharicRaceGameMenu(
    root, main_menu, amharic_typing_race
)
main_menu_to_settings_menu = MainMenuToUserSettingsMenu(
    root,
    main_menu,
    user_settings_menu,
    login_menu,
    signup_menu,
    language_manager,
    user_manager,
)


root.geometry("1000x600")
root.minsize(1000, 600)
root.title("Amharic typing games")

# icon
app_id = "Amharic.Typing.games.Id"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

app_icon_path = (
    pathlib.Path(__file__).parent
    / "assets"
    / "images"
    / "amharic typing games app icon.ico"
)
root.iconbitmap(app_icon_path)

try:
    root.mainloop()
except KeyboardInterrupt:
    print("Program interrupted by user.")
