import customtkinter as ctk
from blinker import signal
from scripts.user_manager import UserManager, User
from scripts.language_manager import LanguageManager
from scripts.custom_widgets import *
import json
import time
import threading
import random
import math
import tkinter as tk

try:
    import winsound as _winsound

    _HAS_WINSOUND = True
except ImportError:
    _HAS_WINSOUND = False


class Menu:
    def open_menu(self, root):
        pass

    def close_menu(self):
        pass


class LoginMenu(Menu):
    def __init__(
        self, root, _language_manager: LanguageManager, _user_manager: UserManager
    ):
        self.language_manager = _language_manager
        self.user_manager = _user_manager
        self.root = root
        self.on_user_logged_in = signal(f"on_user_logged_in {self}")
        self.on_add_user_button_pressed = signal(f"on_plus_button_pressed {self}")

        self.language_set = "English"
        self.theme_set = "system"

        self.main_frame = None
        self.DropDown_frame = None
        self.languages = None
        self.language_dropdown = None
        self.themes_dropdown = None
        self.choose_a_user_label = None
        self.user_icons_frame = None

    def open_menu(self, First_open=False):
        if not self.main_frame:
            self.main_frame = CTkFrame(self.root, fg_color="transparent")
        if not self.DropDown_frame:
            self.DropDown_frame = CTkFrame(self.main_frame, fg_color="transparent")
            self.DropDown_frame.pack(anchor="nw", pady=5)

        # languages selection drop down
        self.languages = ["English", "አማረኛ"]
        if not self.language_dropdown:
            self.language_dropdown = ctk.CTkOptionMenu(
                self.DropDown_frame,
                values=self.languages,
                command=self.on_languge_drop_down_value_changed,
            )
        if self.language_set == "am":
            self.language_dropdown.set("አማረኛ")
            self.language_manager.set_language("am")
        else:
            self.language_dropdown.set("English")
            self.language_manager.set_language("en")

        self.language_dropdown.pack(side="left", padx=5)

        # theme selection drop down
        self.themes = ["System", "Light", "Dark"]
        if not self.themes_dropdown:
            self.themes_dropdown = ctk.CTkOptionMenu(
                self.DropDown_frame,
                values=self.themes,
                command=self.on_themes_drop_down_value_changed,
            )
        self.themes_dropdown.pack(side="left", padx=5)

        ctk.set_appearance_mode(self.theme_set)

        # choose a user label
        if not self.choose_a_user_label:
            self.choose_a_user_label = ctk.CTkLabel(
                self.main_frame, font=("Roboto", 40)
            )
            self.language_manager.register_widget(
                self.choose_a_user_label, "Welcome, login or create a user"
            )
        self.choose_a_user_label.place(rely=0.2, relx=0.5, anchor="center")

        # user icons frame
        if not self.user_icons_frame:
            self.user_icons_frame = ctk.CTkFrame(
                self.main_frame, bg_color="transparent", fg_color="transparent"
            )

        self.user_icons_frame.place(relx=0.5, rely=0.5, anchor="center")

        # user icons frame logic
        self.user_icons = []
        self.update_user_icon_display()

        # connecting signals
        self.user_manager.on_user_created.connect(
            self.on_user_icons_display_need_to_be_updated
        )
        self.user_manager.on_user_deleted.connect(
            self.on_user_icons_display_need_to_be_updated
        )
        self.user_manager.on_user_changed_username.connect(
            self.on_user_icons_display_need_to_be_updated
        )

        # placing frame
        self.main_frame.place(
            relwidth=1, relheight=1, relx=0.5, rely=0.5, anchor="center"
        )
        self.root.update_idletasks()

    def close_menu(self):
        self.main_frame.place_forget()
        self.root.update_idletasks()

    def on_user_icons_display_need_to_be_updated(self, sender, **kwargs):
        self.update_user_icon_display()

    def update_user_icon_display(self):
        for widget in self.user_icons_frame.winfo_children():
            widget.destroy()

        self.user_icons = []
        for user in self.user_manager.get_all_users():
            user_icon = UserProfileCard(self.user_icons_frame, self.user_manager, user)
            user_icon.pack_propagate(False)
            user_icon.pack(side="left", padx=1)
            user_icon.on_user_pressed_icon.connect(self.on_user_icon_presesd)
            self.user_icons.append(user_icon)

        self.add_user_Button = ctk.CTkButton(
            self.user_icons_frame,
            width=150,
            height=190,
            corner_radius=10,
            text="+",
            text_color="white",
            font=("Roboto", 40),
            command=self.on_plus_button_pressed,
        )
        self.add_user_Button.pack(side="left", padx=1)

    def on_languge_drop_down_value_changed(self, value):
        if value == "English":
            self.language_manager.set_language(
                self.language_manager.ENGLISH_LANGUAGE_KEY
            )
            self.language_set = "en"

        if value == "አማረኛ":
            self.language_manager.set_language(
                self.language_manager.AMHARIC_LANGUAGE_KEY
            )
            self.language_set = "am"

    def on_themes_drop_down_value_changed(self, value):
        self.theme_set = value
        ctk.set_appearance_mode(self.theme_set)

    def on_plus_button_pressed(self):
        self.on_add_user_button_pressed.send(self)

    def on_user_icon_presesd(self, sender, user):
        self.user_icons_frame.place_forget()
        self.choose_a_user_label.place_forget()
        self.root.update_idletasks()

        self.user_login_menu = UserloginPopUp(
            user, self.language_manager, self.user_manager, self.main_frame
        )
        self.user_login_menu.place(relx=0.5, rely=0.5, anchor="center")

        self.user_login_menu.on_cancel_login_button_pressed.connect(
            self.on_cancel_login_button_pressed
        )
        self.user_login_menu.on_login_button_pressed.connect(
            self.on_login_button_pressed
        )

    # login
    def on_login_button_pressed(self, sender, user, entered_password):
        hashed_password = user.password

        if self.user_manager.is_Correct_password(hashed_password, entered_password):
            self.log_user_in(user=user)
            self.user_login_menu.password_entery_field.configure(border_width=0)
        else:
            self.user_login_menu.password_entery_field.configure(
                border_width=3, border_color="red"
            )

    def log_user_in(self, user):
        self.user_manager.login(user)
        self.user_login_menu.place_forget()
        self.on_user_logged_in.send(self, user=user)

    def on_cancel_login_button_pressed(self, sender):
        self.user_login_menu.password_entery_field.delete(0, "end")
        self.user_login_menu.password_entery_field.configure(border_width=0)

        self.user_login_menu.place_forget()

        self.choose_a_user_label.place(rely=0.2, relx=0.5, anchor="center")
        self.user_icons_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.update_user_icon_display()
        self.root.update_idletasks()


class SignUpMenu(Menu):
    def __init__(self, root, language_manager, user_manager):
        self.root = root
        self.language_manager = language_manager
        self.user_manager: UserManager = user_manager

        self.on_user_created = signal("on_create_user_button_pressed")
        self.on_cancel_button_pressed = signal("on_cancel_user_button_pressed")

    def open_menu(self):
        if not self.root:
            warnings.warn(
                "attempted to open sign up menu with None root, sign up menu not opened"
            )

        self.root = self.root

        # main frame
        self.main_frame = CTkFrame(self.root)

        self.main_frame.configure(self.root, width=400, height=500)
        self.main_frame.pack_propagate(False)
        self.main_frame.propagate(False)

        # main frame tittle
        self.Create_a_user_label = CTkLabel(self.main_frame, font=("Roboto", 30))
        self.Create_a_user_label.pack(pady=20)
        self.language_manager.register_widget(
            self.Create_a_user_label, "Create a new user"
        )
        self.user_manager.default_profile_picture_path
        # buttons
        self.buttons_frame = CTkFrame(
            self.main_frame, fg_color="transparent", width=390, height=40
        )
        self.buttons_frame.pack_propagate(False)
        self.buttons_frame.pack(side="bottom", pady=15)

        self.create_button = CTkButton(
            self.buttons_frame,
            corner_radius=10,
            text="Create",
            width=175,
            height=40,
            command=self.on_create_user_button_pressed,
            font=("Roboto", 20),
        )
        self.language_manager.register_widget(self.create_button, "Create")
        self.create_button.pack(side="left", padx=10)

        self.cancel_button = CTkButton(
            self.buttons_frame,
            corner_radius=10,
            text="Cancel",
            width=175,
            height=40,
            command=self.on_cancel_user_creation_button_pressed,
            font=("Roboto", 20),
        )
        self.language_manager.register_widget(self.cancel_button, "Cancel")
        self.cancel_button.pack(side="right", padx=10)

        # buffer
        self.button_details_buffer = CTkFrame(
            self.main_frame, height=50, fg_color="transparent"
        )
        self.button_details_buffer.pack_propagate(False)
        self.button_details_buffer.pack(side="bottom")

        # details frame
        self.details_frame = CTkFrame(self.main_frame, fg_color="transparent")
        self.details_frame.pack(side="bottom")

        # username label
        self.username_label = CTkLabel(self.details_frame, font=("Roboto", 20))
        self.language_manager.register_widget(self.username_label, "Username")
        self.username_label.pack(expand=True, fill="both")

        # user name entery
        self.username_entery_text_variable = StringVar()
        self.username_entery_text_variable.trace_add(
            "write", self.on_user_type_into_username_entery
        )
        self.username_entery_field = CTkEntry(
            self.details_frame,
            width=200,
            height=30,
            border_width=0,
            textvariable=self.username_entery_text_variable,
        )
        self.username_entery_field.pack(side="top")

        # requirements for username
        self.username_character_length_requirement_label = CTkLabel(
            self.details_frame, font=("Roboto", 15), text_color="red"
        )
        self.language_manager.register_widget(
            self.username_character_length_requirement_label,
            "-Username must be 4 - 12 characters long",
        )
        self.username_character_length_requirement_label.pack(side="top", pady=2)

        self.username_character_unqieness_requirement_label = CTkLabel(
            self.details_frame, font=("Roboto", 15), text_color="red"
        )
        self.language_manager.register_widget(
            self.username_character_unqieness_requirement_label,
            "-Username must be unique",
        )
        self.username_character_unqieness_requirement_label.pack(side="top", pady=2)

        self.username_password_buffer = CTkFrame(
            self.details_frame, height=20, fg_color="transparent"
        )
        self.username_password_buffer.pack_propagate(False)
        self.username_password_buffer.pack()

        # password
        self.password_label = CTkLabel(self.details_frame, font=("Roboto", 20))
        self.language_manager.register_widget(self.password_label, "Password")
        self.password_label.pack(side="top")

        self.password_entery_text_variable = StringVar()
        self.password_entery_text_variable.trace_add(
            "write", self.on_user_type_into_password_entery
        )
        self.password_entery_field = CTkEntry(
            self.details_frame,
            width=200,
            height=30,
            border_width=0,
            textvariable=self.password_entery_text_variable,
        )
        self.password_entery_field.pack(side="top")

        # requirement for password
        self.password_character_length_requirement_label = CTkLabel(
            self.details_frame, font=("Roboto", 15), text_color="green"
        )
        self.language_manager.register_widget(
            self.password_character_length_requirement_label,
            "-Password must have at least 4 characters or no characters for no password",
        )
        self.password_character_length_requirement_label.pack(side="top", pady=2)

        self.password_character_type_requirements_label = CTkLabel(
            self.details_frame, font=("Roboto", 15), text_color="green"
        )
        self.language_manager.register_widget(
            self.password_character_type_requirements_label,
            "-password must contan atleast one number and 3 letters if its not empty",
        )
        self.password_character_type_requirements_label.pack(side="top", pady=2)

        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.root.update_idletasks()

    def close_menu(self):
        self.main_frame.place_forget()

    def on_create_user_button_pressed(self):
        username = self.username_entery_field.get()
        password = self.password_entery_field.get()

        stripped_username = username.strip()
        stripped_password = password.strip()

        is_username_unique = not self.user_manager.user_exists(stripped_username)
        is_username_in_proper_range_of_characters = (
            len(stripped_username) <= 12 and len(stripped_username) >= 4
        )

        is_password_atleast_four_characters_long = len(stripped_password) >= 4
        is_password_empty = len(stripped_password) == 0

        has_numbers = any(char.isdigit() for char in stripped_password)
        has_atleast_three_letters = (
            sum(char.isalpha() for char in stripped_password) >= 3
        )

        is_valid_username = (
            is_username_unique and is_username_in_proper_range_of_characters
        )

        if is_valid_username and (
            is_password_atleast_four_characters_long
            and has_numbers
            and has_atleast_three_letters
        ):
            self.user_manager.create_user(stripped_username, stripped_password)
            self.on_user_created.send(self, username=stripped_username)

        elif is_valid_username and (is_password_empty):
            self.user_manager.create_user(stripped_username, "")
            self.on_user_created.send(self, username=stripped_username)

    def on_cancel_user_creation_button_pressed(self):
        self.on_cancel_button_pressed.send(self)

    def on_user_type_into_username_entery(self, *args):
        username = self.username_entery_field.get()

        is_username_unique = not self.user_manager.user_exists(username)
        is_username_in_proper_range_of_characters = (
            len(username) <= 12 and len(username) >= 4
        )

        is_valid_username = (
            is_username_unique and is_username_in_proper_range_of_characters
        )

        if is_username_unique:
            self.username_character_unqieness_requirement_label.configure(
                text_color="green"
            )
        else:
            self.username_character_unqieness_requirement_label.configure(
                text_color="red"
            )

        if is_username_in_proper_range_of_characters:
            self.username_character_length_requirement_label.configure(
                text_color="green"
            )
        else:
            self.username_character_length_requirement_label.configure(text_color="red")

    def on_user_type_into_password_entery(self, *args):
        password = self.password_entery_field.get()
        is_password_atleast_four_characters_long = len(password) >= 4
        is_password_empty = len(password) == 0
        is_password_valid = (
            is_password_empty and is_password_atleast_four_characters_long
        )

        has_numbers = any(char.isdigit() for char in password)
        has_atleast_three_letters = sum(char.isalpha() for char in password) >= 3

        if (has_numbers and has_atleast_three_letters) or is_password_empty:
            self.password_character_type_requirements_label.configure(
                text_color="green"
            )
        else:
            self.password_character_type_requirements_label.configure(text_color="red")

        if is_password_empty:
            self.password_character_length_requirement_label.configure(
                text_color="green"
            )
        elif is_password_atleast_four_characters_long:
            self.password_character_length_requirement_label.configure(
                text_color="green"
            )
        else:
            self.password_character_length_requirement_label.configure(text_color="red")


class MainMenu(Menu):
    def __init__(
        self,
        root,
        user_manager: UserManager,
        language_manager: LanguageManager,
    ):
        self.user_manager: UserManager = user_manager
        self.language_manager: LanguageManager = language_manager
        self.root = root

        self.on_profile_button_pressed = signal(f"on settings icon clicked {self}")
        self.on_help_button_pressed = signal(f"on help icon clicked {self}")
        self.on_user_logged_out = signal(f"on log out button pressed {self}")

        self.on_amharic_typing_test_activity_card_icon_pressed = signal(
            f"on typing test acvtivity icon button presed {self}"
        )
        self.on_amharic_rain_activity_card_icon_pressed = signal(
            f"on amharic rain acvtivity icon button presed {self}"
        )

    def open_menu(self):
        if not self.user_manager.current_user:
            warnings.warn("no user logged in, cant open main menu")
            return

        self.main_frame = CTkFrame(self.root, fg_color="transparent")

        self.header_Frame = CTkFrame(self.main_frame, height=10, fg_color="transparent")
        self.header_Frame.pack(fill="x")

        # profile button
        # user_profile_image_path = self.user_manager.default_profile_picture_path
        # if (
        #     self.user_manager.current_user.profile_picture_path
        #     and pathlib.Path(
        #         self.user_manager.current_user.profile_picture_path
        #     ).exists()
        # ):
        #     user_profile_image_path = (
        #         self.user_manager.current_user.profile_picture_path
        #     )

        # self.user_profile_button = ImageButton(
        #     self.header_Frame,
        #     light_image_path=user_profile_image_path,
        #     dark_image_path=user_profile_image_path,
        #     sizex=30,
        #     sizey=30,
        #     size_change_amount=1,
        # )
        # self.user_profile_button.on_mouse_click.connect(
        #     self.on_user_profile_icon_pressed
        # )
        # self.user_profile_button.pack(side="left", padx=10, pady=10)

        # log out button
        logout_black_icon_path = (
            pathlib.Path(__file__).parent.parent
            / "assets"
            / "images"
            / "icons"
            / "logout_icon_black.png"
        )
        logout_white_icon_path = (
            pathlib.Path(__file__).parent.parent
            / "assets"
            / "images"
            / "icons"
            / "logout_icon_white.png"
        )
        self.logout_button = ImageButton(
            self.header_Frame,
            light_image_path=logout_black_icon_path,
            dark_image_path=logout_white_icon_path,
            sizex=25,
            sizey=25,
            size_change_amount=1,
        )
        self.logout_button.on_mouse_click.connect(self.on_logout_icon_pressed)
        self.logout_button.pack(side="left", padx=10, pady=10)

        # help button
        help_icon_black_path = (
            pathlib.Path(__file__).parent.parent
            / "assets"
            / "images"
            / "icons"
            / "help_icon_black.png"
        )
        help_icon_white_path = (
            pathlib.Path(__file__).parent.parent
            / "assets"
            / "images"
            / "icons"
            / "help_icon_white.png"
        )

        self.help_button = ImageButton(
            self.header_Frame,
            light_image_path=help_icon_black_path,
            dark_image_path=help_icon_white_path,
            sizex=25,
            sizey=25,
            size_change_amount=1,
        )
        self.help_button.on_mouse_click.connect(self.on_help_icon_pressed)
        self.help_button.pack(side="left", padx=0, pady=10)

        # languages selection drop down
        self.languages = ["English", "አማረኛ"]
        self.language_dropdown = ctk.CTkOptionMenu(
            self.header_Frame,
            values=self.languages,
            command=self.on_languge_drop_down_value_changed,
        )
        self.language_dropdown.pack(side="left", padx=10)

        if self.user_manager.current_user.language == "am":
            self.language_dropdown.set("አማረኛ")
        elif self.user_manager.current_user.language == "en":
            self.language_dropdown.set("English")

        self.language_manager.set_language(self.user_manager.current_user.language)

        # theme selection drop down
        self.themes = ["System", "Light", "Dark"]
        self.themes_dropdown = ctk.CTkOptionMenu(
            self.header_Frame,
            values=self.themes,
            command=self.on_themes_drop_down_value_changed,
        )
        self.themes_dropdown.pack(side="left", padx=0)

        if self.user_manager.current_user.theme in ["dark", "light", "system"]:
            ctk.set_appearance_mode(self.user_manager.current_user.theme)

        if self.user_manager.current_user.theme == "dark":
            self.themes_dropdown.set("Dark")
        elif self.user_manager.current_user.theme == "light":
            self.themes_dropdown.set("Light")
        elif self.user_manager.current_user.theme == "system":
            self.themes_dropdown.set("System")

        self.activities_frame = CTkFrame(self.main_frame, corner_radius=10)
        self.activities_frame.pack(expand=True, fill="both", pady=5, padx=5)

        self.activities_frame_header_frame = CTkFrame(
            self.activities_frame, height=40, corner_radius=10
        )
        self.activities_frame_header_frame.pack(fill="x", side="top", padx=5, pady=5)

        self.activities_tittle_label = CTkLabel(
            self.activities_frame_header_frame, font=("Roboto", 30)
        )
        self.language_manager.register_widget(
            self.activities_tittle_label, "Play a typing game"
        )
        self.activities_tittle_label.pack(side="left", pady=10, padx=10)

        self.main_scrollable_frame = CTkScrollableFrame(
            self.activities_frame, fg_color="transparent", corner_radius=0
        )
        self.main_scrollable_frame.pack(expand=True, fill="both", padx=5, pady=5)

        self.log_out_confirmation_popup = UserlogoutPopUp(
            self.user_manager.current_user,
            self.language_manager,
            self.user_manager,
            self.main_frame,
        )
        self.log_out_confirmation_popup.on_logout_button_pressed.connect(
            self.on_logout_confirmation_button_pressed
        )
        self.log_out_confirmation_popup.on_cancel_logout_button_pressed.connect(
            self.on_cancel_logout_button_pressed
        )

        self.main_frame.place(
            relwidth=1, relheight=1, relx=0.5, rely=0.5, anchor="center"
        )

        self.root.update_idletasks()

        self.build_actvity_cards()

    def close_menu(self):
        self.main_frame.place_forget()

    def on_user_profile_icon_pressed(self, sender):
        self.on_profile_button_pressed.send(self)

    def on_help_icon_pressed(self, sender):
        self.on_help_button_pressed.send(self)

    def on_logout_icon_pressed(self, sender):
        self.header_Frame.pack_forget()
        self.activities_frame.pack_forget()
        self.log_out_confirmation_popup.place(relx=0.5, rely=0.5, anchor="center")

    def on_logout_confirmation_button_pressed(self, sender, user):
        self.user_manager.logout()
        self.on_user_logged_out.send(self, user=user)

    def on_cancel_logout_button_pressed(self, sender):
        self.header_Frame.pack(fill="x", side="top")
        self.activities_frame.pack(expand=True, fill="both", pady=10, padx=10)
        self.log_out_confirmation_popup.place_forget()

    def on_languge_drop_down_value_changed(self, value):
        if value == "አማረኛ":
            self.user_manager.change_user_language(
                self.user_manager.current_user.username, "am"
            )
            self.language_manager.set_language("am")
        elif value == "English":
            self.user_manager.change_user_language(
                self.user_manager.current_user.username, "en"
            )
            self.language_manager.set_language("en")

    def on_themes_drop_down_value_changed(self, value):
        if self.themes_dropdown.get() == "Dark":
            self.user_manager.change_user_theme(
                self.user_manager.current_user.username, "dark"
            )
            ctk.set_appearance_mode("dark")
        elif self.themes_dropdown.get() == "Light":
            self.user_manager.change_user_theme(
                self.user_manager.current_user.username, "light"
            )
            ctk.set_appearance_mode("light")
        elif self.themes_dropdown.get() == "System":
            self.user_manager.change_user_theme(
                self.user_manager.current_user.username, "system"
            )
            ctk.set_appearance_mode("system")

    def build_actvity_cards(self):
        self.amharic_typing_test_activity_card: ActivityCard = ActivityCard(
            self.main_scrollable_frame,
            str(
                pathlib.Path(__file__).parent.parent
                / "assets"
                / "images"
                / "amharic typing test icon.png"
            ),
            "Amharic Typing Test",
            "A simple typing test to test your amharic typing skills",
        )
        self.amharic_typing_test_activity_card.pack()

        self.language_manager.register_widget(
            self.amharic_typing_test_activity_card.tittle_label, "Amharic Typing Test"
        )
        self.language_manager.register_widget(
            self.amharic_typing_test_activity_card.discription_label,
            "A simple typing test to test your amharic typing skills",
        )

        self.amharic_typing_test_activity_card.on_start_button_pressed.connect(
            self.on_typing_test_activity_button_pressed
        )

        self.Amharic_rain_game_activity_card: ActivityCard = ActivityCard(
            self.main_scrollable_frame,
            str(
                pathlib.Path(__file__).parent.parent
                / "assets"
                / "images"
                / "amharic_rain_icon.png"
            ),
            "Amharic Rain",
            "Letters and words are falling out of the sky! quickly type them out and save them before they fall of your screen.",
        )
        self.Amharic_rain_game_activity_card.pack()

        self.language_manager.register_widget(
            self.Amharic_rain_game_activity_card.tittle_label, "Amharic Rain"
        )
        self.language_manager.register_widget(
            self.Amharic_rain_game_activity_card.discription_label,
            "Letters and words are falling out of the sky! quickly type them out and save them before they fall of your screen.",
        )

        self.Amharic_rain_game_activity_card.on_start_button_pressed.connect(
            self.on_Amharic_rain_activity_button_pressed
        )

    def on_typing_test_activity_button_pressed(self, sender):
        self.on_amharic_typing_test_activity_card_icon_pressed.send(self)

    def on_Amharic_rain_activity_button_pressed(self, sender):
        self.on_amharic_rain_activity_card_icon_pressed.send(self)


class ManualMenu(Menu):
    def __init__(self, root, language_manager):
        super().__init__()
        if not root:
            warnings.warn(
                "attempted to create manual menu with none root, manual menu not created"
            )
            return
        if not language_manager:
            if not root:
                warnings.warn(
                    "attempted to create manual menu with none language manager, manual menu not created"
                )
            return

        self.root = root
        self.on_back_button_pressed = signal(f"on back button pressed {self}")
        self.language_manager: LanguageManager = language_manager

        self.main_frame = None
        self.header_frame = None
        self.back_button = None
        self.tittle = None
        self.pdf_viewer = None

    def open_menu(self):
        if not self.main_frame:
            self.main_frame = CTkFrame(self.root, fg_color="transparent")
            self.main_frame.pack(expand=True, fill="both")
        else:
            self.main_frame.pack(expand=True, fill="both")

        if not self.header_frame:
            self.header_frame = CTkFrame(self.main_frame, fg_color="transparent")
            self.header_frame.pack(fill="x", side="top")

        back_black_icon_path = (
            pathlib.Path(__file__).parent.parent
            / "assets"
            / "images"
            / "icons"
            / "back_icon_black.png"
        )
        back_white_icon_path = (
            pathlib.Path(__file__).parent.parent
            / "assets"
            / "images"
            / "icons"
            / "back_icon_white.png"
        )
        if not self.back_button:
            self.back_button = ImageButton(
                self.header_frame,
                light_image_path=back_black_icon_path,
                dark_image_path=back_white_icon_path,
                sizex=30,
                sizey=30,
                size_change_amount=1,
            )
            self.back_button.pack(side="left", pady=10, padx=10)
            self.back_button.on_mouse_click.connect(self.on_back_icon_pressed)

        if not self.tittle:
            self.tittle = CTkLabel(
                self.header_frame, text="Manual", font=("Roboto", 25)
            )
            self.language_manager.register_widget(self.tittle, "Manual")
            self.tittle.pack(side="left", pady=10)

        pdf_path = None
        if self.language_manager.current_lang == "am":
            pdf_path = (
                pathlib.Path(__file__).parent.parent
                / "assets"
                / "manual"
                / "Amharic_Typing_Guide_amharic_version.pdf"
            )
        else:
            pdf_path = (
                pathlib.Path(__file__).parent.parent
                / "assets"
                / "manual"
                / "Amharic_Typing_Guide_english_version.pdf"
            )

        if not self.pdf_viewer:
            self.pdf_viewer = PDFViewer(self.main_frame, self.root)
            if pathlib.Path(pdf_path).exists():
                self.pdf_viewer.load(pdf_path)
            self.pdf_viewer.pack(expand=True, fill="both", side="top")

        if pathlib.Path(pdf_path).exists():
            self.pdf_viewer.load(pdf_path)

    def close_menu(self):
        self.main_frame.pack_forget()

    def on_back_icon_pressed(self, sender):
        self.on_back_button_pressed.send(self)


# claude aided
class TypingTestMenu(Menu):
    """
    Usage
    -----
        menu = TypingTestMenu(root, language_manager, word_bank_path="assets/words_en.json")
        menu.open_menu()
        menu.close_menu()

    Signals
    -------
        menu.on_back_button_pressed, fired when the back button is clicked
    """

    # ── colour tokens ──────────────────────────────────────────────────────────
    _CORRECT_W = "#22c55e"
    _INCORRECT_W = "#ef4444"
    _CORRECT_C = "#86efac"
    _INCORRECT_C = "#fca5a5"
    _UNTYPED_DARK = "#6b7280"
    _UNTYPED_LITE = "#9ca3af"
    _ACTIVE_FG_D = "#e2e8f0"
    _ACTIVE_FG_L = "#1e293b"
    _ACTIVE_BG_D = "#374151"
    _ACTIVE_BG_L = "#dbeafe"
    _CARET_BG = "#3b82f6"
    _CARET_FG = "#ffffff"

    # ── built-in word bank ─────────────────────────────────────────────────────
    _DEFAULT_WORDS = [
        "ነው",
        "ነበር",
        "አለ",
        "የለም",
        "አይደለም",
        "ይሆናል",
        "ሆነ",
        "አለች",
        "ነች",
        "ናቸው",
        "ሆኑ",
        "አደረገ",
        "አለ",
        "ሄደ",
        "መጣ",
        "አየ",
        "አወቀ",
        "ወሰደ",
        "ሰጠ",
        "ተናገረ",
        "አለፈ",
        "ቆመ",
        "ጀመረ",
        "ጨረሰ",
        "ተመለሰ",
        "ፈለገ",
        "አገኘ",
        "ሞከረ",
        "ቻለ",
        "ሞተ",
        "እና",
        "ወይም",
        "ግን",
        "ስለዚህ",
        "ምክንያቱም",
        "እንዲሁም",
        "አሁን",
        "ከዚያ",
        "እዚህ",
        "እዚያ",
        "ዛሬ",
        "ትናንት",
        "ነገ",
        "ብዙ",
        "ትንሽ",
        "ሁሉ",
        "አንድ",
        "ሁለት",
        "ሦስት",
        "አራት",
        "አምስት",
        "ስድስት",
        "ሰባት",
        "ስምንት",
        "ዘጠኝ",
        "አስር",
        "ሰው",
        "ልጅ",
        "ሴት",
        "ወንድ",
        "ቤት",
        "ስም",
        "ጊዜ",
        "ቀን",
        "ዓመት",
        "ወር",
        "ሥራ",
        "ገንዘብ",
        "ምግብ",
        "ውሃ",
        "አገር",
        "ከተማ",
        "መንገድ",
        "ትምህርት",
        "መጽሐፍ",
        "ቋንቋ",
        "ቤተሰብ",
        "ወዳጅ",
        "ፍቅር",
        "ሰላም",
        "ችግር",
        "መልስ",
        "ጥያቄ",
        "ምክር",
        "ሐሳብ",
        "ፈቃድ",
        "እርዳታ",
        "እኔ",
        "አንተ",
        "እሱ",
        "እሷ",
        "እኛ",
        "እናንተ",
        "እነሱ",
        "የእኔ",
        "የአንተ",
        "የእሱ",
        "ጥሩ",
        "መጥፎ",
        "ትልቅ",
        "ትንሽ",
        "አዲስ",
        "ያረጀ",
        "ፈጣን",
        "ዝግተኛ",
        "ቀላል",
        "ከባድ",
    ]

    def __init__(self, root, language_manager: LanguageManager, word_bank_path=None):
        super().__init__()
        if not root:
            warnings.warn(
                "attempted to create TypingTestMenu with none root, menu not created"
            )
            return
        if not language_manager:
            warnings.warn(
                "attempted to create TypingTestMenu with none language_manager, menu not created"
            )
            return

        self.root = root
        self.language_manager = language_manager
        self.on_back_button_pressed = signal(f"on back button pressed {self}")

        self._word_bank = self._load_word_bank(word_bank_path)

        # typing-test state
        self._words: list = []
        self._committed: list = []  # list[bool] – True = word typed correctly
        self._current_word_idx: int = 0
        self._current_typed: str = ""
        self._start_time = None
        self._running: bool = False
        self._timer_thread = None
        self._test_duration: int = 30
        self._time_left: float = 30.0
        self._wpm: int = 0
        self._acc: int = 100
        self._finished: bool = False

        # widget references (None until open_menu builds them)
        self.main_frame = None
        self.header_frame = None
        self.back_button = None
        self.title_label = None
        self.control_bar = None  # NEW – sits between header and text area
        self.time_label = None
        self.stat_label = None
        self._dur_buttons: dict = {}
        self.text_canvas = None
        self.input_field = None
        self._input_var = None
        self.wpm_label = None
        self.acc_label = None
        self.restart_btn = None

        # result overlay (a CTkFrame placed inside main_frame, not a Toplevel)
        self._result_overlay = None
        self._result_wpm_val = None
        self._result_acc_val = None

    # ── Menu protocol ──────────────────────────────────────────────────────────

    def open_menu(self):
        if not self.main_frame:
            self.main_frame = CTkFrame(self.root, fg_color="transparent")
            self._build_ui()

        self.main_frame.pack(expand=True, fill="both")
        self._new_test()
        self.root.update_idletasks()

    def close_menu(self):
        self._running = False
        if self.main_frame:
            self.main_frame.pack_forget()
        self.root.update_idletasks()

    # ── Build ──────────────────────────────────────────────────────────────────

    def _build_ui(self):
        self._build_header()
        self._build_control_bar()  # NEW position: below header, above text
        self._build_text_area()
        self._build_input_area()
        self._build_stats_bar()
        self._build_result_overlay()

    # ── Header: back button + title only ──────────────────────────────────────

    def _build_header(self):
        if not self.header_frame:
            self.header_frame = CTkFrame(self.main_frame, fg_color="transparent")
            self.header_frame.pack(fill="x", side="top")

        back_black_icon_path = (
            pathlib.Path(__file__).parent.parent
            / "assets"
            / "images"
            / "icons"
            / "back_icon_black.png"
        )
        back_white_icon_path = (
            pathlib.Path(__file__).parent.parent
            / "assets"
            / "images"
            / "icons"
            / "back_icon_white.png"
        )

        if not self.back_button:
            self.back_button = ImageButton(
                self.header_frame,
                light_image_path=back_black_icon_path,
                dark_image_path=back_white_icon_path,
                sizex=30,
                sizey=30,
                size_change_amount=1,
            )
            self.back_button.pack(side="left", pady=10, padx=10)
            self.back_button.on_mouse_click.connect(self._on_back_icon_pressed)

        if not self.title_label:
            self.title_label = CTkLabel(self.header_frame, text="", font=("Roboto", 25))
            self.language_manager.register_widget(self.title_label, "typing_test_title")
            self.title_label.pack(side="left", pady=10, padx=4)

    # ── Control bar: duration buttons (centred) + countdown on the right ───────

    def _build_control_bar(self):
        """
        A horizontal bar that sits directly below the header.

        Layout (left-to-right):
            [spacer]  Time:  15s  30s  60s  120s  [spacer]    42
                      ← centred group →                   ← right-pinned
        """
        if not self.control_bar:
            self.control_bar = CTkFrame(self.main_frame, fg_color="transparent")
            self.control_bar.pack(fill="x", padx=10, pady=(0, 8))

        # Right-side countdown label – packed first so it anchors to the right
        # before the centre group is placed.
        self.stat_label = CTkLabel(
            self.control_bar,
            text=str(self._test_duration),
            font=("Roboto", 34, "bold"),
        )
        self.stat_label.pack(side="right", padx=16)

        # Centre group: "Time:" label + duration buttons
        centre_group = CTkFrame(self.control_bar, fg_color="transparent")
        centre_group.pack(side="left", expand=True)  # expand pushes it to centre

        self.time_label = CTkLabel(centre_group, text="", font=("Roboto", 13))
        self.language_manager.register_widget(self.time_label, "typing_time_label")
        self.time_label.pack(side="left", padx=(0, 6))

        for dur in [15, 30, 60, 120]:
            b = CTkButton(
                centre_group,
                text=f"{dur}s",
                width=52,
                height=30,
                font=("Roboto", 13),
                command=lambda d=dur: self._set_duration(d),
            )
            b.pack(side="left", padx=3)
            self._dur_buttons[dur] = b

    # ── Text area ──────────────────────────────────────────────────────────────

    def _build_text_area(self):
        text_frame = CTkFrame(self.main_frame, corner_radius=10)
        text_frame.pack(fill="x", padx=10, pady=(0, 5))

        self.text_canvas = CTkTextbox(
            text_frame,
            font=("Courier New", 22, "bold"),
            wrap="word",
            state="disabled",
            height=180,
            border_width=0,
        )
        self.text_canvas.pack(fill="both", expand=True, padx=6, pady=6)

    # ── Input area ─────────────────────────────────────────────────────────────

    def _build_input_area(self):
        input_frame = CTkFrame(self.main_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=10, pady=50)

        self._input_var = StringVar()
        self._input_var.trace_add("write", self._on_input_change)

        self.input_field = CTkEntry(
            input_frame,
            textvariable=self._input_var,
            font=("Courier New", 17, "bold"),
            height=44,
            placeholder_text="",
        )
        self.input_field.pack(fill="x")
        self.input_field.bind("<KeyRelease>", self._on_key_release)

    # ── Stats bar ──────────────────────────────────────────────────────────────

    def _build_stats_bar(self):
        stats_frame = CTkFrame(self.main_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=10, pady=5)

        self.wpm_label = CTkLabel(stats_frame, text="", font=("Roboto", 14, "bold"))
        self.language_manager.register_widget(self.wpm_label, "typing_wpm_live")
        self.wpm_label.pack(side="left", padx=(0, 16))

        self.acc_label = CTkLabel(stats_frame, text="", font=("Roboto", 14, "bold"))
        self.language_manager.register_widget(self.acc_label, "typing_acc_live")
        self.acc_label.pack(side="left")

        self.restart_btn = CTkButton(
            stats_frame,
            text="",
            width=110,
            height=34,
            font=("Roboto", 14),
            command=self._new_test,
        )
        self.language_manager.register_widget(self.restart_btn, "typing_restart")
        self.restart_btn.pack(side="right")

    # ── Result overlay (inline, no Toplevel) ───────────────────────────────────

    def _build_result_overlay(self):
        """
        A card Frame placed with place() over the centre of main_frame.
        Hidden by default; shown on test completion; dismissed on restart.
        """
        self._result_overlay = CTkFrame(
            self.main_frame,
            corner_radius=16,
            border_width=2,
        )
        # Do NOT pack/place yet – shown only when the test finishes.

        # Title
        self._result_title_lbl = CTkLabel(
            self._result_overlay, text="", font=("Roboto", 18, "bold")
        )
        self.language_manager.register_widget(
            self._result_title_lbl, "typing_test_complete"
        )
        self._result_title_lbl.pack(pady=(24, 6))

        # Stats row – two equal columns with enforced minimum width so the
        # values never crowd each other regardless of digit count.
        stats_inner = CTkFrame(self._result_overlay)
        stats_inner.pack(padx=24, pady=8, fill="x")
        stats_inner.grid_columnconfigure(0, weight=1, minsize=120)
        stats_inner.grid_columnconfigure(1, weight=1, minsize=120)

        wpm_hdr = CTkLabel(stats_inner, text="", font=("Roboto", 13))
        self.language_manager.register_widget(wpm_hdr, "typing_wpm")
        wpm_hdr.grid(row=0, column=0, pady=(16, 2), padx=16)

        acc_hdr = CTkLabel(stats_inner, text="", font=("Roboto", 13))
        self.language_manager.register_widget(acc_hdr, "typing_accuracy")
        acc_hdr.grid(row=0, column=1, pady=(16, 2), padx=16)

        self._result_wpm_val = CTkLabel(
            stats_inner, text="—", font=("Roboto", 52, "bold")
        )
        self._result_wpm_val.grid(row=1, column=0, pady=(0, 16), padx=16)

        self._result_acc_val = CTkLabel(
            stats_inner, text="—", font=("Roboto", 52, "bold")
        )
        self._result_acc_val.grid(row=1, column=1, pady=(0, 16), padx=16)

        try_again_btn = CTkButton(
            self._result_overlay,
            text="",
            font=("Roboto", 15),
            height=40,
            command=self._new_test,
        )
        self.language_manager.register_widget(try_again_btn, "typing_try_again")
        try_again_btn.pack(pady=(6, 22), padx=30, fill="x")

    def _show_result_overlay(self):
        """Centre the overlay card over main_frame using place()."""
        self._result_overlay.place(relx=0.5, rely=0.5, anchor="center")
        self._result_overlay.lift()

    def _hide_result_overlay(self):
        self._result_overlay.place_forget()

    # ── Test logic ─────────────────────────────────────────────────────────────

    def _new_test(self):
        self._finished = False
        self._running = False
        self._start_time = None
        self._time_left = float(self._test_duration)
        self._committed = []
        self._current_word_idx = 0
        self._current_typed = ""
        self._wpm = 0
        self._acc = 100
        self._words = random.choices(self._word_bank, k=70)

        self._hide_result_overlay()

        self._render_text()
        self._input_var.set("")
        self.input_field.configure(
            state="normal",
            placeholder_text=self.language_manager.translate("typing_placeholder")
            or "",
        )
        self.input_field.focus()
        self.stat_label.configure(text=str(self._test_duration))
        self.wpm_label.configure(
            text=self.language_manager.translate("typing_wpm_live") or "WPM: —"
        )
        self.acc_label.configure(
            text=self.language_manager.translate("typing_acc_live") or "Accuracy: —%"
        )
        self._update_dur_buttons(self._test_duration)

    def _set_duration(self, dur: int):
        self._test_duration = dur
        self._update_dur_buttons(dur)
        self._new_test()

    def _update_dur_buttons(self, active: int):
        for dur, btn in self._dur_buttons.items():
            if dur == active:
                btn.configure(fg_color=("#1f6aa5", "#1f6aa5"))
            else:
                btn.configure(fg_color=("gray75", "gray25"))

    # ── Input handlers ─────────────────────────────────────────────────────────

    def _on_input_change(self, *_):
        if self._finished:
            return
        value = self._input_var.get()
        # The Amharic IME commits the current syllable by inserting a space.
        # Detect that here and treat it the same as _commit_word().
        if value.endswith(" ") or value.endswith("\u00a0"):
            self._commit_word(value.rstrip())
            return
        self._current_typed = value
        if self._current_typed and not self._running:
            self._start_timer()
        self._render_text()

    def _on_key_release(self, _event):
        if self._finished:
            return
        value = self._input_var.get()
        # Catch space from English keyboard path (IME not involved)
        if value.endswith(" ") or value.endswith("\u00a0"):
            self._commit_word(value.rstrip())
            return
        self._current_typed = value
        self._render_text()

    def _commit_word(self, typed: str):
        """Shared word-commit logic called from both IME and direct space paths."""
        if self._finished:
            return
        typed = typed.strip()
        if not typed:
            self._input_var.set("")
            return

        expected = self._words[self._current_word_idx]
        self._committed.append(typed == expected)
        self._current_word_idx += 1
        self._current_typed = ""
        self._input_var.set("")
        self.input_field.after(
            0,
            lambda: (
                self.input_field.delete(0, "end")
                if self.input_field.winfo_exists()
                else None
            ),
        )

        if not self._running:
            self._start_timer()

        self._render_text()
        self._update_stats()

        if self._current_word_idx >= len(self._words):
            self._finish()

    def _on_back_icon_pressed(self, sender):
        self.on_back_button_pressed.send(self)

    # ── Timer ──────────────────────────────────────────────────────────────────

    def _start_timer(self):
        self._running = True
        self._start_time = time.time()
        self._timer_thread = threading.Thread(target=self._timer_loop, daemon=True)
        self._timer_thread.start()

    def _timer_loop(self):
        while self._running:
            elapsed = time.time() - self._start_time
            self._time_left = max(0.0, self._test_duration - elapsed)
            remaining = int(self._time_left) + (1 if self._time_left > 0 else 0)
            if self.stat_label.winfo_exists():
                self.stat_label.after(
                    0, lambda r=remaining: self.stat_label.configure(text=str(r))
                )
            self._update_stats()
            if self._time_left <= 0:
                self._running = False
                self.stat_label.after(0, self._finish)
                break
            time.sleep(0.1)

    # ── Stats ──────────────────────────────────────────────────────────────────

    def _update_stats(self):
        if self._start_time is None:
            return
        elapsed = time.time() - self._start_time
        if elapsed < 0.3:
            return
        n = len(self._committed)
        total_chars = sum(len(self._words[i]) for i in range(n))
        correct_chars = sum(
            len(self._words[i]) for i, ok in enumerate(self._committed) if ok
        )
        wpm = int((correct_chars / 5) / (elapsed / 60))
        acc = int((correct_chars / total_chars) * 100) if total_chars else 100
        self._wpm = wpm
        self._acc = acc

        wpm_tpl = (
            self.language_manager.translate("typing_wpm_live_value") or "WPM: {wpm}"
        )
        acc_tpl = (
            self.language_manager.translate("typing_acc_live_value")
            or "Accuracy: {acc}%"
        )
        self.wpm_label.after(
            0, lambda: self.wpm_label.configure(text=wpm_tpl.format(wpm=wpm))
        )
        self.acc_label.after(
            0, lambda: self.acc_label.configure(text=acc_tpl.format(acc=acc))
        )

    # ── Render ─────────────────────────────────────────────────────────────────

    def _theme_colors(self):
        mode = ctk.get_appearance_mode()
        if mode == "Dark":
            return self._UNTYPED_DARK, self._ACTIVE_FG_D, self._ACTIVE_BG_D
        return self._UNTYPED_LITE, self._ACTIVE_FG_L, self._ACTIVE_BG_L

    def _render_text(self):
        untyped, active_fg, active_bg = self._theme_colors()
        tb = self.text_canvas
        tb.configure(state="normal")
        tb.delete("1.0", "end")

        tb.tag_config("correct_word", foreground=self._CORRECT_W)
        tb.tag_config("incorrect_word", foreground=self._INCORRECT_W)
        tb.tag_config("untyped", foreground=untyped)
        tb.tag_config("cur_ok", foreground=self._CORRECT_C)
        tb.tag_config("cur_err", foreground=self._INCORRECT_C)
        tb.tag_config("cur_untyped", foreground=active_fg)
        tb.tag_config("active_bg", background=active_bg)
        tb.tag_config("caret", foreground=self._CARET_FG, background=self._CARET_BG)

        typed = self._current_typed

        for w_idx, word in enumerate(self._words):
            if w_idx > 0:
                tb.insert("end", " ", "untyped")

            if w_idx < len(self._committed):
                tag = "correct_word" if self._committed[w_idx] else "incorrect_word"
                tb.insert("end", word, tag)

            elif w_idx == self._current_word_idx:
                for c_idx, ch in enumerate(word):
                    if c_idx < len(typed):
                        tag = "cur_ok" if typed[c_idx] == ch else "cur_err"
                        tb.insert("end", ch, (tag, "active_bg"))
                    elif c_idx == len(typed):
                        tb.insert("end", ch, ("caret",))
                    else:
                        tb.insert("end", ch, ("cur_untyped", "active_bg"))

                if len(typed) >= len(word):
                    tb.insert("end", " ", ("caret",))
                    for ex in typed[len(word) :]:
                        tb.insert("end", ex, ("cur_err", "active_bg"))
            else:
                tb.insert("end", word, "untyped")

        chars_before = sum(
            len(self._words[i]) + 1 for i in range(self._current_word_idx)
        )
        try:
            tb.see(f"1.0 + {chars_before} chars")
        except Exception:
            pass

        tb.configure(state="disabled")

    # ── Finish ─────────────────────────────────────────────────────────────────

    def _finish(self):
        if self._finished:
            return
        self._finished = True
        self._running = False
        self._update_stats()
        self.input_field.configure(state="disabled")
        self._result_wpm_val.configure(text=str(self._wpm))
        self._result_acc_val.configure(text=f"{self._acc}%")
        self._show_result_overlay()

    # ── Word bank loader ───────────────────────────────────────────────────────

    @staticmethod
    def _load_word_bank(json_path) -> list:
        """
        Load words from a JSON file.  Accepts two formats:
            ["word1", "word2", ...]
            {"words": ["word1", "word2", ...]}
        Falls back to the built-in list on any error.
        """
        if json_path is None:
            return TypingTestMenu._DEFAULT_WORDS
        path = pathlib.Path(json_path)
        if not path.exists():
            warnings.warn(
                f"TypingTestMenu: word bank not found at {path}, using built-in words"
            )
            return TypingTestMenu._DEFAULT_WORDS
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return [str(w) for w in data if w]
            if isinstance(data, dict) and "words" in data:
                return [str(w) for w in data["words"] if w]
            warnings.warn(
                "TypingTestMenu: unexpected word bank format, using built-in words"
            )
        except Exception as exc:
            warnings.warn(
                f"TypingTestMenu: failed to load word bank ({exc}), using built-in words"
            )
        return TypingTestMenu._DEFAULT_WORDS


class AmharicRainMenu(Menu):

    # ── Content ───────────────────────────────────────────────────────────────
    _LETTERS = list(
        "ሀሁሂሃሄህሆለሉሊላሌልሎሐሑሒሓሔሕሖመሙሚማሜምሞሠሡሢሣሤሥሦረሩሪራሬርሮሰሱሲሳሴስሶሸሹሺሻሼሽሾቀቁቂቃቄቅቆበቡቢባቤብቦቨቩቪቫቬቭቮተቱቲታቴትቶቸቹቺቻቼችቾኀኁኂኃኄኅኆነኑኒናኔንኖኘኙኚኛኜኝኞአኡኢኣኤእኦከኩኪካኬክኮኸኹኺኻኼኽኾወዉዊዋዌውዎዐዑዒዓዔዕዖዘዙዚዛዜዝዞዠዡዢዣዤዥዦየዩዪያዬይዮደዱዲዳዴድዶጀጁጂጃጄጅጆገጉጊጋጌግጎጠጡጢጣጤጥጦጨጩጪጫጬጭጮጰጱጲጳጴጵጶጸጹጺጻጼጽጾፀፁፂፃፄፅፆፈፉፊፋፌፍፎፐፑፒፓፔፕፖ"
    )
    _WORDS_DEFAULT = [
        "ሰላም",
        "ፍቅር",
        "ደስታ",
        "ሀገር",
        "ቤተሰብ",
        "ትምህርት",
        "ጸሐፊ",
        "ሙዚቃ",
        "ወርቅ",
        "ብርሃን",
        "ሰማይ",
        "ምድር",
        "ውሃ",
        "እሳት",
        "አየር",
        "አበባ",
        "ዛፍ",
        "ወንዝ",
        "ተራራ",
        "ሜዳ",
        "ቤት",
        "መንገድ",
        "ሰው",
        "ልጅ",
        "አባት",
        "እናት",
        "ወንድም",
        "እህት",
        "ጓደኛ",
        "አስተማሪ",
        "ተማሪ",
        "ዶክተር",
        "ቀን",
        "ሌሊት",
        "ጠዋት",
        "ምሽት",
        "ዓመት",
        "ወር",
        "ሳምንት",
        "ሰዓት",
        "ፀሐይ",
        "ጨረቃ",
        "ኮከብ",
        "ደመና",
        "ዝናብ",
        "ነፋስ",
        "በረዶ",
        "ሙቀት",
        "ስጋ",
        "ዳቦ",
        "ቡና",
        "ሻይ",
        "ወተት",
        "ፍሬ",
        "አትክልት",
        "ምግብ",
        "መጽሐፍ",
        "ብዕር",
        "ወረቀት",
        "ፊደል",
        "ቋንቋ",
        "ቃል",
    ]

    # ── Translations ──────────────────────────────────────────────────────────
    _T = {
        "en": {
            "title": "Amharic Rain",
            "subtitle": "Type the falling words before they hit the ground",
            "play": "Play",
            "settings": "Settings",
            "back_to_app": "Back",
            "mode_label": "Game Mode",
            "mode_letters": "Letters",
            "mode_words": "Words",
            "mode_both": "Both",
            "difficulty": "Difficulty",
            "diff_easy": "Easy",
            "diff_medium": "Medium",
            "diff_hard": "Hard",
            "volume": "Volume",
            "language": "Language",
            "lang_en": "English",
            "lang_am": "አማረኛ",
            "back": "Back",
            "score": "Score",
            "paused": "PAUSED",
            "resume": "Resume",
            "main_menu": "Main Menu",
            "game_over": "Game Over",
            "final_score": "Final Score",
            "play_again": "Play Again",
            "type_here": "Type here…",
            "pause": "Pause",
            "level": "Level",
            "lives": "Lives",
        },
        "am": {
            "title": "አማረኛ ዝናብ",
            "subtitle": "ቃላቱ ሳይወድቁ ጻፏቸው",
            "play": "ጀምር",
            "settings": "ቅንብሮች",
            "back_to_app": "ወደኋላ",
            "mode_label": "የጨዋታ ዓይነት",
            "mode_letters": "ፊደሎች",
            "mode_words": "ቃላት",
            "mode_both": "ሁለቱም",
            "difficulty": "ደረጃ",
            "diff_easy": "ቀላል",
            "diff_medium": "መካከለኛ",
            "diff_hard": "ከባድ",
            "volume": "ድምፅ",
            "language": "ቋንቋ",
            "lang_en": "English",
            "lang_am": "አማርኛ",
            "back": "ወደኋላ",
            "score": "ነጥብ",
            "paused": "ቆሟል",
            "resume": "ቀጥል",
            "main_menu": "ዋና ሜኒዩ",
            "game_over": "ጨዋታ አበቃ",
            "final_score": "የመጨረሻ ነጥብ",
            "play_again": "እንደገና ተጫወት",
            "type_here": "እዚህ ይጻፉ…",
            "pause": "አቁም",
            "level": "ደረጃ",
            "lives": "ህይወት",
        },
    }

    # ── Difficulty presets ────────────────────────────────────────────────────
    _DIFFICULTY = {
        "easy": {
            "start_speed": 0.55,
            "speed_inc": 0.015,
            "spawn_rate": 2.8,
            "spawn_dec": 0.08,
            "min_spawn": 1.2,
            "lives": 7,
        },
        "medium": {
            "start_speed": 0.85,
            "speed_inc": 0.025,
            "spawn_rate": 2.2,
            "spawn_dec": 0.12,
            "min_spawn": 0.8,
            "lives": 5,
        },
        "hard": {
            "start_speed": 1.20,
            "speed_inc": 0.040,
            "spawn_rate": 1.6,
            "spawn_dec": 0.18,
            "min_spawn": 0.5,
            "lives": 3,
        },
    }

    _INITIAL_SCORE = 25
    _SCORE_GAIN = 5
    _SCORE_LOSS = 4

    # ── Boss word constants ───────────────────────────────────────────────────
    _BOSS_COLOR = "#FFD700"  # gold
    _BOSS_OUTLINE = "#FF8C00"  # dark-orange glow shadow
    _BOSS_HIT_COLOR = "#FFF176"  # bright flash per hit
    _BOSS_FONT = ("Ebrima", 24, "bold")
    _BOSS_CHANCE = 0.15  # 15 % per spawn cycle
    _BOSS_SPEED_MULT = 0.90  # falls at 90 % of normal speed
    _BOSS_HITS = 3
    _HIT_DIGITS = ["❶", "❷", "❸", "❹", "❺"]

    # ── Palette ───────────────────────────────────────────────────────────────
    _BG_DARK = "#0a0d18"
    _BG_MID = "#131929"
    _BG_CARD = "#1c2240"
    _ACCENT = "#7c8cff"
    _ACCENT2 = "#a78bfa"
    _GREEN = "#4ade80"
    _RED = "#f87171"
    _TEXT_MAIN = "#e8eaf6"
    _TEXT_DIM = "#7b7fa8"
    _INPUT_BG = "#111827"
    _WORD_COLORS = [
        "#7c8cff",
        "#a78bfa",
        "#67e8f9",
        "#4ade80",
        "#fbbf24",
        "#fb7185",
        "#38bdf8",
        "#c084fc",
    ]

    # ── Fonts ─────────────────────────────────────────────────────────────────
    _F_TITLE = ("Segoe UI", 42, "bold")
    _F_SUBTITLE = ("Segoe UI", 15)
    _F_BTN = ("Segoe UI", 16, "bold")
    _F_LABEL = ("Segoe UI", 14)
    _F_WORD = ("Ebrima", 26, "bold")
    _F_WORD_SM = ("Ebrima", 20, "bold")
    _F_HUD = ("Segoe UI", 16, "bold")
    _F_INPUT = ("Ebrima", 22)
    _F_BIG = ("Segoe UI", 64, "bold")

    _STARS: list = []

    # ─────────────────────────────────────────────────────────────────────────

    def __init__(self, language_manager=None):
        self.language_manager = language_manager
        self.on_back_button_pressed = signal(f"amharic_rain_back_{id(self)}")

        self.lang = (
            "am" if getattr(language_manager, "current_lang", "en") == "am" else "en"
        )
        self.mode = "both"
        self.difficulty = "medium"
        self.volume = 0.7

        # Per-difficulty word banks; fall back to _WORDS_DEFAULT for any missing key
        self._word_bank: dict = {"easy": [], "medium": [], "hard": []}

        self.root = None  # set in open_menu(root)
        self.score = self._INITIAL_SCORE
        self.lives = 5
        self.level = 1
        self._paused = False
        self._running = False
        self._items: list = []
        self._boss: dict | None = None
        self._spawn_timer = 0.0
        self._level_timer = 0.0
        self._current_speed = 1.0
        self._spawn_interval = 2.0
        self._last_tick = 0.0
        self._tag_counter = 0
        self._pause_overlay_shown = False
        self._pause_frame = None
        self._pause_dim = None
        self._game_area = None
        self._sounds: dict = {}
        self._snd_ready = False

        self.main_frame = None
        self._canvas = None
        self._input_var = None
        self._input_entry = None
        self._score_label = None
        self._level_label = None
        self._lives_label = None
        self._pause_btn = None

    # ── Word bank API ─────────────────────────────────────────────────────────

    def load_word_bank(self, path: str) -> bool:
        """
        Load words from a JSON file.
        Expected format: {"easy": [...], "medium": [...], "hard": [...]}
        Any missing difficulty key falls back to _WORDS_DEFAULT at runtime.
        Returns True on success, False on failure.
        """
        import json

        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if isinstance(data, dict):
                for diff in ("easy", "medium", "hard"):
                    words = data.get(diff, [])
                    self._word_bank[diff] = [str(w) for w in words if str(w).strip()]
                return True
        except Exception as exc:
            print(f"[AmharicRain] load_word_bank failed: {exc}")
        self._word_bank = {"easy": [], "medium": [], "hard": []}
        return False

    def set_word_bank(self, bank: dict) -> None:
        """
        Directly set the word bank from a dict.
        Expected: {"easy": [...], "medium": [...], "hard": [...]}
        """
        for diff in ("easy", "medium", "hard"):
            words = bank.get(diff, []) if isinstance(bank, dict) else []
            self._word_bank[diff] = [str(w) for w in words if str(w).strip()]

    def _words_for_difficulty(self) -> list:
        """Return the word list for the current difficulty, falling back to the built-in default."""
        return self._word_bank.get(self.difficulty) or list(self._WORDS_DEFAULT)

    # ── Menu protocol (overrides Menu base) ──────────────────────────────────

    def open_menu(self, root):
        self.root = root
        if not self.main_frame:
            self.main_frame = ctk.CTkFrame(
                self.root, fg_color=self._BG_DARK, corner_radius=0
            )
        self.main_frame.place(
            relwidth=1, relheight=1, relx=0.5, rely=0.5, anchor="center"
        )
        self._show_game_menu()
        self.root.update_idletasks()

    def close_menu(self):
        self._running = False
        if self.main_frame:
            self.main_frame.place_forget()
        if self.root:
            self.root.update_idletasks()

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _t(self, key: str) -> str:
        return self._T[self.lang].get(key, key)

    def _clear(self):
        self._running = False
        for attr in ("_pause_frame", "_pause_dim"):
            w = getattr(self, attr, None)
            if w and w.winfo_exists():
                w.destroy()
            setattr(self, attr, None)
        self._game_area = None
        if self.main_frame:
            for w in self.main_frame.winfo_children():
                w.destroy()
        self._canvas = self._input_var = self._input_entry = None
        self._score_label = self._level_label = self._lives_label = self._pause_btn = (
            None
        )
        self._pause_overlay_shown = False

    def _exit_to_app(self):
        self.on_back_button_pressed.send(self)

    # ── Night-sky star field ──────────────────────────────────────────────────

    def _build_stars(self, w: int, h: int):
        import random as _r

        rng = _r.Random(42)
        self._STARS = []
        for _ in range(200):
            self._STARS.append(
                (rng.randint(0, w), rng.randint(0, h), 1, rng.uniform(0.3, 1.0))
            )
        for _ in range(30):
            self._STARS.append(
                (rng.randint(0, w), rng.randint(0, h), 2, rng.uniform(0.5, 1.0))
            )
        for _ in range(5):
            self._STARS.append((rng.randint(0, w), rng.randint(0, h), 3, 1.0))

    def _draw_stars(self, canvas):
        canvas.delete("stars")
        w = canvas.winfo_width() or 800
        h = canvas.winfo_height() or 600
        if not self._STARS:
            self._build_stars(w, h)
        for sx, sy, sz, alpha in self._STARS:
            v = int(alpha * 220) + 35
            color = f"#{v:02x}{v:02x}{min(255, v + 30):02x}"
            r = sz
            canvas.create_oval(
                sx - r, sy - r, sx + r, sy + r, fill=color, outline="", tags="stars"
            )

    # ══════════════════════════════════════════════════════════
    #  SOUND ENGINE
    # ══════════════════════════════════════════════════════════

    def _init_sound(self):
        if self._snd_ready:
            return
        try:
            import pygame
            import numpy as np

            if not pygame.mixer.get_init():
                pygame.mixer.pre_init(
                    frequency=44100, size=-16, channels=2, buffer=2048
                )
                pygame.mixer.init()
            if not pygame.mixer.get_init():
                return
            self._pg_mixer = pygame.mixer
            self._np = np
            self._sounds = {
                # gameplay
                "key": self._make_tone(880, 0.055, "sine", decay=0.5),
                "match": self._make_chord([523, 659, 784], 0.35, decay=0.45),
                "wrong": self._make_tone(180, 0.22, "square", decay=0.6),
                "miss": self._make_tone(220, 0.28, "sine", decay=0.7),
                "levelup": self._make_arp([523, 659, 784, 1047], 0.12),
                "gameover": self._make_arp([523, 440, 392, 294], 0.22, descend=True),
                # UI
                "btn": self._make_tone(660, 0.07, "sine", decay=0.8),
                "back": self._make_tone(440, 0.09, "sine", decay=0.7),
                "seg": self._make_tone(740, 0.06, "sine", decay=0.9),
                "slider": self._make_tone(1100, 0.035, "sine", decay=1.2),
            }
            pygame.mixer.set_num_channels(16)
            self._snd_ready = True
        except Exception:
            import traceback

            traceback.print_exc()
            self._snd_ready = False

    def _make_tone(self, freq, duration, shape="sine", decay=0.5, volume=0.6):
        try:
            import numpy as np, pygame

            sr = 44100
            n = int(sr * duration)
            t = np.linspace(0, duration, n, endpoint=False)
            if shape == "sine":
                wave = np.sin(2 * np.pi * freq * t)
            elif shape == "square":
                wave = np.sign(np.sin(2 * np.pi * freq * t)) * 0.5
            elif shape == "saw":
                wave = 2 * (t * freq - np.floor(t * freq + 0.5))
            else:
                wave = np.sin(2 * np.pi * freq * t)
            env = np.exp(-decay * t / max(duration, 1e-9) * 6)
            mono = (wave * env * volume * 32767).astype(np.int16)
            stereo = np.ascontiguousarray(np.column_stack([mono, mono]))
            return pygame.sndarray.make_sound(stereo)
        except Exception:
            return None

    def _make_chord(self, freqs, duration, decay=0.5, volume=0.45):
        try:
            import numpy as np, pygame

            sr = 44100
            t = np.linspace(0, duration, int(sr * duration), endpoint=False)
            wave = sum(np.sin(2 * np.pi * f * t) for f in freqs) / len(freqs)
            env = np.exp(-decay * t / max(duration, 1e-9) * 6)
            mono = (wave * env * volume * 32767).astype(np.int16)
            stereo = np.ascontiguousarray(np.column_stack([mono, mono]))
            return pygame.sndarray.make_sound(stereo)
        except Exception:
            return None

    def _make_arp(self, freqs, note_dur, descend=False, volume=0.55):
        try:
            import numpy as np, pygame

            sr = 44100
            samples = []
            for freq in freqs:
                t = np.linspace(0, note_dur, int(sr * note_dur), endpoint=False)
                wave = np.sin(2 * np.pi * freq * t)
                env = np.exp(-4 * t / max(note_dur, 1e-9))
                samples.append(wave * env)
            mono = (np.concatenate(samples) * volume * 32767).astype(np.int16)
            stereo = np.ascontiguousarray(np.column_stack([mono, mono]))
            return pygame.sndarray.make_sound(stereo)
        except Exception:
            return None

    def _on_volume_change(self, v: float, label):
        self.volume = v / 100
        label.configure(text=f"{int(v)}%")
        self._snd("slider")

    def _snd(self, name: str):
        if not self._snd_ready:
            return
        snd = self._sounds.get(name)
        if snd:
            try:
                vol = max(0.01, self.volume * 0.85)
                snd.set_volume(vol)
                ch = self._pg_mixer.find_channel(False)
                if ch:
                    ch.set_volume(vol)
                    ch.play(snd)
                else:
                    snd.play()
            except Exception:
                pass

    # ── Widget factories with built-in sounds ─────────────────────────────────

    def _btn(self, parent, *, sound="btn", command=None, **kwargs) -> ctk.CTkButton:
        def _cmd():
            self._snd(sound)
            if command:
                command()

        return ctk.CTkButton(parent, command=_cmd, **kwargs)

    def _seg(self, parent, *, on_change=None, **kwargs) -> ctk.CTkSegmentedButton:
        def _cmd(v):
            self._snd("seg")
            if on_change:
                on_change(v)

        return ctk.CTkSegmentedButton(parent, command=_cmd, **kwargs)

    # ══════════════════════════════════════════════════════════
    #  SCREENS
    # ══════════════════════════════════════════════════════════

    def _show_game_menu(self):
        self._clear()
        self._init_sound()

        bg_canvas = tk.Canvas(self.main_frame, bg=self._BG_DARK, highlightthickness=0)
        bg_canvas.place(relwidth=1, relheight=1)
        bg_canvas.update_idletasks()
        self._draw_stars(bg_canvas)
        bg_canvas.bind("<Configure>", lambda e, c=bg_canvas: self._draw_stars(c))

        outer = ctk.CTkFrame(self.main_frame, fg_color="transparent", corner_radius=0)
        outer.place(relwidth=1, relheight=1)
        outer.grid_rowconfigure(0, weight=1)
        outer.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(
            outer,
            fg_color=self._BG_MID,
            corner_radius=24,
            border_width=1,
            border_color=self._BG_CARD,
            bg_color="transparent",
        )
        card.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")
        card.grid_rowconfigure(list(range(8)), weight=1)
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkFrame(card, fg_color=self._ACCENT, height=6, corner_radius=3).grid(
            row=0, column=0, padx=60, pady=(32, 0), sticky="ew"
        )
        ctk.CTkLabel(
            card, text=self._t("title"), font=self._F_TITLE, text_color=self._TEXT_MAIN
        ).grid(row=1, column=0, pady=(18, 2))
        ctk.CTkLabel(
            card,
            text=self._t("subtitle"),
            font=self._F_SUBTITLE,
            text_color=self._TEXT_DIM,
        ).grid(row=2, column=0, pady=(0, 24))

        _b = dict(
            width=260, height=52, corner_radius=14, font=self._F_BTN, text_color="#fff"
        )
        self._btn(
            card,
            text=self._t("play"),
            command=self._show_setup,
            fg_color=self._ACCENT,
            hover_color="#5a6bff",
            sound="btn",
            **_b,
        ).grid(row=3, column=0, pady=8)
        self._btn(
            card,
            text=self._t("settings"),
            command=self._show_settings,
            fg_color=self._BG_CARD,
            hover_color="#2e3354",
            sound="btn",
            **_b,
        ).grid(row=4, column=0, pady=8)
        self._btn(
            card,
            text=self._t("back_to_app"),
            command=self._exit_to_app,
            fg_color="#2d1f2f",
            hover_color="#3d2040",
            sound="back",
            **_b,
        ).grid(row=5, column=0, pady=8)

        lang_row = ctk.CTkFrame(card, fg_color="transparent")
        lang_row.grid(row=6, column=0, pady=(16, 28))
        ctk.CTkLabel(
            lang_row,
            text=self._t("language") + ":",
            font=self._F_LABEL,
            text_color=self._TEXT_DIM,
        ).pack(side="left", padx=8)

        def _lang_change(v):
            self._snd("seg")
            self.lang = "am" if v in ("አማርኛ", "አማረኛ") else "en"
            self._show_game_menu()

        ctk.CTkSegmentedButton(
            lang_row,
            values=[self._t("lang_en"), self._t("lang_am")],
            command=_lang_change,
            font=self._F_LABEL,
            selected_color=self._ACCENT,
            selected_hover_color="#5a6bff",
            unselected_color=self._BG_CARD,
            fg_color=self._BG_CARD,
        ).pack(side="left")

    def _show_settings(self):
        self._clear()

        bg_canvas = tk.Canvas(self.main_frame, bg=self._BG_DARK, highlightthickness=0)
        bg_canvas.place(relwidth=1, relheight=1)
        bg_canvas.update_idletasks()
        self._draw_stars(bg_canvas)
        bg_canvas.bind("<Configure>", lambda e, c=bg_canvas: self._draw_stars(c))

        outer = ctk.CTkFrame(self.main_frame, fg_color="transparent", corner_radius=0)
        outer.place(relwidth=1, relheight=1)
        outer.grid_rowconfigure(0, weight=1)
        outer.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(
            outer,
            fg_color=self._BG_MID,
            corner_radius=24,
            border_width=1,
            border_color=self._BG_CARD,
            bg_color="transparent",
        )
        card.grid(row=0, column=0, padx=60, pady=40, sticky="nsew")
        card.grid_columnconfigure(1, weight=1)

        def row_label(r, key):
            ctk.CTkLabel(
                card,
                text=self._t(key) + ":",
                font=self._F_LABEL,
                text_color=self._TEXT_DIM,
                anchor="e",
            ).grid(row=r, column=0, padx=(30, 12), pady=18, sticky="e")

        ctk.CTkLabel(
            card,
            text=self._t("settings"),
            font=self._F_TITLE,
            text_color=self._TEXT_MAIN,
        ).grid(row=0, column=0, columnspan=2, pady=(28, 8))

        row_label(1, "volume")
        vol_var = ctk.DoubleVar(value=self.volume * 100)
        vol_label = ctk.CTkLabel(
            card,
            text=f"{int(self.volume * 100)}%",
            font=self._F_LABEL,
            text_color=self._TEXT_MAIN,
        )
        vol_label.grid(row=1, column=2, padx=(0, 20))
        ctk.CTkSlider(
            card,
            from_=0,
            to=100,
            variable=vol_var,
            width=280,
            button_color=self._ACCENT,
            button_hover_color="#5a6bff",
            progress_color=self._ACCENT,
            command=lambda v: self._on_volume_change(float(v), vol_label),
        ).grid(row=1, column=1, padx=(0, 30), sticky="w")

        row_label(2, "language")

        def _on_lang_change(v):
            self._snd("seg")
            self.lang = "am" if v in ("አማርኛ", "አማረኛ", "Amharic") else "en"
            self._show_settings()

        lang_seg = ctk.CTkSegmentedButton(
            card,
            values=["English", "አማርኛ"],
            font=self._F_LABEL,
            selected_color=self._ACCENT,
            selected_hover_color="#5a6bff",
            unselected_color=self._BG_CARD,
            fg_color=self._BG_CARD,
            command=_on_lang_change,
        )
        lang_seg.set("አማርኛ" if self.lang == "am" else "English")
        lang_seg.grid(row=2, column=1, padx=(0, 30), sticky="w", pady=18)

        self._btn(
            card,
            text=self._t("back"),
            command=self._show_game_menu,
            width=200,
            height=48,
            corner_radius=14,
            font=self._F_BTN,
            fg_color=self._BG_CARD,
            hover_color="#2e3354",
            text_color=self._TEXT_MAIN,
            sound="back",
        ).grid(row=8, column=0, columnspan=3, pady=(18, 32))

    def _show_setup(self):
        self._clear()

        bg_canvas = tk.Canvas(self.main_frame, bg=self._BG_DARK, highlightthickness=0)
        bg_canvas.place(relwidth=1, relheight=1)
        bg_canvas.update_idletasks()
        self._draw_stars(bg_canvas)
        bg_canvas.bind("<Configure>", lambda e, c=bg_canvas: self._draw_stars(c))

        outer = ctk.CTkFrame(self.main_frame, fg_color="transparent", corner_radius=0)
        outer.place(relwidth=1, relheight=1)
        outer.grid_rowconfigure(0, weight=1)
        outer.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(
            outer,
            fg_color=self._BG_MID,
            corner_radius=24,
            border_width=1,
            border_color=self._BG_CARD,
            bg_color="transparent",
        )
        card.grid(row=0, column=0, padx=60, pady=40, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card, text=self._t("play"), font=self._F_TITLE, text_color=self._TEXT_MAIN
        ).grid(row=0, column=0, pady=(28, 8))
        ctk.CTkLabel(
            card,
            text=self._t("mode_label"),
            font=self._F_LABEL,
            text_color=self._TEXT_DIM,
        ).grid(row=1, column=0, pady=(12, 4))

        def _on_mode(v):
            self._snd("seg")
            self.mode = (
                "letters"
                if v in (self._t("mode_letters"), "Letters", "ፊደሎች")
                else "words" if v in (self._t("mode_words"), "Words", "ቃላት") else "both"
            )

        mode_seg = ctk.CTkSegmentedButton(
            card,
            values=[
                self._t("mode_letters"),
                self._t("mode_words"),
                self._t("mode_both"),
            ],
            font=self._F_BTN,
            selected_color=self._ACCENT,
            selected_hover_color="#5a6bff",
            unselected_color=self._BG_CARD,
            fg_color=self._BG_CARD,
            command=_on_mode,
        )
        mode_seg.set(self._t(f"mode_{self.mode}"))
        mode_seg.grid(row=2, column=0, padx=40, pady=(4, 20), sticky="ew")

        ctk.CTkLabel(
            card,
            text=self._t("difficulty"),
            font=self._F_LABEL,
            text_color=self._TEXT_DIM,
        ).grid(row=3, column=0, pady=(0, 4))

        def _on_diff(v):
            self._snd("seg")
            self.difficulty = (
                "easy"
                if v in (self._t("diff_easy"), "Easy", "ቀላል")
                else "hard" if v in (self._t("diff_hard"), "Hard", "ከባድ") else "medium"
            )

        diff_seg = ctk.CTkSegmentedButton(
            card,
            values=[self._t("diff_easy"), self._t("diff_medium"), self._t("diff_hard")],
            font=self._F_BTN,
            selected_color=self._ACCENT2,
            selected_hover_color="#7c5bfa",
            unselected_color=self._BG_CARD,
            fg_color=self._BG_CARD,
            command=_on_diff,
        )
        diff_seg.set(self._t(f"diff_{self.difficulty}"))
        diff_seg.grid(row=4, column=0, padx=40, pady=(4, 32), sticky="ew")

        _b = dict(
            width=240, height=52, corner_radius=14, font=self._F_BTN, text_color="#fff"
        )
        self._btn(
            card,
            text=self._t("play"),
            command=self._start_game,
            fg_color=self._ACCENT,
            hover_color="#5a6bff",
            sound="btn",
            **_b,
        ).grid(row=5, column=0, pady=6)
        self._btn(
            card,
            text=self._t("back"),
            command=self._show_game_menu,
            fg_color=self._BG_CARD,
            hover_color="#2e3354",
            sound="back",
            **_b,
        ).grid(row=6, column=0, pady=(6, 32))

    # ══════════════════════════════════════════════════════════
    #  GAME
    # ══════════════════════════════════════════════════════════

    def _start_game(self):
        self._boss = None
        self._items.clear()
        self.score = self._INITIAL_SCORE
        self.lives = self._DIFFICULTY[self.difficulty]["lives"]
        self.level = 1
        self._paused = False
        self._tag_counter = 0
        self._pause_overlay_shown = False
        d = self._DIFFICULTY[self.difficulty]
        self._current_speed = d["start_speed"]
        self._spawn_interval = d["spawn_rate"]
        self._spawn_timer = 0.0
        self._level_timer = 0.0
        self._last_tick = time.time()
        self._clear()
        self._running = True
        self._init_sound()
        self._build_game_ui()
        self._tick()

    def _build_game_ui(self):
        outer = self.main_frame
        for i in range(3):
            outer.grid_rowconfigure(i, weight=1 if i == 1 else 0)
        outer.grid_columnconfigure(0, weight=1)

        hud = ctk.CTkFrame(outer, fg_color=self._BG_MID, height=56, corner_radius=0)
        hud.grid(row=0, column=0, sticky="ew")
        hud.grid_columnconfigure(2, weight=1)
        hud.grid_propagate(False)

        self._score_label = ctk.CTkLabel(
            hud,
            text=f"{self._t('score')}: {self.score}",
            font=self._F_HUD,
            text_color=self._GREEN,
        )
        self._score_label.grid(row=0, column=0, padx=24, pady=12, sticky="w")

        self._level_label = ctk.CTkLabel(
            hud,
            text=f"{self._t('level')}: {self.level}",
            font=self._F_HUD,
            text_color=self._ACCENT,
        )
        self._level_label.grid(row=0, column=1, padx=12, pady=12, sticky="w")

        self._lives_label = ctk.CTkLabel(
            hud, text="♥ " * self.lives, font=("Segoe UI", 15), text_color=self._RED
        )
        self._lives_label.grid(row=0, column=2, padx=12, pady=12, sticky="w")

        self._pause_btn = self._btn(
            hud,
            text=self._t("pause"),
            command=self._toggle_pause,
            width=110,
            height=34,
            corner_radius=10,
            font=("Segoe UI", 13, "bold"),
            fg_color=self._BG_CARD,
            hover_color="#2e3354",
            text_color=self._TEXT_MAIN,
            sound="btn",
        )
        self._pause_btn.grid(row=0, column=3, padx=(0, 20), pady=10, sticky="e")

        self._game_area = ctk.CTkFrame(outer, fg_color=self._BG_DARK, corner_radius=0)
        self._game_area.grid(row=1, column=0, sticky="nsew")
        self._game_area.grid_rowconfigure(0, weight=1)
        self._game_area.grid_columnconfigure(0, weight=1)

        self._canvas = tk.Canvas(
            self._game_area, bg=self._BG_DARK, highlightthickness=0
        )
        self._canvas.grid(row=0, column=0, sticky="nsew")

        def _on_canvas_configure(e):
            self._STARS = []
            self._draw_stars(self._canvas)
            self._draw_danger_line()

        self._canvas.bind("<Configure>", _on_canvas_configure)
        self._canvas.after(
            50, lambda: (self._draw_stars(self._canvas), self._draw_danger_line())
        )

        inp = ctk.CTkFrame(outer, fg_color=self._BG_MID, height=68, corner_radius=0)
        inp.grid(row=2, column=0, sticky="ew")
        inp.grid_columnconfigure(0, weight=1)
        inp.grid_propagate(False)

        self._input_var = tk.StringVar()
        self._input_var.trace_add("write", self._on_input_change)

        self._input_entry = ctk.CTkEntry(
            inp,
            textvariable=self._input_var,
            placeholder_text=self._t("type_here"),
            font=self._F_INPUT,
            fg_color=self._INPUT_BG,
            border_color=self._ACCENT,
            border_width=2,
            text_color=self._TEXT_MAIN,
            corner_radius=12,
            height=46,
        )
        self._input_entry.grid(row=0, column=0, padx=24, pady=11, sticky="ew")
        self._input_entry.focus()
        self._input_entry.bind("<Return>", lambda e: self._submit_input())

    def _draw_danger_line(self):
        if not self._canvas or not self._canvas.winfo_exists():
            return
        w, h = self._canvas.winfo_width(), self._canvas.winfo_height()
        self._canvas.delete("dangerline")
        self._canvas.create_line(
            0,
            h - 72,
            w,
            h - 72,
            fill=self._RED,
            width=2,
            dash=(8, 6),
            tags="dangerline",
        )

    # ── Input handling ────────────────────────────────────────────────────────

    def _on_input_change(self, *_):
        if not self._running or self._paused or not self._canvas:
            return
        typed = self._input_var.get()
        if typed:
            self._snd("key")

        for item in self._items:
            color = (
                self._GREEN
                if (not item["matched"] and item["text"].startswith(typed) and typed)
                else item["color"]
            )
            self._canvas.itemconfig(item["tag"], fill=color)

        if self._boss and typed:
            color = (
                self._BOSS_HIT_COLOR
                if self._boss["text"].startswith(typed)
                else self._BOSS_COLOR
            )
            self._canvas.itemconfig(self._boss["tag"], fill=color)

    def _submit_input(self):
        typed = self._input_var.get().strip()
        if not typed:
            return

        # Boss check first
        if self._boss and self._boss["text"] == typed:
            self._boss["hits"] += 1
            hits = self._boss["hits"]
            if hits >= self._BOSS_HITS:
                self._boss_success()
            else:
                new_label = self._boss_label(self._boss["text"], hits)
                for t in (
                    self._boss["tag"],
                    self._boss["glow_tag"],
                    self._boss["glow_tag2"],
                ):
                    try:
                        self._canvas.itemconfig(t, text=new_label)
                    except Exception:
                        pass
                self._flash_boss_hit()
                self._snd("match")
            self._input_var.set("")
            return

        # Normal items
        matched = False
        for item in list(self._items):
            if item["text"] == typed:
                self._items.remove(item)
                self._canvas.delete(item["tag"])
                self.score += self._SCORE_GAIN
                self._update_hud()
                self._spawn_burst(item["x"], item["y"], item["color"])
                self._snd("match")
                matched = True
                break
        if not matched:
            self._snd("wrong")
        self._input_var.set("")

    # ── Particles ─────────────────────────────────────────────────────────────

    def _spawn_burst(self, x: float, y: float, color: str):
        for _ in range(8):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(20, 60)
            dx, dy = math.cos(angle) * speed, math.sin(angle) * speed
            tag = f"p_{time.time()}_{random.random()}"
            r = random.randint(3, 7)
            self._canvas.create_oval(
                x - r, y - r, x + r, y + r, fill=color, outline="", tags=tag
            )
            self._anim_particle(tag, x, y, dx, dy, 6)

    def _anim_particle(self, tag, x, y, dx, dy, steps):
        if not self._canvas or not self._canvas.winfo_exists() or steps <= 0:
            self._canvas and self._canvas.delete(tag)
            return
        nx, ny = x + dx * 0.15, y + dy * 0.15
        self._canvas.move(tag, dx * 0.15, dy * 0.15)
        self._canvas.after(
            25,
            lambda: self._anim_particle(
                tag, nx, ny, dx * 0.85, dy * 0.85 + 2, steps - 1
            ),
        )

    # ══════════════════════════════════════════════════════════
    #  BOSS WORDS
    # ══════════════════════════════════════════════════════════

    def _boss_label(self, text: str, hits: int) -> str:
        filled = "".join(self._HIT_DIGITS[i] for i in range(hits))
        remaining = "○" * (self._BOSS_HITS - hits)
        return f"★ {text}  {filled}{remaining}"

    def _spawn_boss(self, canvas_w: int):
        words = self._words_for_difficulty()
        pool = [w for w in words if len(w) >= 3] or words
        text = random.choice(pool)

        x = random.randint(60, max(61, canvas_w - 60))
        self._tag_counter += 1
        base_tag = f"boss_{self._tag_counter}"
        glow_tag = f"bossglow_{self._tag_counter}"
        glow_tag2 = f"bossglow2_{self._tag_counter}"

        label = self._boss_label(text, 0)

        self._canvas.create_text(
            x + 2,
            -28,
            text=label,
            font=self._BOSS_FONT,
            fill=self._BOSS_OUTLINE,
            tags=glow_tag2,
            anchor="center",
        )
        self._canvas.create_text(
            x,
            -30,
            text=label,
            font=self._BOSS_FONT,
            fill=self._BOSS_OUTLINE,
            tags=glow_tag,
            anchor="center",
        )
        self._canvas.create_text(
            x,
            -30,
            text=label,
            font=self._BOSS_FONT,
            fill=self._BOSS_COLOR,
            tags=base_tag,
            anchor="center",
        )

        self._boss = {
            "text": text,
            "x": float(x),
            "y": -30.0,
            "speed": self._current_speed * self._BOSS_SPEED_MULT,
            "hits": 0,
            "tag": base_tag,
            "glow_tag": glow_tag,
            "glow_tag2": glow_tag2,
        }

    def _boss_success(self):
        if not self._boss:
            return
        bx, by = self._boss["x"], self._boss["y"]
        self._remove_boss_canvas_items()
        self._boss = None

        self.lives = min(self.lives + 1, 10)
        self._update_hud()
        self._spawn_burst(bx, by, self._BOSS_COLOR)
        self._spawn_burst(bx - 20, by + 10, self._BOSS_HIT_COLOR)
        self._spawn_burst(bx + 20, by + 10, self._BOSS_HIT_COLOR)
        self._snd("levelup")

        try:
            self._lives_label.configure(text_color=self._BOSS_COLOR)
            self.root.after(
                600,
                lambda: (
                    self._lives_label.configure(text_color=self._RED)
                    if self._lives_label and self._lives_label.winfo_exists()
                    else None
                ),
            )
        except Exception:
            pass

    def _boss_miss(self, boss: dict):
        """Boss reached the danger line — disappear silently, no penalty."""
        self._remove_boss_canvas_items(boss)
        if self._boss is boss:
            self._boss = None

    def _remove_boss_canvas_items(self, boss: dict | None = None):
        b = boss if boss is not None else self._boss
        if b is None:
            return
        for key in ("tag", "glow_tag", "glow_tag2"):
            try:
                self._canvas.delete(b[key])
            except Exception:
                pass

    def _flash_boss_hit(self):
        if not self._boss:
            return
        try:
            self._canvas.itemconfig(self._boss["tag"], fill=self._BOSS_HIT_COLOR)
            tag = self._boss["tag"]
            self.root.after(
                180,
                lambda: (
                    self._canvas.itemconfig(tag, fill=self._BOSS_COLOR)
                    if self._canvas and self._canvas.winfo_exists()
                    else None
                ),
            )
        except Exception:
            pass

    # ══════════════════════════════════════════════════════════
    #  GAME LOOP
    # ══════════════════════════════════════════════════════════

    def _tick(self):
        if not self._running:
            return
        now = time.time()
        dt = now - self._last_tick
        self._last_tick = now

        if self._paused:
            self.root.after(50, self._tick)
            return

        if not self._canvas or not self._canvas.winfo_exists():
            return

        w, h = self._canvas.winfo_width(), self._canvas.winfo_height()
        danger_y = h - 72

        self._spawn_timer += dt
        if self._spawn_timer >= self._spawn_interval:
            self._spawn_timer = 0.0
            self._spawn_item(w)

        self._level_timer += dt
        if self._level_timer >= 20.0:
            self._level_timer = 0.0
            self._level_up()

        fallen = []
        for item in self._items:
            item["y"] += item["speed"] * dt * 60
            self._canvas.coords(item["tag"], item["x"], item["y"])
            if item["y"] >= danger_y:
                fallen.append(item)

        for item in fallen:
            self._items.remove(item)
            self._canvas.delete(item["tag"])
            self.lives = max(0, self.lives - 1)
            self._update_hud()
            self._flash_score()
            self._snd("miss")

        if self._boss:
            self._boss["y"] += self._boss["speed"] * dt * 60
            ny, nx = self._boss["y"], self._boss["x"]
            self._canvas.coords(self._boss["tag"], nx, ny)
            self._canvas.coords(self._boss["glow_tag"], nx, ny)
            self._canvas.coords(self._boss["glow_tag2"], nx + 2, ny - 2)
            if ny >= danger_y:
                self._boss_miss(self._boss)

        if self.lives <= 0:
            self._game_over()
            return

        self.root.after(16, self._tick)

    def _spawn_item(self, canvas_w: int):
        if canvas_w < 10:
            return

        if self._boss is None and random.random() < self._BOSS_CHANCE:
            self._spawn_boss(canvas_w)
            return

        words = self._words_for_difficulty()
        if self.mode == "letters":
            text, font = random.choice(self._LETTERS), self._F_WORD
        elif self.mode == "words":
            text, font = random.choice(words), self._F_WORD_SM
        else:
            if random.random() < 0.45:
                text, font = random.choice(self._LETTERS), self._F_WORD
            else:
                text, font = random.choice(words), self._F_WORD_SM

        x = random.randint(40, max(41, canvas_w - 40))
        color = random.choice(self._WORD_COLORS)
        self._tag_counter += 1
        tag = f"item_{self._tag_counter}"
        self._canvas.create_text(
            x, -30, text=text, font=font, fill=color, tags=tag, anchor="center"
        )
        self._items.append(
            {
                "text": text,
                "x": float(x),
                "y": -30.0,
                "speed": self._current_speed,
                "color": color,
                "tag": tag,
                "matched": False,
            }
        )

    def _level_up(self):
        self.level += 1
        d = self._DIFFICULTY[self.difficulty]
        self._current_speed = min(
            self._current_speed + d["speed_inc"] * self.level, 4.5
        )
        self._spawn_interval = max(
            self._spawn_interval - d["spawn_dec"], d["min_spawn"]
        )
        self._update_hud()
        self._flash_level()
        self._snd("levelup")

    def _update_hud(self):
        if self._score_label and self._score_label.winfo_exists():
            self._score_label.configure(
                text=f"{self._t('score')}: {self.score}",
                text_color=self._GREEN if self.score > 0 else self._RED,
            )
            self._level_label.configure(text=f"{self._t('level')}: {self.level}")
            if self._lives_label and self._lives_label.winfo_exists():
                hearts = ("♥ " * self.lives).strip() or "☆"
                self._lives_label.configure(
                    text=hearts, text_color=self._RED if self.lives > 1 else "#ff4444"
                )

    def _flash_score(self):
        lbl = self._score_label
        if not lbl:
            return
        try:
            lbl.configure(text_color=self._RED)

            def _restore():
                if self._score_label and self._score_label.winfo_exists():
                    self._score_label.configure(
                        text_color=(
                            self._GREEN
                            if self.score > self._INITIAL_SCORE // 2
                            else self._RED
                        )
                    )

            self.root.after(300, _restore)
        except Exception:
            pass

    def _flash_level(self):
        lbl = self._level_label
        if not lbl:
            return
        try:
            lbl.configure(text_color=self._ACCENT2)

            def _restore():
                if self._level_label and self._level_label.winfo_exists():
                    self._level_label.configure(text_color=self._ACCENT)

            self.root.after(500, _restore)
        except Exception:
            pass

    # ── Pause ──────────────────────────────────────────────────────────────────

    def _toggle_pause(self):
        self._paused = not self._paused
        if self._paused:
            self._pause_btn.configure(text=self._t("resume"))
            self._show_pause_popup()
        else:
            self._hide_pause_popup()
            self._pause_btn.configure(text=self._t("pause"))
            self._last_tick = time.time()

    def _show_pause_popup(self):
        if not self.main_frame or not self.main_frame.winfo_exists():
            return
        self._pause_overlay_shown = True

        self._pause_dim = tk.Frame(self.main_frame, bg="#0a0d18")
        self._pause_dim.place(relwidth=1, relheight=1)
        self._pause_dim.lower()

        self._pause_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self._BG_MID,
            corner_radius=16,
            border_width=2,
            border_color=self._ACCENT,
        )
        self._pause_frame.place(relx=0.5, rely=0.5, anchor="center")

        inner = ctk.CTkFrame(self._pause_frame, fg_color="transparent")
        inner.pack(padx=40, pady=32)

        ctk.CTkLabel(
            inner,
            text=self._t("paused"),
            font=("Segoe UI", 32, "bold"),
            text_color=self._TEXT_MAIN,
        ).pack(pady=(0, 4))
        ctk.CTkLabel(
            inner,
            text="⏸  Game is paused",
            font=("Segoe UI", 13),
            text_color=self._TEXT_DIM,
        ).pack(pady=(0, 20))
        ctk.CTkFrame(
            inner, fg_color=self._BG_CARD, height=2, corner_radius=1, width=260
        ).pack(pady=(0, 20))

        _b = dict(
            width=260,
            height=48,
            corner_radius=12,
            font=("Segoe UI", 15, "bold"),
            text_color="#ffffff",
        )
        self._btn(
            inner,
            text="▶  " + self._t("resume"),
            command=self._toggle_pause,
            fg_color=self._ACCENT,
            hover_color="#5a6bff",
            sound="btn",
            **_b,
        ).pack(pady=(0, 10))

        _b2 = {k: v for k, v in _b.items() if k != "text_color"}
        self._btn(
            inner,
            text=self._t("main_menu"),
            command=lambda: (self._hide_pause_popup(), self._show_game_menu()),
            fg_color=self._BG_CARD,
            hover_color="#2e3354",
            text_color=self._TEXT_MAIN,
            sound="back",
            **_b2,
        ).pack(pady=(0, 4))

    def _hide_pause_popup(self):
        for attr in ("_pause_dim", "_pause_frame"):
            w = getattr(self, attr, None)
            if w and w.winfo_exists():
                w.destroy()
            setattr(self, attr, None)
        self._pause_overlay_shown = False

    # ── Game Over ──────────────────────────────────────────────────────────────

    def _game_over(self):
        if not self._running:
            return
        self._running = False
        self._boss = None
        self._snd("gameover")
        final_score, final_level = self.score, self.level
        self._clear()

        bg_canvas = tk.Canvas(self.main_frame, bg=self._BG_DARK, highlightthickness=0)
        bg_canvas.place(relwidth=1, relheight=1)
        bg_canvas.update_idletasks()
        self._draw_stars(bg_canvas)
        bg_canvas.bind("<Configure>", lambda e, c=bg_canvas: self._draw_stars(c))

        outer = ctk.CTkFrame(self.main_frame, fg_color="transparent", corner_radius=0)
        outer.place(relwidth=1, relheight=1)
        outer.grid_rowconfigure(0, weight=1)
        outer.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(
            outer,
            fg_color=self._BG_MID,
            corner_radius=24,
            border_width=1,
            border_color=self._BG_CARD,
            bg_color="transparent",
        )
        card.grid(row=0, column=0, padx=80, pady=60, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card, text=self._t("game_over"), font=self._F_BIG, text_color=self._RED
        ).grid(row=0, column=0, pady=(36, 8))
        ctk.CTkLabel(
            card,
            text=f"{self._t('final_score')}: {final_score}   |   {self._t('level')}: {final_level}",
            font=("Segoe UI", 20),
            text_color=self._TEXT_DIM,
        ).grid(row=1, column=0, pady=(0, 40))

        _b = dict(
            width=220, height=52, corner_radius=14, font=self._F_BTN, text_color="#fff"
        )
        self._btn(
            card,
            text=self._t("play_again"),
            command=self._start_game,
            fg_color=self._ACCENT,
            hover_color="#5a6bff",
            sound="btn",
            **_b,
        ).grid(row=2, column=0, pady=8)
        self._btn(
            card,
            text=self._t("main_menu"),
            command=self._show_game_menu,
            fg_color=self._BG_CARD,
            hover_color="#2e3354",
            sound="btn",
            **_b,
        ).grid(row=3, column=0, pady=8)
        self._btn(
            card,
            text=self._t("back_to_app"),
            command=self._exit_to_app,
            fg_color="#2d1f2f",
            hover_color="#3d2040",
            sound="back",
            **_b,
        ).grid(row=4, column=0, pady=(8, 36))
