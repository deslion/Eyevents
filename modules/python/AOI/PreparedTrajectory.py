from EyeTrackingPackage.modules.python.AOI.Trajectory import Trajectory
import numpy as np
from tqdm import tqdm, tqdm_notebook

class PreparedTrajectory(Trajectory):

    def __init__(self, data):
        """
        Загружает траекторию из переданного объекта pandas.DataFrame

        Inputs:
            data - pandas.DataFrame с траекторией
        """
        self.grouped_data = None

        self.data = data


def get_transition_matrix(path, settings=None):
    """
    Функция переводит записанные координаты в матрицу числа переходов между областями
    """
    # Задание стандартных настроек при отсутствии на входе
    if settings is None:
        settings = {
            'txy_columns': [0, 1, 2],
            'txy_coefs': [.001, 1280, 720],
            'min_time': True,
            'ts_in_group': 100,
            'cells_xy': [5, 5],
            'empty_aoi': True
        }

    # Разбор настроек
    t_col, x_col, y_col = settings['txy_columns']
    t_coef, x_coef, y_coef = settings['txy_coefs']
    min_time = settings['min_time']
    ts_in_group = settings['ts_in_group']
    cells_x, cells_y = settings['cells_xy']
    empty_aoi = settings['empty_aoi']

    # Считывание и предобработка траектории
    tr = Trajectory(path, t_col, x_col, y_col)
    tr.set_parameters(x_coef=x_coef, y_coef=y_coef, t_coef=t_coef,
                      min_time=min_time, ts_in_group=ts_in_group,
                      cells_x=cells_x, cells_y=cells_y)
    tr.prepare_time()
    tr.group_by_time()
    tr.prepare_coordinates()

    # Расчёт и вывод матрицы числа переходов
    tr.get_transition_matrix(empty_aoi, to_probabilities=False)
    return tr.transition_matrix


def get_classes_probabilities(class_pathes, settings=None, main_path=None, nb = True):
    """
    Для каждого класса по заданным файлам строится матрица вероятностей переходов
    """
    iter_ = tqdm_notebook if nb else tqdm

    class_matrixes = dict([x, None] for x in class_pathes.keys())

    prefix = './' if main_path is None else main_path

    _classes = class_matrixes.keys()

    for _class in _classes:
        class_seq = []
        for x in iter_(class_pathes[_class]):
            class_seq.append(get_transition_matrix(prefix + x, settings))
        class_matrixes[_class] = class_seq
        print('Class \'{}\' was evaluated'.format(_class))

    classes_total_number = dict([x, np.sum(class_matrixes[x], 0)] for x in _classes)

    classes_probabilities = dict([x, classes_total_number[x] / np.sum(classes_total_number[x], 1)] for x in _classes)

    return classes_probabilities


def get_likelyhood_estimation(new_path, classes_probabilities, settings=None):
    """

    """
    # Задание стандартных настроек при отсутствии на входе
    if settings is None:
        settings = {
            'txy_columns': [0, 1, 2],
            'txy_coefs': [.001, 1280, 720],
            'min_time': True,
            'ts_in_group': 100,
            'cells_xy': [5, 5],
            'empty_aoi': True
        }

    # Разбор настроек
    t_col, x_col, y_col = settings['txy_columns']
    t_coef, x_coef, y_coef = settings['txy_coefs']
    min_time = settings['min_time']
    ts_in_group = settings['ts_in_group']
    cells_x, cells_y = settings['cells_xy']
    empty_aoi = settings['empty_aoi']

    # Считывание новой траектории
    tr = Trajectory(new_path, t_col, x_col, y_col)
    tr.set_parameters(x_coef=x_coef, y_coef=y_coef, t_coef=t_coef,
                      min_time=min_time, ts_in_group=ts_in_group,
                      cells_x=cells_x, cells_y=cells_y)
    tr.prepare_time()
    tr.group_by_time()
    tr.prepare_coordinates()

    # Расчёт матрицы числа переходов
    tr.get_transition_matrix(empty_aoi, to_probabilities=False)
    M = tr.transition_matrix

    _classes = classes_probabilities.keys()

    likelyhood_estimation = dict([x, np.nansum(M * np.log(classes_probabilities[x]))] for x in _classes)

    return likelyhood_estimation
