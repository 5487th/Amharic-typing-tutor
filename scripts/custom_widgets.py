from customtkinter import *
import warnings
from blinker import signal
from PIL import Image, ImageEnhance, ImageTk
import pathlib
import fitz

from scripts.user_manager import User
from scripts.user_manager import UserManager
from scripts.language_manager import LanguageManager


class UserProfileCard(CTkFrame):
    def __init__(self, master, user_manager: UserManager, user: User, **kwargs):
        super().__init__(master, **kwargs)
        if not user:
            warnings.warn(
                "attempted to create user login icon with no user, user icon not created"
            )
            return

        self.user = user
        self.master = master
        self.on_user_pressed_icon = signal(f"on_user_pressed_{self.user.username}_icon")
        self.user_manager = user_manager

        self.configure(width=150, height=190, corner_radius=10)
        self.pack_propagate(False)

        self.bind("<Enter>", self.on_mouse_entered)
        self.bind("<Leave>", self.on_mouse_exit)
        self.bind("<Button-1>", self.on_mouse_clicked)

        self.profile_picture = None

        if pathlib.Path(user.profile_picture_path).exists():
            image_object = Image.open(user.profile_picture_path)
            ctk_image = CTkImage(
                light_image=image_object, dark_image=image_object, size=(120, 120)
            )
            self.profile_picture = CTkLabel(self, text="", image=ctk_image)
        else:
            image_object = Image.open(self.user_manager.default_profile_picture_path)
            ctk_image = CTkImage(
                light_image=image_object, dark_image=image_object, size=(120, 120)
            )
            self.profile_picture = CTkLabel(self, text="", image=ctk_image)

        self.profile_picture.pack(pady=10)
        self.profile_picture.bind("<Enter>", self.on_mouse_entered)
        self.profile_picture.bind("<Leave>", self.on_mouse_exit)
        self.profile_picture.bind("<Button-1>", self.on_mouse_clicked)

        self.label_background = CTkFrame(self, corner_radius=10, width=135, height=35)
        self.label_background.pack(side="bottom", pady=8)
        self.label_background.pack_propagate(False)

        self.label_background.bind("<Enter>", self.on_mouse_entered)
        self.label_background.bind("<Leave>", self.on_mouse_exit)
        self.label_background.bind("<Button-1>", self.on_mouse_clicked)

        self.username_label = CTkLabel(
            self.label_background,
            text=self.user.username,
            font=("Roboto", 20),
            fg_color="transparent",
        )
        self.username_label.pack(expand=True)

        self.username_label.bind("<Enter>", self.on_mouse_entered)
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


class UserloginPopUp(CTkFrame):
    def __init__(
        self,
        user: User,
        language_manager: LanguageManager,
        user_manager: UserManager,
        master,
        **kwargs,
    ):
        super().__init__(master, **kwargs)

        self.on_login_button_pressed = signal("on_login_button_presssed")
        self.on_cancel_login_button_pressed = signal("on_cancel_button_presssed")

        self.root = master
        self.language_manager = language_manager
        self.user_manager = user_manager
        self.user = user

        if not user_manager.user_has_empty_password(user.username):
            self.configure(width=300, height=450)
        else:
            self.configure(width=300, height=340)

        self.pack_propagate(False)

        self.login_to_label = CTkLabel(self, font=("Roboto", 40))
        self.language_manager.register_widget(self.login_to_label, "Login...")
        self.login_to_label.pack(pady=10)

        image_object = Image.open(self.user.profile_picture_path)
        ctk_image = CTkImage(
            light_image=image_object, dark_image=image_object, size=(120, 120)
        )
        self.user_profile = CTkLabel(self, text="", image=ctk_image)
        self.user_profile.pack(pady=10)

        self.username_label = CTkLabel(self, text=user.username, font=("Roboto", 30))
        self.username_label.pack(pady=10)

        self.username_password_buffer = CTkFrame(
            self, height=10, fg_color="transparent"
        )
        self.username_password_buffer.pack()

        self.password_label = CTkLabel(self, text=f"Password", font=("Roboto", 20))
        self.language_manager.register_widget(self.password_label, "Password")

        self.password_entery_text_variable = StringVar(value="")
        self.password_entery_field = CTkEntry(
            self,
            width=200,
            height=30,
            border_width=0,
            textvariable=self.password_entery_text_variable,
            placeholder_text="password..",
        )

        if not user_manager.user_has_empty_password(user.username):
            self.password_label.pack(pady=5)
            self.password_entery_field.pack(side="top", pady=10)

        self.buttons_frame = CTkFrame(
            self, width=285, height=50, fg_color="transparent"
        )
        self.buttons_frame.pack(side="bottom", pady=10)
        self.buttons_frame.pack_propagate(False)

        self.login_button = CTkButton(
            self.buttons_frame,
            height=50,
            width=135,
            corner_radius=10,
            font=("Roboto", 25),
            command=self.login_button_pressed,
        )
        self.language_manager.register_widget(self.login_button, "Login")
        self.login_button.pack(side="left", padx=5)

        self.cancel_login_button = CTkButton(
            self.buttons_frame,
            height=50,
            width=135,
            corner_radius=10,
            font=("Roboto", 25),
            command=self.Cancel_button_pressed,
        )
        self.language_manager.register_widget(self.cancel_login_button, "Cancel")
        self.cancel_login_button.pack(side="right", padx=5)

        self.root.update_idletasks()

    def login_button_pressed(self):
        self.on_login_button_pressed.send(
            self, user=self.user, entered_password=self.password_entery_field.get()
        )

    def Cancel_button_pressed(self):
        self.on_cancel_login_button_pressed.send(self)


class logging_in_transition_screen(CTkFrame):
    def __init__(
        self,
        language_manager: LanguageManager,
        user_manager: UserManager,
        root,
        **kwargs,
    ):
        super().__init__(root, **kwargs)

        self.language_manager = language_manager
        self.user_manager = user_manager

        self.configure()
        self.place_configure(relwidth=1, relheight=1)
        root.update_idletasks()

        self.username_profile_frame = CTkFrame(self, fg_color="transparent")
        self.username_profile_frame.place(relx=0.5, rely=0.3, anchor="center")

        image_object = Image.open(user_manager.current_user.profile_picture_path)
        ctk_image = CTkImage(
            light_image=image_object, dark_image=image_object, size=(280, 280)
        )
        self.user_profile = CTkLabel(
            self.username_profile_frame, text="", image=ctk_image
        )
        self.user_profile.pack()

        self.user_name_label = CTkLabel(
            self.username_profile_frame,
            text=user_manager.current_user.username,
            font=("Roboto", 40),
        )
        self.user_name_label.pack(pady=10)

        self.logging_you_in_label = CTkLabel(self, font=("Roboto", 40))
        self.logging_you_in_label.place(rely=0.8, relx=0.5, anchor="center")

        # dot animation
        self.dot_count = 0
        self.base_text = self.language_manager.translate("logging you in")
        root.update_idletasks()

        self.animate_dots()

    def animate_dots(self):
        self.dot_count = (self.dot_count % 3) + 1
        dots = "." * self.dot_count

        self.logging_you_in_label.configure(text=f"{self.base_text}{dots}")

        self.after(300, self.animate_dots)


class ImageButton(CTkLabel):
    def __init__(self, root, image_path, sizex=40, sizey=40, **kwargs):
        super().__init__(root, **kwargs)
        if not root:
            warnings.warn(
                "attempted to create image button with none root, imagebutton not created"
            )
            return
        if not image_path:
            warnings.warn(
                "attempted to create image button with none imagepath, imagebutton not created"
            )
            return
        if not pathlib.Path(image_path).exists():
            warnings.warn(
                "attempted to createa image button with an invalid image path, image button not created "
            )
            return

        self.image_path = image_path
        self.sizex = sizex
        self.sizey = sizey

        self.image_object = Image.open(self.image_path)
        self.ctk_image = CTkImage(
            light_image=self.image_object,
            dark_image=self.image_object,
            size=(self.sizex, self.sizey),
        )
        self.configure(text="", image=self.ctk_image)

        self.on_mouse_enter = signal(f"on_mouse_hover_over {self}")
        self.on_mouse_exit = signal(f"on_mouse_enter {self}")
        self.on_mouse_click = signal(f"on_mouse_clicked {self}")

        self.bind("<Enter>", self.mouse_enter)
        self.bind("<Leave>", self.mouse_exit)
        self.bind("<Button-1>", self.mouse_clicked)

    def mouse_enter(self, event):
        self.darken_image()
        self.on_mouse_enter.send(self)

    def mouse_exit(self, event):
        self.configure(image=self.ctk_image)
        self.on_mouse_exit.send(self)

    def mouse_clicked(self, event):
        self.lighten_image()
        self.after(100, self.darken_image)
        self.on_mouse_click.send(self)

    def darken_image(self):
        enhancer = ImageEnhance.Brightness(self.image_object)
        dark_img = enhancer.enhance(0.8)
        ctk_image = CTkImage(light_image=dark_img, dark_image=dark_img, size=(50, 50))

        self.configure(image=ctk_image)

    def lighten_image(self):
        enhancer = ImageEnhance.Brightness(self.image_object)
        dark_img = enhancer.enhance(1.2)
        ctk_image = CTkImage(light_image=dark_img, dark_image=dark_img, size=(50, 50))

        self.configure(image=ctk_image)


class GamesIcon(CTkFrame):
    def __init__(self, master, activity_image_path, activity_name, menu, **kwargs):
        super().__init__(master, **kwargs)

        self.menu = menu
        self.menu_image_path = activity_image_path
        self.activity_name = activity_name

        self.configure(width=190, height=190, corner_radius=10)
        self.pack_propagate(False)

        self.bind("<Enter>", self.on_mouse_entered)
        self.bind("<Leave>", self.on_mouse_exit)
        self.bind("<Button-1>", self.on_mouse_clicked)

        if pathlib.Path(activity_image_path).exists():
            image_object = Image.open(activity_image_path)
            ctk_image = CTkImage(
                light_image=image_object, dark_image=image_object, size=(120, 120)
            )
            self.activity_picture = CTkLabel(self, text="", image=ctk_image)
        else:
            image_object = Image.open(activity_image_path)
            ctk_image = CTkImage(
                light_image=image_object, dark_image=image_object, size=(120, 120)
            )
            self.activity_picture = CTkLabel(self, text="", image=ctk_image)

        self.activity_picture.pack(pady=10)
        self.activity_picture.bind("<Enter>", self.on_mouse_entered)
        self.activity_picture.bind("<Leave>", self.on_mouse_exit)
        self.activity_picture.bind("<Button-1>", self.on_mouse_clicked)

        self.label_background = CTkFrame(self, corner_radius=10, width=180, height=35)
        self.label_background.pack(side="bottom", pady=8)
        self.label_background.pack_propagate(False)

        self.label_background.bind("<Enter>", self.on_mouse_entered)
        self.label_background.bind("<Leave>", self.on_mouse_exit)
        self.label_background.bind("<Button-1>", self.on_mouse_clicked)

        self.activity_name_label = CTkLabel(
            self.label_background,
            text=self.activity,
            font=("Roboto", 20),
            fg_color="transparent",
        )
        self.username_label.pack(expand=True)

        self.username_label.bind("<Enter>", self.on_mouse_entered)
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


class UserProfilePopup(CTkFrame):
    def __init__(self, master, root, **kwarfs):
        super().__init__(master)

        self.master = master
        self.root = root

        self.configure(width=60, height=100, corner_radius=10)
        self.propagate = False

        self.settings_button = CTkButton(
            self,
        )
        self.manual_button = None
        self.log_out_button = None


class PDFViewer(CTkFrame):

    def __init__(self, master, root, width=800, height=600, render_scale=2, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)

        self.root = root
        self.render_scale = render_scale

        self.pdf = None
        self.page_count = 0
        self.current_page = 0

        self.current_pil_image = None
        self.tk_image = None

        # =========================
        # TOP BAR
        # =========================
        self.topbar = CTkFrame(self)
        self.topbar.pack(fill="x", padx=10, pady=10)

        self.prev_button = CTkButton(
            self.topbar, text="◀", width=40, command=self.previous_page
        )
        self.prev_button.pack(side="left")

        self.page_label = CTkLabel(self.topbar, text="0 / 0")
        self.page_label.pack(side="left", expand=True)

        self.next_button = CTkButton(
            self.topbar, text="▶", width=40, command=self.next_page
        )
        self.next_button.pack(side="right")

        # =========================
        # IMAGE DISPLAY
        # =========================
        self.image_label = CTkLabel(self, text="")
        self.image_label.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # =========================
        # EVENTS
        # =========================
        self.bind("<Configure>", self._on_resize)

        self.root.bind("<Left>", self._left_key)
        self.root.bind("<Right>", self._right_key)

    def load(self, pdf_path):

        self.close()

        self.pdf = fitz.open(pdf_path)

        self.page_count = len(self.pdf)

        self.current_page = 0

        self.show_page(0)

    def close(self):

        if self.pdf:
            self.pdf.close()

        self.pdf = None
        self.page_count = 0
        self.current_page = 0

    def next_page(self):

        if not self.pdf:
            return

        if self.current_page < self.page_count - 1:
            self.show_page(self.current_page + 1)

    def previous_page(self):

        if not self.pdf:
            return

        if self.current_page > 0:
            self.show_page(self.current_page - 1)

    def show_page(self, page_number):

        page = self.pdf.load_page(page_number)

        matrix = fitz.Matrix(self.render_scale, self.render_scale)

        pix = page.get_pixmap(matrix=matrix, alpha=False)

        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        self.current_pil_image = image

        self.current_page = page_number

        self.page_label.configure(text=f"{self.current_page + 1} / {self.page_count}")

        self._update_image()

    def _update_image(self):

        if self.current_pil_image is None:
            return

        image = self.current_pil_image.copy()

        width = max(self.image_label.winfo_width(), 100)
        height = max(self.image_label.winfo_height(), 100)

        image.thumbnail((width, height))

        self.tk_image = ImageTk.PhotoImage(image)

        self.image_label.configure(image=self.tk_image)

    def _left_key(self, event):
        self.previous_page()

    def _right_key(self, event):
        self.next_page()

    def _on_resize(self, event):
        self.after(50, self._update_image)
