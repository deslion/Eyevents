from eyevents.messages import messages
from eyevents.settings import LANG
from eyevents.settings import settings as template


class ValuesChecker:
    @staticmethod
    def check_settings(settings):
        # Type checking
        if type(settings) is not dict:
            raise TypeError(messages['SETTINGS_TYPE_ERROR'][LANG] + '\n' + messages['SETTINGS_INFO_MESSAGE'][LANG])
        # Keys containing checking
        for x in list(template.keys()):
            if x not in list(settings.keys()):
                raise ValueError(messages['SETTINGS_CONTENT_ERROR'][LANG] + messages['MISSING'][LANG] + x)
        # Inside values type checking
        for x in list(settings.keys()):
            if type(settings[x]) is not dict:
                raise TypeError(messages['SETTINGS_TYPE_ERROR'][LANG] + messages['TYPE'][LANG] + x)
        # Each key checking for containing needed items
        # -loading
        for x in list(template['loading'].keys()):
            if x not in list(settings['loading'].keys()):
                raise ValueError(messages['SETTINGS_LOADING_ERROR'][LANG] + messages['MISSING'][LANG] + x)
        # -columns
        for x in ['time', 'porx', 'pory']:
            if x not in list(settings['columns'].keys()):
                raise ValueError(messages['SETTINGS_COLUMNS_ERROR'][LANG] + messages['MISSING'][LANG] + x)
        # -common
        for x in list(template['common'].keys()):
            if x not in list(settings['common'].keys()):
                raise ValueError(messages['SETTINGS_COMMON_ERROR'][LANG] + messages['MISSING'][LANG] + x)
        # -smoothing
        # -velocity
        # -oculus
        return True
