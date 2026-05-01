import customtkinter as ctk
from blinker import signal

from scripts.user_manager import UserManager, User
from scripts.language_manager import LanguageManager
from scripts.reusable_custom_widgets import *

class Menu:
    def open_menu(self, root):
        pass

    def close_menu(self):
        pass

class UserloginSignupScreen(Menu):
    def __init__(self, root, _language_manager:LanguageManager, _user_manager:UserManager):
        self.language_manager = _language_manager
        self.user_manager = _user_manager
        self.root=root
    
    def open_menu(self):
        #languages selection drop down
        self.languages = ["English", "አማርኛ"]
        self.language_dropdown = ctk.CTkOptionMenu(self.root,values=self.languages,command=self.on_languge_drop_down_value_changed)
        self.language_dropdown.place(relx=0.01, rely=0.015)

        #choose a user label
        self.choose_a_user_label = ctk.CTkLabel(self.root,font=("Roboto", 40))
        self.language_manager.register_widget(self.choose_a_user_label,"Welcome, login or create a user")
        self.choose_a_user_label.place(rely=0.2,relx=0.5,anchor="center")
        
        #user icons frame
        self.user_icons_frame = ctk.CTkFrame(self.root, bg_color="transparent", fg_color="transparent")
        self.user_icons_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.user_icons = []

        self.update_user_icon_display()

        self.user_manager.on_user_created.connect(self.on_user_icons_display_need_to_be_updated)
        self.user_manager.on_user_deleted.connect(self.on_user_icons_display_need_to_be_updated)
        self.user_manager.on_user_changed_username.connect(self.on_user_icons_display_need_to_be_updated)

        self.user_creation_menu = UserCreationMenu(self.language_manager, self.user_manager, self.root)
    
    def close_menu(self):
        if self.language_dropdown:
            self.language_dropdown.place_forget()
        if self.choose_a_user_label:
            self.choose_a_user_label.place_forget()
        if self.user_icons_frame:
            self.user_icons_frame.place_forget()
        
    #singup login screen 
    def on_user_icons_display_need_to_be_updated(self, sender, **kwargs):
        self.update_user_icon_display()
        
    def update_user_icon_display(self):
        for widget in self.user_icons_frame.winfo_children():
            widget.destroy()

        self.user_icons = []
        for user in self.user_manager.get_all_users():
            user_icon = UserLoginIcon(self.user_icons_frame, self.user_manager, user)
            user_icon.pack_propagate(False)
            user_icon.pack(side = "left", padx = 1)
            user_icon.on_user_pressed_icon.connect(self.on_user_icon_presesd)
            self.user_icons.append(user_icon)
        
        self.add_user_Button = ctk.CTkButton(self.user_icons_frame,width=150,height=190,corner_radius=10, text="+", text_color="white", font=("Roboto",40),command=self.on_plus_button_pressed)
        self.add_user_Button.pack(side ="left", padx = 1)

    def on_languge_drop_down_value_changed(self, value):
        if self.language_manager:
            if value == "English":
                self.language_manager.set_language(self.language_manager.ENGLISH_LANGUAGE_KEY)
            if value == "አማርኛ":
                self.language_manager.set_language(self.language_manager.AMHARIC_LANGUAGE_KEY)
    
    def on_plus_button_pressed(self):
        self.user_icons_frame.place_forget()
        self.choose_a_user_label.place_forget()

        self.user_creation_menu.place(rely=0.5, relx=0.5, anchor="center")

        self.user_creation_menu.username_character_unqieness_requirement_label.configure(text_color="red")
        self.user_creation_menu.username_character_length_requirement_label.configure(text_color="red")
        self.user_creation_menu.password_character_type_requirements_label.configure(text_color="red")
        self.user_creation_menu.password_character_length_requirement_label.configure(text_color="red")

        self.user_creation_menu.on_create_button_pressed.connect(self.on_create_user_button_pressed)
        self.user_creation_menu.on_cancel_button_pressed.connect(self.on_cancel_button_pressed)
        
        self.user_creation_menu.on_user_type_in_username_entery.connect(self.on_user_type_into_username_entery)
        self.user_creation_menu.on_user_type_in_password_entery.connect(self.on_user_type_into_password_entery)
        self.on_user_type_into_password_entery(self, "")

    def on_user_icon_presesd(self, sender, user):
        if user.password == "":
            self.user_manager.login(user)
        else:
            self.user_icons_frame.place_forget()
            self.choose_a_user_label.place_forget()

            self.user_login_menu = UserloginMenu(user, self.language_manager, self.user_manager, self.root)
            self.user_login_menu.place(relx=0.5,rely=0.5,anchor="center")
            
            self.user_login_menu.on_cancel_login_button_pressed.connect(self.on_cancel_login_button_pressed)
            self.user_login_menu.on_login_button_pressed.connect(self.on_login_button_pressed)
   
   #login menu
    def on_login_button_pressed(self, sender, user, entered_password):
        hashed_password=user.password

        if self.user_manager.is_Correct_password(hashed_password, entered_password):
            self.user_manager.login(user)
            print("correct")
            self.user_login_menu.password_entery_field.configure(border_width=0)

        else:
            self.user_login_menu.password_entery_field.configure(border_width=3, border_color="red")

    def on_cancel_login_button_pressed(self, sender):
        self.user_login_menu.password_entery_field.delete(0,"end")
        self.user_login_menu.password_entery_field.configure(border_width=0)
        
        self.user_login_menu.place_forget()


        self.choose_a_user_label.place(rely=0.2,relx=0.5,anchor="center")
        self.user_icons_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.update_user_icon_display()
   
    #user creation menu
    def on_create_user_button_pressed(self, sender, username, password):
            stripped_username = username.strip()
            stripped_password = password.strip()

            is_username_unique = not self.user_manager.User_exists(stripped_username)
            is_username_in_proper_range_of_characters = (len(stripped_username) <= 12 and len(stripped_username) >= 4)

            is_password_atleast_four_characters_long = len(stripped_password) >= 4
            is_password_empty = len(stripped_password) == 0

            has_numbers = any(char.isdigit() for char in stripped_password)
            has_atleast_three_letters = sum(char.isalpha() for char in stripped_password) >= 3

            is_valid_username = (is_username_unique and is_username_in_proper_range_of_characters)
              
            if is_valid_username and (is_password_atleast_four_characters_long and has_numbers and has_atleast_three_letters):
                self.user_manager.create_user(stripped_username, stripped_password)
                self.on_cancel_button_pressed(self)
            elif is_valid_username and (is_password_empty):
                self.user_manager.create_user(stripped_username, "")
                self.on_cancel_button_pressed(self)

    def on_cancel_button_pressed(self, sender):
        self.choose_a_user_label.place(rely=0.2,relx=0.5,anchor="center")
        self.user_icons_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.update_user_icon_display()

        self.user_creation_menu.username_entery_field.delete(0,"end")
        self.user_creation_menu.password_entery_field.delete(0, "end")
        self.user_creation_menu.place_forget()

        self.user_creation_menu.username_character_unqieness_requirement_label.configure(text_color="red")
        self.user_creation_menu.username_character_length_requirement_label.configure(text_color="red")

    def on_user_type_into_username_entery(self, sender, username):
        is_username_unique = self.user_manager.User_exists(username)
        is_username_in_proper_range_of_characters = (len(username) <= 12 and len(username) >= 4)
        is_valid_username = (is_username_unique and is_username_in_proper_range_of_characters)

        if is_username_unique:
            self.user_creation_menu.username_character_unqieness_requirement_label.configure(text_color="green")
        else:
            self.user_creation_menu.username_character_unqieness_requirement_label.configure(text_color="red")
        
        if is_username_in_proper_range_of_characters:
            self.user_creation_menu.username_character_length_requirement_label.configure(text_color="green")
        else:
            self.user_creation_menu.username_character_length_requirement_label.configure(text_color="red")

    def on_user_type_into_password_entery(self, sender, password):
        is_password_atleast_four_characters_long = len(password) >= 4
        is_password_empty = len(password) == 0
        is_password_valid = is_password_empty and is_password_atleast_four_characters_long

        has_numbers = any(char.isdigit() for char in password)
        has_atleast_three_letters = sum(char.isalpha() for char in password) >= 3

        if (has_numbers and has_atleast_three_letters) or is_password_empty:
            self.user_creation_menu.password_character_type_requirements_label.configure(text_color="green")
        else:
            self.user_creation_menu.password_character_type_requirements_label.configure(text_color="red")
        
        if is_password_empty:
            self.user_creation_menu.password_character_length_requirement_label.configure(text_color="green")
        elif is_password_atleast_four_characters_long:
            self.user_creation_menu.password_character_length_requirement_label.configure(text_color="green")
        else:
            self.user_creation_menu.password_character_length_requirement_label.configure(text_color="red")
