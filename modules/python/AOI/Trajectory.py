import pandas as pd
import numpy as np
from EyeTrackingPackage.modules.python.AOI.AOI import AOI


class Trajectory(AOI):

    def __init__(self, file, t_col=0, x_col=1, y_col=2, **kwargs):
        """
        Загружает траекторию из указанного файла

        Inputs:
            file - путь к файлу csv или txt
            t_col, x_col, y_col - номера столбцов с отметкой времени и координатами
            **kwargs - дополнительные настройки загрузчика: разделитель, десятичная точка и пр.
        """
        self.grouped_data = None
        self.x_coef = None
        self.y_coef = None
        self.min_time = None
        self.t_coef = None
        self.ts_in_group = None
        self.cells_x = None
        self.cells_y = None
        self.aoi_df = None

        df = pd.read_csv(file, **kwargs)
        cols = []
        for col_number in [t_col, x_col, y_col]:
            cols.append(df.columns[col_number])
        df = df[cols].copy()
        df.columns = ['t', 'x', 'y']
        self.raw_data = df.copy()

    def set_parameters(self, x_coef=1280, y_coef=720, t_coef=.001, min_time=True,
                       ts_in_group=1, cells_x=5, cells_y=5):
        """

        """
        self.x_coef = x_coef
        self.y_coef = y_coef
        self.t_coef = t_coef
        self.min_time = min_time
        self.ts_in_group = ts_in_group
        self.cells_x = cells_x
        self.cells_y = cells_y
        self.data = self.raw_data.copy()

    def prepare_time(self):
        """
        Переводит отметки времени к нулю (опционально) и в нужные единицы измерения
        """
        if self.min_time:
            self.data['t'] -= min(self.data['t'])
        self.data['t'] = self.data['t'] * self.t_coef

    def prepare_coordinates(self):
        """
        Переводит координаты из интервала 0..1 в 0..x_coef и 0..y_coef
        """
        self.data['x'] *= self.x_coef
        self.data['y'] *= self.y_coef

    def group_by_time(self):
        """

        """
        df = self.data.copy()
        df['t'] = [int(x) for x in df['t'] / self.ts_in_group]
        self.grouped_data = df.groupby('t').agg('tail', 1).reset_index().drop('index', 1)

    def trajectory_to_aois(self):
        """

        """
        self.get_aoi_list()
        aois = self.aois
        t_s, aoi_num = [], []
        for row in self.data.iterrows():
            t, x, y = row[1]
            t_s.append(t)
            no_aoi = True
            for aoi in aois.keys():
                if aois[aoi].includes(x, y):
                    aoi_num.append(aoi)
                    no_aoi = False
                    break
            if no_aoi:
                aoi_num.append(0)
        df = pd.DataFrame({'t': t_s, 'aoi': aoi_num})
        self.aoi_df = df.copy()

    def get_transition_matrix(self, empty_aoi=True, to_probabilities=True):
        """

        """
        if self.aoi_df is None:
            self.trajectory_to_aois()

        cells = self.cells_x * self.cells_y
        n_aois = cells + int(empty_aoi)

        aoi_df = self.aoi_df.copy()
        if not empty_aoi:
            aoi_df = aoi_df[aoi_df['aoi'] < cells].copy()

        aoi_seq = aoi_df['aoi'].values - 1

        transition_matrix = np.zeros((n_aois, n_aois))

        for from_, to_ in zip(aoi_seq[:-1], aoi_seq[1:]):
            transition_matrix[to_][from_] += 1

        if to_probabilities:
            colsums = sum(transition_matrix)
            colsums[colsums == 0] = 1
            transition_matrix /= colsums

        self.transition_matrix = transition_matrix.copy()
