messages = dict(
    MISSING=dict(
        rus="\nНе хватает: ",
        eng="\nMissing key: "
    ),
    TYPE=dict(
        rus="\nНеправильный тип: ",
        eng="\nWrong type: "
    ),
    SETTINGS_INFO_MESSAGE=dict(
        rus="""Настройки должны иметь следующий формат:
settings = dict(
    # Настройки загрузки траекторий
    loading=dict(
        sep=',',  # разделитель столбцов в текстовом файле траектории
        decimal='.',  # десятичный разделитель в текстовом файле траектории
        skiprows=0,  # число неинформативных строк
        header=0,  # номер строки с заголовками или None, если заголовков нет
    ),
    # Названия или позиции столбцов с требуемыми значениями
    columns=dict(
        time=0,  # позиция или имя столбца с отметками времени
        porx=1,  # X-координата точки взора на стимуле
        pory=2,  # Y-координата точки взора на стимуле
        psizex=None,  # размер зрачка по X-координате, можно не задавать
        psizey=None,  # размер зрачка по Y-координате, можно не задавать
    ),
    # Общие настройки эксперимента
    common=dict(
        size=[59, 33],  # физические размеры экрана в сантиметрах
        resolution=[1920, 1080],  # разрешение экрана в пикселях
        distance=50,  # расстояние от экрана до головы испытуемого
        adjust_time=True,  # флаг, выравнивать метку времени (t = t - min(t))
        normalized=True,  # флаг, координаты записывались нормированно на интервал 0..1
        reference_point=[0, 0],  # точка калибровки айтрекера, верхний левый угол по-умолчанию. None для центра
    ),
    # Настройки сглаживания
    smoothing=dict(
        window=33,  # величина скользящего окна в сэмплах
        center=True,  # флаг, производить вычисления в середине окна
        method='median',  # метод сглаживания: median, mean или savgol. savgol - фильтрация методом Савицкого-Голея
        order=2,  # порядок фильтра Савицкого-Голея
        fillna=True  # флаг, заполнять пропуски, возникшие при сглаживании
    ),
    # Настройки вычисления сглаживания
    velocity=dict(
        velocity_type='analytical',  # метод вычисления: analytical (методом Савицкого-Голея) 
        # или finite_difference (метод конечных разностей)
        window=13  # длина фильтра Савицкого-Голея (для типа = analytical)
    ),
    # Настройки определения окуломоторных событий
    oculus=dict(
        method='IVT',  # метод определения (только IVT на данный момент)
        velocity_threshold=30,  # порог скорости для IVT-детектора
    )
)""",
        eng="""Settings must be set as follows:
settings = dict(
    # csv-loading settings
    loading=dict(
        sep=',',  # column separator symbol, for pandas csv-reading
        decimal='.',  # decimal separator symbol, for pandas csv-reading
        skiprows=0,  # non-informative lines count to skip
        header=0,  # header row number or None
    ),
    # column names or positions in index
    columns=dict(
        time=0,  # timestamp or other time column
        porx=1,  # point of regard, x-coordinate
        pory=2,  # point of regard, y-coordinate
        psizex=None,  # pupil size, in x-coordinates, not necessary
        psizey=None,  # pupil size, in y-coordinates, not necessary
    ),
    # common experiment settings
    common=dict(
        size=[59, 33],  # screen physical size in centimeters (two elements list)
        resolution=[1920, 1080],  # screen resolution in pixels (two elements list)
        distance=50,  # distance to head
        adjust_time=True,  # flag, adjust time to have 0 as first stamp (t = t - min(t))
        normalized=True,  # flag, coordinates were normalized to 0..1 interval
        reference_point=[0, 0],  # calibration point, top-left corner as default value. Can be None for center
    ),
    # contains coordinates smoothing settings
    smoothing=dict(
        window=33,  # rolling window size
        center=True,  # flag, make calculation on the central point, not on the right
        method='median',  # smoothing method, one of [median, mean, savgol]. savgol for Savitzky-Golay filter
        order=2,  # Savitzky-Golay filter order
        fillna=True  # flag, fill na after smoothing, back- and forward fill will be done
    ),
    # velocity calculation settings
    velocity=dict(
        velocity_type='analytical',  # velocity calculation type, one of ['analytical', 'finite_difference']
        window=13  # window for analytical method calculation
    ),
    # contains oculomotor events detectors settings
    oculus=dict(
        method='IVT',  # chosen detection method
        velocity_threshold=30,  # velocity threshold for IVT detector, in angular degrees
    )
)"""
    ),
    SETTINGS_TYPE_ERROR=dict(
        rus='Все настройки должны быть словарём, проверьте тип данных',
        eng='All settings must be a dict-objects, check values'
    ),
    SETTINGS_CONTENT_ERROR=dict(
        rus='''
Настройки должны содержать: 
    'loading' для настроек чтения траекторий
    'columns' для задания позиций столбцов
    'common' для прочих настроек эксперимента
    'smoothing' для настроек сглаживания координат
    'velocity' для настроек вычисления угловых скоростей
    'oculus' для настроек детектора окуломоторных событий''',
        eng='''
Settings must contain: 
    'loading' for loading trajectory parameters
    'columns' for their positions
    'common' for experiments common settings
    'smoothing' for coordinates smoothing settings
    'velocity' for angular velocity calculation settings
    'oculus' for oculomotor events detection settings'''
    ),
    SETTINGS_LOADING_ERROR=dict(
        rus="""
Настройки загрузки должны содержать следующие поля:
    'sep' - разделитель столбцов в текстовом файле траектории
    'decimal' - десятичный разделитель в текстовом файле траектории
    'skiprows' - число неинформативных строк
    'header' - номер строки с заголовками или None, если заголовков нет""",
        eng="""
Loading settings must contain:
    'sep' - column separator symbol, for pandas csv-reading
    'decimal' - # decimal separator symbol, for pandas csv-reading
    'skiprows' - non-informative lines count to skip
    'header' - header row number or None"""
    ),
    SETTINGS_COLUMNS_ERROR=dict(
        rus="""
Настройки столбцов должны содержать следующие поля:
    'time' - позиция или имя столбца с отметками времени
    'porx' - X-координата точки взора на стимуле
    'pory' - Y-координата точки взора на стимуле
Настройки также могут содержать (не обязательно):
    'psizex' - размер зрачка по X-координате
    'psizey' - размер зрачка по Y-координате""",
        eng="""
Columns settings must contain: 
    'time' - timestamp or other time column, integer or string if header is set
    'porx' - point of regard, x-coordinate, integer or string if header is set
    'pory' - point of regard, y-coordinate, integer or string if header is set
Also can be set, but not necessary:
    'psizex' - pupil size, in x-coordinates, integer or string if header is set
    'psizey' - pupil size, in y-coordinates, integer or string if header is set"""
    ),
    SETTINGS_COMMON_ERROR=dict(
        rus="""
Общие настройки эксперимента должны содержать:
    'size' - физические размеры экрана в сантиметрах
    'resolution' - разрешение экрана в пикселях
    'distance' - расстояние от экрана до головы испытуемого
    'adjust_time' - флаг, выравнивать метку времени (t = t - min(t))
    'normalized' - флаг, координаты записывались нормированно на интервал 0..1
    'reference_point' - точка калибровки айтрекера, верхний левый угол по-умолчанию. None для центра""",
        eng="""
Experiments common settings must contain:
    'size' - screen physical size in centimeters (two elements list)
    'resolution' - screen resolution in pixels (two elements list)
    'distance' - distance to head
    'adjust_time' - flag, adjust time to have 0 as first stamp (t = t - min(t))
    'normalized' - flag, coordinates were normalized to 0..1 interval
    'reference_point' - calibration point, top-left corner as default value. Can be None for center"""
    )
)
