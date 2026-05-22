import customtkinter as ctk
from blinker import signal
from scripts.user_manager import UserManager, User
from scripts.language_manager import LanguageManager
from scripts.custom_widgets import *


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

    def open_menu(self):
        self.main_frame = CTkFrame(self.root, fg_color="transparent")

        # languages selection drop down
        self.languages = ["English", "አማርኛ"]
        self.language_dropdown = ctk.CTkOptionMenu(
            self.main_frame,
            values=self.languages,
            command=self.on_languge_drop_down_value_changed,
        )

        # choose a user label
        self.choose_a_user_label = ctk.CTkLabel(self.main_frame, font=("Roboto", 40))
        self.language_manager.register_widget(
            self.choose_a_user_label, "Welcome, login or create a user"
        )

        # user icons frame
        self.user_icons_frame = ctk.CTkFrame(
            self.main_frame, bg_color="transparent", fg_color="transparent"
        )

        # placing the widgets down
        self.language_dropdown.place(relx=0.01, rely=0.015)
        self.choose_a_user_label.place(rely=0.2, relx=0.5, anchor="center")
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
        if self.language_manager:
            if value == "English":
                self.language_manager.set_language(
                    self.language_manager.ENGLISH_LANGUAGE_KEY
                )
            if value == "አማርኛ":
                self.language_manager.set_language(
                    self.language_manager.AMHARIC_LANGUAGE_KEY
                )

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
        self.user_manager = user_manager

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

        is_username_unique = not self.user_manager.User_exists(stripped_username)
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
        is_username_unique = not self.user_manager.User_exists(username)
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

        self.on_settings_button_pressed = signal(f"on settings icon clicked {self}")
        self.on_help_button_pressed = signal(f"on help icon clicker {self}")
        self.on_user_logged_out = signal(f"on log out button pressed {self}")

    def open_menu(self):
        if not self.user_manager.current_user:
            warnings.warn("no user logged in, cant open main menu")
            return

        self.main_frame = CTkFrame(self.root, fg_color="transparent")

        self.header_Frame = CTkFrame(self.main_frame, height=20, fg_color="transparent")
        self.header_Frame.pack(fill="x")

        # settings button
        settings_button_image_path = (
            pathlib.Path(__file__).parent.parent
            / "assets"
            / "images"
            / "settings_icon.png"
        )
        self.settings_button = ImageButton(
            self.header_Frame,
            image_path=settings_button_image_path,
            sizex=25,
            sizey=25,
            size_change_amount=1,
        )
        self.settings_button.on_mouse_click.connect(self.on_settings_icon_pressed)
        self.settings_button.pack(side="left", padx=10, pady=10)

        # help button
        help_button_image_path = (
            pathlib.Path(__file__).parent.parent / "assets" / "images" / "help_icon.png"
        )
        self.help_button = ImageButton(
            self.header_Frame,
            image_path=help_button_image_path,
            sizex=25,
            sizey=25,
            size_change_amount=1,
        )
        self.help_button.on_mouse_click.connect(self.on_help_icon_pressed)
        self.help_button.pack(side="left", padx=0, pady=10)

        # log out button
        logout_button_image_path = (
            pathlib.Path(__file__).parent.parent
            / "assets"
            / "images"
            / "log_out_icon.png"
        )
        self.logout_button = ImageButton(
            self.header_Frame,
            image_path=logout_button_image_path,
            sizex=25,
            sizey=25,
            size_change_amount=1,
        )
        self.logout_button.on_mouse_click.connect(self.on_logout_icon_pressed)
        self.logout_button.pack(side="left", padx=10, pady=10)

        self.main_scrollable_frame = CTkScrollableFrame(
            self.main_frame, corner_radius=0
        )

        self.main_scrollable_frame.pack(expand=True, fill="both")

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

    def close_menu(self):
        self.main_frame.place_forget()

    def on_settings_icon_pressed(self, sender):
        self.on_settings_button_pressed.send(self)

    def on_help_icon_pressed(self, sender):
        self.on_help_button_pressed.send(self)

    def on_logout_icon_pressed(self, sender):
        self.header_Frame.pack_forget()
        self.main_scrollable_frame.pack_forget()
        self.log_out_confirmation_popup.place(relx=0.5, rely=0.5, anchor="center")

    def on_logout_confirmation_button_pressed(self, sender, user):
        self.user_manager.logout()
        self.on_user_logged_out.send(self, user=user)

    def on_cancel_logout_button_pressed(self, sender):
        self.header_Frame.pack(fill="x")
        self.main_scrollable_frame.pack(expand=True, fill="both")
        self.log_out_confirmation_popup.place_forget()


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
            self.main_frame.pack()
        self.header_frame = CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.pack(fill="x", side="top")

        back_button_path = (
            pathlib.Path(__file__).parent.parent / "assets" / "images" / "back_icon.png"
        )
        if not self.back_button:
            self.back_button = ImageButton(self.header_frame, back_button_path, 30, 30)
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
            self.pdf_viewer.pack(expand=True, fill="both", side="bottom")
        if pathlib.Path(pdf_path).exists():
            self.pdf_viewer.load(pdf_path)

    def close_menu(self):
        self.main_frame.place_forget()

    def on_back_icon_pressed(self, sender):
        self.on_back_button_pressed.send(self)
