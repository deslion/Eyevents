LANG = 'rus'

# This dictionary contains template of main settings for trajectories loading
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
)
