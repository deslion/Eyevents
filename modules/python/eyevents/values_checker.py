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
        # --main keys
        for x in ['window', 'center', 'method', 'fillna']:
            if x not in list(settings['smoothing'].keys()):
                raise ValueError(messages['SETTINGS_SMOOTHING_ERROR'][LANG] + messages['MISSING'][LANG] + x)
        # --methods checkings
        if settings['smoothing']['method'] not in ['med', 'median', 'avg', 'average', 'mean', 'savgol']:
            raise ValueError(messages['SETTINGS_SMOOTHING_METHOD_ERROR'][LANG])
        # --savgol window checkings
        if settings['smoothing']['method'] == 'savgol' and 'order' not in list(settings['smoothing'].keys()):
            raise ValueError(messages['SETTINGS_SMOOTHING_ORDER_ERROR'][LANG])
        # -velocity
        # --main keys
        if 'velocity_type' not in list(settings['velocity'].keys()):
            raise ValueError(messages['SETTINGS_VELOCITY_ERROR'][LANG])
        # --type checking
        if settings['velocity']['velocity_type'] not in ['analytical', 'finite_difference']:
            raise ValueError(messages['SETTINGS_VELOCITY_TYPE_ERROR'][LANG])
        # --window checking
        if settings['velocity']['velocity_type'] == 'analytical' and 'window' not in settings['velocity'].keys():
            raise ValueError(messages['SETTINGS_VELOCITY_WINDOW_ERROR'][LANG])
        # -oculus
        cond_keys = any([x not in settings['oculus'].keys() for x in ['method', 'velocity_threshold']])
        if cond_keys:
            raise ValueError(messages['SETTINGS_OCULUS_ERROR'][LANG])
        cond_meth = settings['oculus']['method'] != 'IVT'
        if cond_meth:
            raise ValueError(messages['SETTINGS_OCULUS_ERROR'][LANG])
        return True
