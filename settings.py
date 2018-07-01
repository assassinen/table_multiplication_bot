import os
import tempfile
import argparse
import json

class Settings:

    def __init__(self):
        self.settings = {'start': 4, 'stop': 4, 'number_steps': 10, 'timeout': 10}
        self.params_list = ['start', 'stop']
        self.settings_paht = 'settings.data'


    def get_settings_date(self):
        try:
            data = json.load(open(self.settings_paht))
        except:
            data = {}
        return data


    def get_settings(self, chat_id=None):
        if chat_id is not None:
            settings_data = self.get_settings_date()
            if str(chat_id) in settings_data:
                self.settings = settings_data[str(chat_id)]
        return self.settings


    def change_setting(self, settings, *args):
        new_settings = dict(zip(self.params_list, args))
        for key in new_settings.keys():
            settings[key] = int(new_settings[key])
        return settings


    def set_settings(self, chat_id=None, *args):
        if chat_id is not None and args != ():
            settings_date = self.get_settings_date()
            if chat_id in settings_date:
                settings = settings_date[chat_id]
            else:
                settings = self.settings
            settings_date[str(chat_id)] = self.change_setting(settings, *args)
        else:
            return False

        with open(self.settings_paht, 'w') as f:
            out = json.dumps(settings_date, indent=4)
            f.write(out)
            return True

