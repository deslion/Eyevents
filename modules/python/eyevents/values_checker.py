from eyevents.messages import messages
from eyevents.settings import LANG


class ValuesChecker:
    @staticmethod
    def check_settings(settings):
        # Type checking
        if type(settings) is not dict:
            raise TypeError(messages['SETTINGS_TYPE_ERROR'][LANG] + '\n' + messages['SETTINGS_INFO_MESSAGE'][LANG])
        # Keys containing checking
        if any([x not in list(settings.keys()) for x in ['columns', 'common', 'loading']]):
            raise ValueError(messages['SETTINGS_CONTENT_ERROR'][LANG])
        # Each key checking for containing needed items
        # -columns

        # -common

        # -loading

        return True
