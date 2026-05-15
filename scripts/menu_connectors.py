import customtkinter as ctk
from scripts.menus import *
import warnings


class LoginToSignupConnector:
    def __init__(self, login_menu: LoginMenu, signup_menu: SignUpMenu):
        if not login_menu:
            warnings.warn(
                "attempted to create a login to sign up menu connetor with None login menu"
            )
            return
        if not signup_menu:
            warnings.warn(
                "attempted to crate a login to sign up menu connetor with None sign up menu"
            )
            return
        self.login_menu = login_menu
        self.signup_menu = signup_menu

        self.login_menu.on_add_user_button_pressed.connect(
            self.on_add_user_button_pressed
        )
        self.signup_menu.on_cancel_button_pressed.connect(
            self.on_cancel_or_create_pressed
        )
        self.signup_menu.on_user_created.connect(self.on_cancel_or_create_pressed)

    def on_add_user_button_pressed(self, sender, **kwargs):
        self.login_menu.close_menu()
        self.signup_menu.open_menu()

    def on_cancel_or_create_pressed(self, sender, **kwargs):
        self.signup_menu.username_entery_field.delete(0, "end")
        self.signup_menu.password_entery_field.delete(0, "end")

        self.signup_menu.username_character_unqieness_requirement_label.configure(
            text_color="red"
        )
        self.signup_menu.username_character_length_requirement_label.configure(
            text_color="red"
        )
        self.signup_menu.password_character_length_requirement_label.configure(
            text="green"
        )
        self.signup_menu.password_character_type_requirements_label.configure(
            text="green"
        )

        self.signup_menu.close_menu()
        self.login_menu.open_menu()


class LoginToMainMenuConnector:
    def __init__(
        self,
        root: ctk.CTk,
        login_menu: LoginMenu,
        main_menu: MainMenu,
        language_manager: LanguageManager,
        user_manager: UserManager,
    ):
        if not root:
            warnings.warn(
                "attempted to create a login to main menu connector with None root"
            )
            return
        if not login_menu:
            warnings.warn(
                "attempted to create a login to main menu connector with None login menu"
            )
            return
        if not main_menu:
            warnings.warn(
                "attempted to crate a login to main menu connector with None main menu"
            )
            return
        if not language_manager:
            warnings.warn(
                "attempted to crate a login to main menu connector with None language manager"
            )
            return
        if not user_manager:
            warnings.warn(
                "attempted to crate a login to main menu connector with None user manager"
            )
            return

        self.login_menu = login_menu
        self.main_menu = main_menu
        self.language_manager = language_manager
        self.use_manager = user_manager
        self.root = root

        self.login_menu.on_user_logged_in.connect(self.on_user_logged_in)

    def on_user_logged_in(self, sender, user):
        self.login_menu.close_menu()

        self.transition_screen = logging_in_transition_screen(
            self.language_manager, self.use_manager, self.root
        )
        self.transition_screen.place(relx=0.5, rely=0.5, anchor="center")
        self.root.update_idletasks()
        self.root.after(2700, self.end_transition_screen)

    def end_transition_screen(self):
        self.transition_screen.place_forget()
        self.main_menu.open_menu()
