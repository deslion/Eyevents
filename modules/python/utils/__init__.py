messages = dict(
    SETTINGS_INFO_MESSAGE=dict(
        rus="""В общем виде настройки должны иметь следующий формат:
settings = dict(
    # Названия или позиции столбцов с требуемыми значениями
    columns=dict(
        time=None,  # позиция или имя столбца с отметками времени
        porx=None,  # X-координата точки взора на стимуле
        pory=None,  # Y-координата точки взора на стимуле
        psizex=None,  # размер зрачка по X-координате, можно не задавать
        psizey=None,  # размер зрачка по Y-координате, можно не задавать
    ),
    # Общие настройки эксперимента
    common=dict(
        size=None,  # физические размеры экрана в сантиметрах
        resolution=None,  # разрешение экрана в пикселях
        distance=None,  # расстояние от экрана до головы испытуемого
        adjuct_time=True,  # флаг, выравнивать метку времени (t = t - min(t))
    ),
    # Настройки загрузки траекторий
    loading=dict(
        sep=',',  # разделитель столбцов в текстовом файле траектории
        decimal='.',  # десятичный разделитель в текстовом файле траектории
        skiprows=0,  # число неинформативных строк
        header=0,  # номер строки с заголовками или None, если заголовков нет
    )
)""",
        eng="""Settings must be set as follows:
settings = dict(
    # column names or positions in index
    columns=dict(
        time=None,  # timestamp or other time column
        porx=None,  # point of regard, x-coordinate
        pory=None,  # point of regard, y-coordinate
        psizex=None,  # pupil size, in x-coordinates, not necessary
        psizey=None,  # pupil size, in y-coordinates, not necessary
    ),
    # common experiment settings
    common=dict(
        size=None,  # screen physical size in centimeters (two elements list)
        resolution=None,  # screen resolution in pixels (two elements list)
        distance=None,  # distance to head
        adjuct_time=True,  # flag, adjust time to have 0 as first stamp (t = t - min(t))
    ),
    # csv-loading settings
    loading=dict(
        sep=',',  # column separator symbol, for pandas csv-reading
        decimal='.',  # decimal separator symbol, for pandas csv-reading
        skiprows=0,  # non-informative lines count to skip
        header=0,  # header row number or None
    )
)"""
    ),
    SETTINGS_TYPE_ERROR=dict(
        rus='Настройки должны быть словарём, проверьте тип данных',
        eng='Settings must be a dict-objects, check values'
    ),
    SETTINGS_CONTENT_ERROR=dict(
        rus='''
Настройки должны содержать: 
    'loading' для настроек чтения траекторий
    'columns' для позиций столбцов
    'common' для прочих настроек''',
        eng='''
Settings must contain: 
    'loading' for loading trajectory parameters
    'columns' for their positions
    'common' for other ones'''
    )
)
