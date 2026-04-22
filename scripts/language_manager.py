import pathlib
import json
import warnings

class LanguageManager:
    ENGLISH_LANGUAGE_KEY = "en"
    AMHARIC_LANGUAGE_KEY = "am"
    TRANSLATIONS_FILE_PATH = pathlib.Path(__file__).parent.parent/'assets'/'translations.json'
    TRANSLATIONS_DICT = {}

    def __init__(self, default_lang="en"):
        self.current_lang=""

        if default_lang in [LanguageManager.ENGLISH_LANGUAGE_KEY, LanguageManager.AMHARIC_LANGUAGE_KEY]:
            self.current_lang=default_lang
        
        self.registered_widgets = []
        with open(self.TRANSLATIONS_FILE_PATH,"r") as file:
         LanguageManager.TRANSLATIONS_DICT = json.load(file)
        
    def set_language(self, lang):
        if lang in [LanguageManager.ENGLISH_LANGUAGE_KEY, LanguageManager.AMHARIC_LANGUAGE_KEY]:
            self.current_lang=lang
            self.update_all_widgets()
        else:
            warnings.warn("attempted to set language with invalid language, language set to english")
            self.current_lang = self.ENGLISH_LANGUAGE_KEY
           
    def register_widget(self, widget, key):
        self.registered_widgets.append((widget, key))
        widget.configure(text=self.translate(key))
    
    def update_all_widgets(self):
        for widget, key in self.registered_widgets:
            widget.configure(text=self.translate(key))
    
    def translate(self, key):
        if self.TRANSLATIONS_DICT:
            translation = self.TRANSLATIONS_DICT.get(key,{}).get(self.current_lang)
            if translation:
                return translation
            else:
                warnings.warn("key not found, returning passed key")
                return key