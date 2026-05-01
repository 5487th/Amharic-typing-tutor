from customtkinter import *
import warnings
from blinker import signal
from PIL import Image
import pathlib

from scripts.user_manager import User
from scripts.user_manager import UserManager
from scripts.language_manager import LanguageManager

class UserLoginIcon(CTkFrame):
    def __init__(self, master, user_manager:UserManager, user:User, **kwargs):
        super().__init__(master, **kwargs)
        if not user:
            warnings.warn("attempted to create user login icon with no user, user icon not created")
            return
        
        self.user = user
        self.master = master
        self.on_user_pressed_icon = signal(f"on_user_pressed_{self.user.username}_icon")
        self.user_manager = user_manager

        self.configure(width=150,height=190,corner_radius=10)
        self.pack_propagate(False)

        self.bind("<Enter>",self.on_mouse_entered)
        self.bind("<Leave>", self.on_mouse_exit)
        self.bind("<Button-1>", self.on_mouse_clicked)

        if pathlib.Path(user.profile_picture_path).exists():
            image_object = Image.open(user.profile_picture_path)
            ctk_image=CTkImage(light_image=image_object, dark_image=image_object, size=(120, 120)) 
            self.profile_picture = CTkLabel(self, text="", image=ctk_image)
        else:
            image_object = Image.open(self.user_manager.default_profile_picture_path)
            ctk_image=CTkImage(light_image=image_object, dark_image=image_object, size=(120, 120))
            self.profile_picture=CTkLabel(self,text="", image=ctk_image)        
        
        self.profile_picture.pack(pady=10)
        self.profile_picture.bind("<Enter>",self.on_mouse_entered)
        self.profile_picture.bind("<Leave>", self.on_mouse_exit)
        self.profile_picture.bind("<Button-1>", self.on_mouse_clicked)

        self.label_background = CTkFrame(self, corner_radius=10,width=135,height=35)
        self.label_background.pack(side="bottom",pady=8)
        self.label_background.pack_propagate(False)

        self.label_background.bind("<Enter>",self.on_mouse_entered)
        self.label_background.bind("<Leave>", self.on_mouse_exit)
        self.label_background.bind("<Button-1>", self.on_mouse_clicked)

        self.username_label = CTkLabel(self.label_background, text=self.user.username, font=("Roboto",20), fg_color="transparent")
        self.username_label.pack(expand=True)

        self.username_label.bind("<Enter>",self.on_mouse_entered)
        self.username_label.bind("<Leave>", self.on_mouse_exit)
        self.username_label.bind("<Button-1>", self.on_mouse_clicked)

        self.original_color = self.cget("fg_color")
        self.hover_color = ("gray70", "gray30")

    def on_mouse_entered(self, event):
        self.configure(fg_color=self.hover_color)

    def on_mouse_exit(self, event):
        self.reset_color()

    def on_mouse_clicked(self, event):
        self.configure(fg_color=("gray80", "gray40"))
        self.after(150, self.set_to_hover_color)
        self.on_user_pressed_icon.send(self, user=self.user)
    
    def set_to_hover_color(self):
        self.configure(fg_color=self.hover_color)
    def reset_color(self):
        self.configure(fg_color=self.original_color)
        
class UserCreationMenu(CTkFrame):
    def __init__(self, language_manager:LanguageManager, user_manager:UserManager, master, **kwargs):
        super().__init__(master, **kwargs)

        self.root = master
        self.language_manager = language_manager
        self.user_manager = user_manager

        self.on_create_button_pressed=signal("on_create_user_button_pressed")
        self.on_cancel_button_pressed=signal("on_cancel_user_button_pressed")
        self.on_user_type_in_username_entery=signal("on_user_type_in_username_entery")
        self.on_user_type_in_password_entery=signal("on_user_type_in_password_entery")

        #main frame
        self.configure(self.root, width=400, height=500)
        self.pack_propagate(False)
        self.propagate(False)

        #main frame tittle
        self.Create_a_user_label=CTkLabel(self, font=("Roboto" ,30))
        self.Create_a_user_label.pack(pady=20)
        self.language_manager.register_widget(self.Create_a_user_label,"Create a new user")

        #username label
        self.username_label = CTkLabel(self, font=("Roboto",20))
        self.language_manager.register_widget(self.username_label,"Username")
        self.username_label.pack(side="top")

        #user name entery
        self.username_entery_text_variable = StringVar() 
        self.username_entery_text_variable.trace_add("write",self.on_username_typed)
        self.username_entery_field = CTkEntry(self, width=200, height=30, border_width=0, textvariable=self.username_entery_text_variable)
        self.username_entery_field.pack(side="top")

        #requirements for username
        self.username_character_length_requirement_label=CTkLabel(self, font=("Roboto",15))
        self.language_manager.register_widget(self.username_character_length_requirement_label, "-Username must be 4 - 12 characters long")
        self.username_character_length_requirement_label.pack(side="top", pady=2)

        self.username_character_unqieness_requirement_label=CTkLabel(self, font=("Roboto",15))
        self.language_manager.register_widget(self.username_character_unqieness_requirement_label, "-Username must be unique")
        self.username_character_unqieness_requirement_label.pack(side="top", pady=2)
        
        self.username_password_buffer=CTkFrame(self, height=20, fg_color="transparent")
        self.username_password_buffer.pack_propagate(False)
        self.username_password_buffer.pack()
        
        #password
        self.password_label = CTkLabel(self, font=("Roboto", 20))
        self.language_manager.register_widget(self.password_label, "Password")
        self.password_label.pack(side="top")

        self.password_entery_text_variable = StringVar()
        self.password_entery_text_variable.trace_add("write",self.on_password_typed)
        self.password_entery_field = CTkEntry(self, width=200, height=30, border_width=0, textvariable=self.password_entery_text_variable)
        self.password_entery_field.pack(side="top")

        #requirement for password
        self.password_character_length_requirement_label = CTkLabel(self, font=("Roboto",15))
        self.language_manager.register_widget(self.password_character_length_requirement_label, "-Password must have at least 4 characters or no characters for no password")
        self.password_character_length_requirement_label.pack(side="top", pady=2)

        self.password_character_type_requirements_label = CTkLabel(self, font=("Roboto",15))
        self.language_manager.register_widget(self.password_character_type_requirements_label, "-password must contan atleast one number and 3 letters if its not empty")
        self.password_character_type_requirements_label.pack(side = "top", pady=2)

        #buttons
        self.buttons_frame = CTkFrame(self, fg_color="transparent", width=390, height=40)
        self.buttons_frame.pack_propagate(False)
        self.buttons_frame.pack(side="bottom", pady=15)

        self.create_button = CTkButton(self.buttons_frame, corner_radius=10, text="Create", width=175, height=40,command=self.on_create_button_pressed_func, font =("Roboto",20))
        self.language_manager.register_widget(self.create_button, "Create")
        self.create_button.pack(side="left", padx=10)   

        self.cancel_button = CTkButton(self.buttons_frame, corner_radius=10, text="Cancel", width=175, height=40, command=self.on_cancel_button_pressed_func, font =("Roboto",20))
        self.language_manager.register_widget(self.cancel_button, "Cancel")
        self.cancel_button.pack(side="right", padx=10)               

    def on_create_button_pressed_func(self):
        self.on_create_button_pressed.send(self, username=self.username_entery_field.get(), password=self.password_entery_field.get())
    def on_cancel_button_pressed_func(self):
        self.on_cancel_button_pressed.send(self)
    def on_username_typed(self, *args):
        self.on_user_type_in_username_entery.send(self, username=self.username_entery_field.get())
    def on_password_typed(self, *args):
        self.on_user_type_in_password_entery.send(self,password=self.password_entery_field.get())

class UserloginMenu(CTkFrame):
    def __init__(self, user:User, language_manager:LanguageManager, user_manager:UserManager, master, **kwargs):
        super().__init__(master, **kwargs)

        self.on_login_button_pressed = signal("on_login_button_presssed")
        self.on_cancel_login_button_pressed = signal("on_cancel_button_presssed")

        self.root = master
        self.language_manager = language_manager
        self.user_manager = user_manager
        self.user = user

        self.configure(width=300, height=450)
        self.pack_propagate(False)
        
        self.login_to_label=CTkLabel(self,font=("Roboto",40))
        self.language_manager.register_widget(self.login_to_label, "Login...")
        self.login_to_label.pack(pady=10)

        image_object=Image.open(self.user.profile_picture_path)
        ctk_image=CTkImage(light_image=image_object,dark_image=image_object, size=(120,120))
        self.user_profile = CTkLabel(self, text="", image=ctk_image)
        self.user_profile.pack(pady=10)

        self.username_label=CTkLabel(self, text=user.username, font=("Roboto",30))
        self.username_label.pack(pady=10)

        self.username_password_buffer=CTkFrame(self, height=10, fg_color="transparent")
        self.username_password_buffer.pack()

        self.password_label = CTkLabel(self,text=f"Password", font=("Roboto", 20))
        self.language_manager.register_widget(self.password_label,"Password")
        self.password_label.pack(pady=5)

        self.password_entery_text_variable = StringVar()
        self.password_entery_field = CTkEntry(self, width=200, height=30, border_width=0, textvariable=self.password_entery_text_variable)
        self.password_entery_field.pack(side="top", pady=10)

        self.buttons_frame=CTkFrame(self,width=285, height=50, fg_color="transparent")
        self.buttons_frame.pack(side="bottom",pady=10)
        self.buttons_frame.pack_propagate(False)

        self.login_button = CTkButton(self.buttons_frame, height=50, width=135, corner_radius=10, font=("Roboto",25),command=self.login_button_pressed)
        self.language_manager.register_widget(self.login_button, "Login")
        self.login_button.pack(side="left", padx=5)

        self.cancel_login_button =  CTkButton(self.buttons_frame, height=50, width=135, corner_radius=10, font=("Roboto",25), command=self.Cancel_button_pressed)
        self.language_manager.register_widget(self.cancel_login_button, "Cancel")
        self.cancel_login_button.pack(side="right",padx=5)
    
    def login_button_pressed(self):
        self.on_login_button_pressed.send(self, user=self.user, entered_password=self.password_entery_field.get())
    def Cancel_button_pressed(self):
        self.on_cancel_login_button_pressed.send(self)
    
    