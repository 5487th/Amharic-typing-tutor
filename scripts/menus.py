import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import customtkinter as ctk
from PIL import Image, ImageDraw
from tkinter import filedialog
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
        self._popup_frame = None

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
        self._popup_frame = None

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

        self.main_frame.configure(self.root, width=700, height=500)
        self.main_frame.pack_propagate(False)
        self.main_frame.propagate(False)

        # main frame tittle
        self.Create_a_user_label = CTkLabel(self.main_frame, font=("Roboto", 30))
        self.Create_a_user_label.pack(pady=20, side="top", fill="x")
        self.language_manager.register_widget(
            self.Create_a_user_label, "Create a new user"
        )

        # buttons
        self.buttons_frame = CTkFrame(
            self.main_frame, fg_color="transparent", width=390, height=40
        )
        self.buttons_frame.pack_propagate(False)
        self.buttons_frame.pack(side="bottom", pady=15, fill="x")

        self.create_button = CTkButton(
            self.buttons_frame,
            corner_radius=10,
            text="Create",
            width=250,
            height=40,
            command=self.on_create_user_button_pressed,
            font=("Roboto", 20),
        )
        self.language_manager.register_widget(self.create_button, "Create")
        self.create_button.pack(side="left", padx=50)

        self.cancel_button = CTkButton(
            self.buttons_frame,
            corner_radius=10,
            text="Cancel",
            width=250,
            height=40,
            command=self.on_cancel_user_creation_button_pressed,
            font=("Roboto", 20),
        )
        self.language_manager.register_widget(self.cancel_button, "Cancel")
        self.cancel_button.pack(side="right", padx=50)

        self.image_path = None
        if not self.image_path:
            self.image_path = self.user_manager.default_profile_picture_path

        self.profile_view_frame = CTkFrame(self.main_frame)
        self.profile_view_frame.pack(side="left", pady=10, padx=40)

        # profile button
        self.profile_button = ImageButton(
            self.profile_view_frame,
            dark_image_path=self.image_path,
            light_image_path=self.image_path,
            sizex=260,
            sizey=260,
        )
        self.profile_button.on_mouse_click.connect(self.on_profile_clicked)
        self.profile_button.pack(side="left", pady=10, padx=10)

        # reset profile button
        reset_dark_icon = (
            pathlib.Path(__file__).parent.parent
            / "assets"
            / "images"
            / "icons"
            / "reset_icon_black.png"
        )
        reset_white_icon = (
            pathlib.Path(__file__).parent.parent
            / "assets"
            / "images"
            / "icons"
            / "reset_icon_white.png"
        )

        self.reset_button = ImageButton(
            self.profile_view_frame,
            dark_image_path=reset_white_icon,
            light_image_path=reset_dark_icon,
            sizex=40,
            sizey=40,
            size_change_amount=1,
        )
        self.reset_button.on_mouse_click.connect(self.on_reset_profile_clicked)
        self.reset_button.place(relx=0.99, rely=0.01, anchor="ne")

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

        user_profile_path = self.user_manager.default_profile_picture_path
        if self.image_path and pathlib.Path(self.image_path).exists():
            user_profile_path = self.image_path

        image_object = self.circular_crop(user_profile_path)

        save_dir = pathlib.Path(__file__).parent.parent / "data" / "profile_pictures"

        save_path = save_dir / f"{random.randint(0, 100000000)}_profile_picture.png"
        if is_valid_username:
            save_path = save_dir / f"{stripped_username}_profile_picture.png"

        profile_picture_path = self.user_manager.default_profile_picture_path
        if image_object:
            save_dir.mkdir(parents=True, exist_ok=True)
            image_object.save(save_path, format="PNG")
            profile_picture_path = save_path
            print("so dis did happen")

        if is_valid_username and (
            is_password_atleast_four_characters_long
            and has_numbers
            and has_atleast_three_letters
        ):
            self.user_manager.create_user(
                stripped_username, stripped_password, str(profile_picture_path)
            )
            self.on_user_created.send(self, username=stripped_username)

        elif is_valid_username and (is_password_empty):
            self.user_manager.create_user(
                stripped_username, "", str(profile_picture_path)
            )
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

    def on_profile_clicked(self, sender):
        profile_path = filedialog.askopenfilename(
            title="Select Profile Image",
            initialdir=os.path.expanduser("~/Pictures"),  # Start in Photos directory
            filetypes=[
                ("Image files", ("*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp")),
                ("All files", "*.*"),
            ],
        )

        if not profile_path:
            return

        self.image_path = profile_path
        self.profile_button.set_image(
            self.circular_crop(self.image_path), self.circular_crop(self.image_path)
        )

    def circular_crop(self, image_path, size=None):
        # Open the image
        img = Image.open(image_path).convert("RGBA")

        # Make the image square by cropping to the smallest dimension
        width, height = img.size
        min_dim = min(width, height)
        left = (width - min_dim) // 2
        top = (height - min_dim) // 2
        right = left + min_dim
        bottom = top + min_dim
        img = img.crop((left, top, right, bottom))

        # Optionally resize to a fixed size (e.g. for your button)
        if size:
            img = img.resize((size, size), Image.LANCZOS)

        # Create circular mask
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, img.size[0], img.size[1]), fill=255)

        # Apply mask
        result = Image.new("RGBA", img.size)
        result.paste(img, (0, 0), mask=mask)

        return result

    def on_reset_profile_clicked(self, sender):
        self.profile_button.set_image_by_path(
            self.user_manager.default_profile_picture_path,
            self.user_manager.default_profile_picture_path,
        )


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
        self.on_amharic_race_activity_card_icon_pressed = signal(
            f"on amharic race acvtivity icon button presed {self}"
        )
        self.on_amharic_dodge_activity_card_icon_pressed = signal(
            f"on amharic dodge acvtivity icon button presed {self}"
        )

    def open_menu(self):
        if not self.user_manager.current_user:
            warnings.warn("no user logged in, cant open main menu")
            return

        self.main_frame = CTkFrame(self.root, fg_color="transparent")

        self.header_Frame = CTkFrame(self.main_frame, height=10, fg_color="transparent")
        self.header_Frame.pack(fill="x")

        # profile button
        user_profile_image_path = self.user_manager.default_profile_picture_path
        if (
            self.user_manager.current_user.profile_picture_path
            and pathlib.Path(
                self.user_manager.current_user.profile_picture_path
            ).exists()
        ):
            user_profile_image_path = (
                self.user_manager.current_user.profile_picture_path
            )

        self.user_profile_button = ImageButton(
            self.header_Frame,
            light_image_path=user_profile_image_path,
            dark_image_path=user_profile_image_path,
            sizex=30,
            sizey=30,
            size_change_amount=1,
        )
        self.user_profile_button.on_mouse_click.connect(
            self.on_user_profile_icon_pressed
        )
        self.user_profile_button.pack(side="left", padx=10, pady=10)

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

        # -----------------------amharic rain--------------------------
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

        # -----------------------amharic race--------------------------
        self.Amharic_race_game_activity_card: ActivityCard = ActivityCard(
            self.main_scrollable_frame,
            str(
                pathlib.Path(__file__).parent.parent
                / "assets"
                / "images"
                / "amharic_typing_racer_icon.png"
            ),
            "Amharic typing Race",
            "you are in a typing race, with 3 other cars. type out the provided phargraph before the other cars and grab your crown!",
        )
        self.Amharic_race_game_activity_card.pack()

        self.language_manager.register_widget(
            self.Amharic_race_game_activity_card.tittle_label, "Amharic typing Race"
        )
        self.language_manager.register_widget(
            self.Amharic_race_game_activity_card.discription_label,
            "you are in a typing race, with 3 other cars. type out the provided phargraph before the other cars and grab your crown!",
        )

        self.Amharic_race_game_activity_card.on_start_button_pressed.connect(
            self.on_Amharic_race_activity_button_pressed
        )
        # -----------------------amharic dodge--------------------------
        self.Amharic_dodge_game_activity_card: ActivityCard = ActivityCard(
            self.main_scrollable_frame,
            str(
                pathlib.Path(__file__).parent.parent
                / "assets"
                / "images"
                / "amharic_dodge_icon.png"
            ),
            "Dodge the cars",
            "you find yourself driving the wrong direction on a highway! you must now dodge the incoming cars, using your keyboard",
        )
        self.Amharic_dodge_game_activity_card.pack()

        self.language_manager.register_widget(
            self.Amharic_dodge_game_activity_card.tittle_label, "Dodge the cars"
        )
        self.language_manager.register_widget(
            self.Amharic_dodge_game_activity_card.discription_label,
            "you find yourself driving the wrong direction on a highway! you must now dodge the incoming cars, using your keyboard",
        )

        self.Amharic_dodge_game_activity_card.on_start_button_pressed.connect(
            self.on_Amharic_dodge_activity_button_pressed
        )

    def on_typing_test_activity_button_pressed(self, sender):
        self.on_amharic_typing_test_activity_card_icon_pressed.send(self)

    def on_Amharic_rain_activity_button_pressed(self, sender):
        self.on_amharic_rain_activity_card_icon_pressed.send(self)

    def on_Amharic_race_activity_button_pressed(self, sender):
        self.on_amharic_race_activity_card_icon_pressed.send(self)

    def on_Amharic_dodge_activity_button_pressed(self, sender):
        self.on_amharic_dodge_activity_card_icon_pressed.send(self)


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


class UserSettingsMenu(Menu):
    def __init__(self, root, user_manager, language_manager):
        super().__init__()
        if not root:
            warnings.warn(
                "attempted to create user settings menu with None root, "
                "user settings menu not created"
            )
            return
        if not user_manager:
            warnings.warn(
                "attempted to create user settings menu with None user manager, "
                "user settings menu not created"
            )
            return
        if not language_manager:
            warnings.warn(
                "attempted to create user settings menu with None language manager, "
                "user settings menu not created"
            )
            return

        self.root = root
        self.language_manager = language_manager
        self.user_manager = user_manager

        self.on_back_button_pressed = signal(f"on_back_button_pressed{self}")
        self.on_account_deleted = signal(f"on_account_deleted{self}")

        self._frame: ctk.CTkFrame = None
        self._avatar_canvas: ctk.CTkCanvas = None
        self._avatar_photo = None  # must keep reference to prevent GC
        self._feedback_label: ctk.CTkLabel = None

    # -----------------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------------

    def open_menu(self):
        if self._frame and self._frame.winfo_exists():
            self._frame.lift()
            return
        self._build_ui()
        self._frame.pack(fill="both", expand=True)

    def close_menu(self):
        if self._frame and self._frame.winfo_exists():
            self._frame.pack_forget()
            self._frame.destroy()
            self._frame = None

    # -----------------------------------------------------------------------
    # UI construction
    # -----------------------------------------------------------------------

    def _build_ui(self):
        lm = self.language_manager
        user = self.user_manager.current_user

        self._frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")

        # ── Top bar ────────────────────────────────────────────────────────
        top_bar = ctk.CTkFrame(self._frame, height=48, corner_radius=0)
        top_bar.pack(fill="x", side="top")
        top_bar.pack_propagate(False)

        _back_icon_black = (
            pathlib.Path(__file__).parent.parent
            / "assets"
            / "images"
            / "icons"
            / "back_icon_black.png"
        )
        _back_icon_white = (
            pathlib.Path(__file__).parent.parent
            / "assets"
            / "images"
            / "icons"
            / "back_icon_white.png"
        )
        if _back_icon_black.exists() and _back_icon_white.exists():
            _back_img = ctk.CTkImage(
                light_image=Image.open(_back_icon_black),
                dark_image=Image.open(_back_icon_white),
                size=(28, 28),
            )
            ctk.CTkButton(
                top_bar,
                text="",
                image=_back_img,
                width=36,
                height=36,
                fg_color="transparent",
                hover_color=("gray85", "gray25"),
                command=self._on_back,
            ).pack(side="left", padx=10, pady=6)
        else:
            ctk.CTkButton(
                top_bar,
                text="← Back",
                width=80,
                height=32,
                fg_color="transparent",
                hover_color=("gray85", "gray25"),
                anchor="w",
                command=self._on_back,
            ).pack(side="left", padx=12, pady=8)

        title_label = ctk.CTkLabel(
            top_bar,
            text=lm.translate("Settings"),
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        title_label.pack(side="left", padx=4)
        lm.register_widget(title_label, "Settings")

        # ── Scrollable content ─────────────────────────────────────────────
        scroll = ctk.CTkScrollableFrame(
            self._frame, corner_radius=0, fg_color="transparent"
        )
        scroll.pack(fill="both", expand=True)

        inner = ctk.CTkFrame(scroll, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=32, pady=20)

        # ── Profile picture card ───────────────────────────────────────────
        pic_card = self._make_card(inner)
        pic_card.pack(fill="x", pady=(0, 16))

        pic_heading = ctk.CTkLabel(
            pic_card,
            text=lm.translate("Profile picture"),
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        )
        pic_heading.pack(anchor="w", padx=20, pady=(16, 12))
        lm.register_widget(pic_heading, "Profile picture")

        avatar_row = ctk.CTkFrame(pic_card, fg_color="transparent")
        avatar_row.pack(fill="x", padx=20, pady=(0, 16))

        # Avatar canvas (circular)
        self._avatar_canvas = ctk.CTkCanvas(
            avatar_row,
            width=90,
            height=90,
            highlightthickness=0,
            bd=0,
        )
        self._avatar_canvas.pack(side="left")
        self._draw_avatar(self._resolve_profile_picture(user))

        btn_col = ctk.CTkFrame(avatar_row, fg_color="transparent")
        btn_col.pack(side="left", padx=20, anchor="center")

        _choose_btn = ctk.CTkButton(
            btn_col,
            text=lm.translate("settings_choose_photo"),
            width=160,
            command=self._change_profile_picture,
        )
        _choose_btn.pack(anchor="w", pady=(0, 8))
        lm.register_widget(_choose_btn, "settings_choose_photo")

        _reset_btn = ctk.CTkButton(
            btn_col,
            text=lm.translate("settings_reset_photo"),
            width=160,
            fg_color="transparent",
            border_width=1,
            command=self._reset_profile_picture,
        )
        _reset_btn.pack(anchor="w")
        lm.register_widget(_reset_btn, "settings_reset_photo")

        # ── Password card ──────────────────────────────────────────────────
        pw_card = self._make_card(inner)
        pw_card.pack(fill="x", pady=(0, 16))

        pw_heading = ctk.CTkLabel(
            pw_card,
            text=lm.translate("Password"),
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        )
        pw_heading.pack(anchor="w", padx=20, pady=(16, 4))
        lm.register_widget(pw_heading, "Password")

        _pw_desc = ctk.CTkLabel(
            pw_card,
            text=lm.translate("settings_pw_description"),
            font=ctk.CTkFont(size=12),
            text_color=("gray45", "gray65"),
            anchor="w",
            wraplength=380,
            justify="left",
        )
        _pw_desc.pack(anchor="w", padx=20, pady=(0, 12))
        lm.register_widget(_pw_desc, "settings_pw_description")

        _change_pw_btn = ctk.CTkButton(
            pw_card,
            text=lm.translate("settings_change_password_btn"),
            width=180,
            command=self._open_change_password_dialog,
        )
        _change_pw_btn.pack(anchor="w", padx=20, pady=(0, 16))
        lm.register_widget(_change_pw_btn, "settings_change_password_btn")

        # ── Danger zone card ───────────────────────────────────────────────
        danger_card = self._make_card(inner, danger=True)
        danger_card.pack(fill="x", pady=(0, 16))

        _danger_heading = ctk.CTkLabel(
            danger_card,
            text=lm.translate("settings_danger_zone"),
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#E05252",
            anchor="w",
        )
        _danger_heading.pack(anchor="w", padx=20, pady=(16, 4))
        lm.register_widget(_danger_heading, "settings_danger_zone")

        _danger_desc = ctk.CTkLabel(
            danger_card,
            text=lm.translate("settings_danger_description"),
            font=ctk.CTkFont(size=12),
            text_color=("gray45", "gray65"),
            anchor="w",
            wraplength=380,
            justify="left",
        )
        _danger_desc.pack(anchor="w", padx=20, pady=(0, 12))
        lm.register_widget(_danger_desc, "settings_danger_description")

        _delete_btn = ctk.CTkButton(
            danger_card,
            text=lm.translate("settings_delete_account_btn"),
            width=180,
            fg_color="#C0392B",
            hover_color="#922B21",
            command=self._open_delete_account_dialog,
        )
        _delete_btn.pack(anchor="w", padx=20, pady=(0, 16))
        lm.register_widget(_delete_btn, "settings_delete_account_btn")

        # ── Feedback label ─────────────────────────────────────────────────
        self._feedback_label = ctk.CTkLabel(inner, text="", font=ctk.CTkFont(size=12))
        self._feedback_label.pack(pady=(4, 0))

    # -----------------------------------------------------------------------
    # Avatar drawing
    # -----------------------------------------------------------------------

    def _draw_avatar(self, image_path):
        size = 90
        try:
            p = pathlib.Path(image_path)
            img = Image.open(p).convert("RGBA")
            # Square-crop to the smallest dimension (same as SignUpMenu.circular_crop)
            w, h = img.size
            min_dim = min(w, h)
            left = (w - min_dim) // 2
            top = (h - min_dim) // 2
            img = img.crop((left, top, left + min_dim, top + min_dim))
            raw = img.resize((size, size), Image.LANCZOS)
        except Exception:
            raw = Image.new("RGBA", (size, size), (100, 100, 100, 255))

        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
        result = Image.new("RGBA", (size, size))
        result.paste(raw, (0, 0), mask=mask)

        # Walk up the widget tree to find the nearest non-transparent real color
        bg = "#2b2b2b"
        try:
            widget = self._avatar_canvas.master
            while widget is not None:
                color = widget.cget("fg_color")
                color = color[1] if isinstance(color, (list, tuple)) else color
                if color and color != "transparent":
                    bg = color
                    break
                widget = widget.master
        except Exception:
            pass

        self._avatar_canvas.configure(bg=bg)
        self._avatar_photo = ImageTk.PhotoImage(result)
        self._avatar_canvas.delete("all")
        self._avatar_canvas.create_image(size // 2, size // 2, image=self._avatar_photo)

    # -----------------------------------------------------------------------
    # Change-password dialog (built inline as a CTkToplevel)
    # -----------------------------------------------------------------------

    def _open_change_password_dialog(self):
        lm = self.language_manager
        um = self.user_manager

        # ── Dark scrim ──────────────────────────────────────────────────────
        overlay = ctk.CTkFrame(
            self._frame, fg_color=("gray20", "gray10"), corner_radius=0
        )
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        # ── Auto-sizing centered card ────────────────────────────────────────
        card = ctk.CTkFrame(overlay, corner_radius=12)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            card,
            text=lm.translate("settings_change_password_title"),
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(pady=(20, 14), padx=32)

        lbl_cur = ctk.CTkLabel(
            card, text=lm.translate("settings_current_password"), anchor="w"
        )
        lbl_cur.pack(fill="x", padx=28, pady=(0, 2))
        lm.register_widget(lbl_cur, "settings_current_password")
        current_entry = ctk.CTkEntry(card, show="•", width=300)
        current_entry.pack(padx=28, pady=(0, 10))

        lbl_new = ctk.CTkLabel(
            card, text=lm.translate("settings_new_password"), anchor="w"
        )
        lbl_new.pack(fill="x", padx=28, pady=(0, 2))
        lm.register_widget(lbl_new, "settings_new_password")
        new_entry = ctk.CTkEntry(card, show="•", width=300)
        new_entry.pack(padx=28, pady=(0, 10))

        lbl_conf = ctk.CTkLabel(
            card, text=lm.translate("settings_confirm_password"), anchor="w"
        )
        lbl_conf.pack(fill="x", padx=28, pady=(0, 2))
        lm.register_widget(lbl_conf, "settings_confirm_password")
        confirm_entry = ctk.CTkEntry(card, show="•", width=300)
        confirm_entry.pack(padx=28, pady=(0, 8))

        error_label = ctk.CTkLabel(
            card, text="", text_color="#E05252", font=ctk.CTkFont(size=12)
        )
        error_label.pack(pady=(0, 8))

        def _submit():
            current = current_entry.get()
            new_pw = new_entry.get()
            confirm = confirm_entry.get()
            user = um.current_user
            if not um.is_Correct_password(user.password, current):
                error_label.configure(text="Current password is incorrect.")
                return
            if len(new_pw) != 0 and len(new_pw) < 4:
                error_label.configure(
                    text="New password must be ≥ 4 characters or empty."
                )
                return
            if new_pw != confirm:
                error_label.configure(text="Passwords do not match.")
                return
            um.change_user_password(user.username, new_pw)
            overlay.destroy()
            self._show_feedback("Password changed successfully.")

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(fill="x", padx=28, pady=(0, 20))

        cancel_btn = ctk.CTkButton(
            btn_row,
            text=lm.translate("Cancel"),
            width=136,
            fg_color="transparent",
            border_width=1,
            command=overlay.destroy,
        )
        cancel_btn.pack(side="left", padx=(0, 6))
        lm.register_widget(cancel_btn, "Cancel")

        save_btn = ctk.CTkButton(
            btn_row,
            text=lm.translate("settings_save"),
            width=136,
            command=_submit,
        )
        save_btn.pack(side="left", padx=(6, 0))
        lm.register_widget(save_btn, "settings_save")

        current_entry.focus_set()

    # -----------------------------------------------------------------------
    # Delete-account dialog (built inline as a CTkToplevel)
    # -----------------------------------------------------------------------

    def _open_delete_account_dialog(self):
        user = self.user_manager.current_user
        if not user:
            return

        lm = self.language_manager
        um = self.user_manager

        # ── Dark scrim ──────────────────────────────────────────────────────
        overlay = ctk.CTkFrame(
            self._frame, fg_color=("gray20", "gray10"), corner_radius=0
        )
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        # ── Auto-sizing centered card ────────────────────────────────────────
        card = ctk.CTkFrame(overlay, corner_radius=12)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            card,
            text=lm.translate("settings_delete_account_title"),
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#E05252",
        ).pack(pady=(20, 6), padx=32)

        ctk.CTkLabel(
            card,
            text=f'"{user.username}"',
            font=ctk.CTkFont(size=13),
            wraplength=280,
        ).pack(pady=(0, 4), padx=32)

        _confirm_desc = ctk.CTkLabel(
            card,
            text=lm.translate("settings_delete_confirm_desc"),
            font=ctk.CTkFont(size=12),
            text_color=("gray45", "gray65"),
            wraplength=280,
        )
        _confirm_desc.pack(pady=(0, 12), padx=32)
        lm.register_widget(_confirm_desc, "settings_delete_confirm_desc")

        # ── Password confirmation field ──────────────────────────────────────
        pw_label = ctk.CTkLabel(
            card,
            text=lm.translate("settings_current_password"),
            anchor="w",
        )
        pw_label.pack(fill="x", padx=28, pady=(0, 2))
        lm.register_widget(pw_label, "settings_current_password")

        pw_entry = ctk.CTkEntry(card, show="•", width=280)
        pw_entry.pack(padx=28, pady=(0, 8))

        error_label = ctk.CTkLabel(
            card, text="", text_color="#E05252", font=ctk.CTkFont(size=12)
        )
        error_label.pack(pady=(0, 8))

        def _confirm():
            entered = pw_entry.get()
            if not um.is_Correct_password(user.password, entered):
                error_label.configure(text="Incorrect password.")
                pw_entry.configure(border_width=2, border_color="#E05252")
                return
            overlay.destroy()
            username = user.username
            um.logout()
            um.delete_user(username)
            self.close_menu()
            self.on_account_deleted.send(self, user=user)

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(fill="x", padx=28, pady=(0, 20))

        cancel_btn = ctk.CTkButton(
            btn_row,
            text=lm.translate("Cancel"),
            width=120,
            fg_color="transparent",
            border_width=1,
            command=overlay.destroy,
        )
        cancel_btn.pack(side="left", padx=(0, 6))
        lm.register_widget(cancel_btn, "Cancel")

        ctk.CTkButton(
            btn_row,
            text=lm.translate("settings_delete_btn"),
            width=120,
            fg_color="#C0392B",
            hover_color="#922B21",
            command=_confirm,
        ).pack(side="left", padx=(6, 0))

        pw_entry.focus_set()

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    def _make_card(self, parent, danger=False):
        border_color = ("#FFCCCC", "#5C2020") if danger else ("gray80", "gray25")
        return ctk.CTkFrame(
            parent, corner_radius=10, border_width=1, border_color=border_color
        )

    def _resolve_profile_picture(self, user):
        if user and user.profile_picture_path:
            p = pathlib.Path(user.profile_picture_path)
            if p.exists() and p.is_file():
                return str(p)
        return str(self.user_manager.default_profile_picture_path)

    def _show_feedback(self, text, color="#4CAF50"):
        if self._feedback_label and self._feedback_label.winfo_exists():
            self._feedback_label.configure(text=text, text_color=color)
            self._frame.after(3000, self._clear_feedback)

    def _clear_feedback(self):
        if self._feedback_label and self._feedback_label.winfo_exists():
            self._feedback_label.configure(text="")

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------

    def _on_back(self):
        self.on_back_button_pressed.send(self)
        self.close_menu()

    def circular_crop(self, image_path, size=None):
        img = Image.open(image_path).convert("RGBA")
        width, height = img.size
        min_dim = min(width, height)
        left = (width - min_dim) // 2
        top = (height - min_dim) // 2
        img = img.crop((left, top, left + min_dim, top + min_dim))
        if size:
            img = img.resize((size, size), Image.LANCZOS)
        mask = Image.new("L", img.size, 0)
        ImageDraw.Draw(mask).ellipse((0, 0, img.size[0], img.size[1]), fill=255)
        result = Image.new("RGBA", img.size)
        result.paste(img, (0, 0), mask=mask)
        return result

    def _change_profile_picture(self):
        path = filedialog.askopenfilename(
            parent=self.root,
            title="Choose a profile picture",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.webp")],
        )
        if not path:
            return

        user = self.user_manager.current_user

        # Delete the old cropped file if it's inside profile_pictures/ (not the default)
        old_path = (
            pathlib.Path(user.profile_picture_path)
            if user.profile_picture_path
            else None
        )
        profile_pictures_dir = (
            pathlib.Path(__file__).parent.parent / "data" / "profile_pictures"
        )
        if old_path and old_path.exists() and profile_pictures_dir in old_path.parents:
            try:
                old_path.unlink()
            except Exception:
                pass

        # Crop circularly and save into profile_pictures/
        cropped = self.circular_crop(path)
        profile_pictures_dir.mkdir(parents=True, exist_ok=True)
        save_path = profile_pictures_dir / f"{user.username}_profile_picture.png"
        cropped.save(save_path, format="PNG")

        self.user_manager.change_user_profile_picture(user.username, str(save_path))
        self._draw_avatar(str(save_path))
        self._show_feedback("Profile picture updated.")

    def _reset_profile_picture(self):
        user = self.user_manager.current_user

        # Delete the old cropped file if it lives in profile_pictures/
        old_path = (
            pathlib.Path(user.profile_picture_path)
            if user.profile_picture_path
            else None
        )
        profile_pictures_dir = (
            pathlib.Path(__file__).parent.parent / "data" / "profile_pictures"
        )
        if old_path and old_path.exists() and profile_pictures_dir in old_path.parents:
            try:
                old_path.unlink()
            except Exception:
                pass

        default = str(self.user_manager.default_profile_picture_path)
        self.user_manager.change_user_profile_picture(user.username, default)
        self._draw_avatar(default)
        self._show_feedback("Profile picture reset to default.")
