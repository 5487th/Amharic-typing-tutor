import pathlib
import json
import warnings


class LanguageManager:
    ENGLISH_LANGUAGE_KEY = "en"
    AMHARIC_LANGUAGE_KEY = "am"
    TRANSLATIONS_FILE_PATH = (
        pathlib.Path(__file__).parent.parent / "assets" / "translations.json"
    )
    TRANSLATIONS_DICT = {}

    def __init__(self, default_lang="en"):
        self.current_lang = ""

        if default_lang in [
            LanguageManager.ENGLISH_LANGUAGE_KEY,
            LanguageManager.AMHARIC_LANGUAGE_KEY,
        ]:
            self.current_lang = default_lang

        self.registered_widgets = []
        with open(self.TRANSLATIONS_FILE_PATH, "r") as file:
            LanguageManager.TRANSLATIONS_DICT = json.load(file)

    def set_language(self, lang):
        if not lang:
            warnings.warn("called set language function with 'none' lang, lang not set")
            return

        if lang in [
            LanguageManager.ENGLISH_LANGUAGE_KEY,
            LanguageManager.AMHARIC_LANGUAGE_KEY,
        ]:
            self.current_lang = lang
            self.update_all_widgets()
        else:
            warnings.warn(
                "called set language function with invalid lang, lang not set"
            )
            self.current_lang = self.ENGLISH_LANGUAGE_KEY

    def register_widget(self, widget, key):
        self.registered_widgets.append((widget, key))
        widget.configure(text=self.translate(key))

    def update_all_widgets(self):
        alive_widgets = []
        for widget, key in self.registered_widgets:
            if widget and widget.winfo_exists():
                widget.configure(text=self.translate(key))
                alive_widgets.append((widget, key))
        self.registered_widgets = alive_widgets

    def translate(self, key):
        if self.TRANSLATIONS_DICT:
            translation = self.TRANSLATIONS_DICT.get(key, {}).get(self.current_lang)
            if translation:
                return translation
            else:
                warnings.warn(f"key '{key}' not found, returning passed key")
                return key
