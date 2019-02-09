import numpy as np
from AOI.Rectangle import Rectangle


class AOI:

    def __init__(self, x_coef, y_coef, cells_x, cells_y):
        """

        """
        self.x_coef = x_coef
        self.y_coef = y_coef
        self.cells_x = cells_x
        self.cells_y = cells_y

    def get_aoi_list(self):
        """

        """
        x_step = self.x_coef / self.cells_x
        y_step = self.y_coef / self.cells_y

        xs = np.arange(0, self.x_coef + x_step, x_step)
        ys = np.arange(0, self.y_coef + y_step, y_step)

        aoi_num = 1
        aois = dict()

        for y_0, y_1 in zip(ys[:-1], ys[1:]):
            for x_0, x_1 in zip(xs[:-1], xs[1:]):
                aois[aoi_num] = Rectangle(x_0, x_1, y_0, y_1)
                aoi_num += 1

        aois[aoi_num] = Rectangle(-np.inf, np.inf, -np.inf, np.inf)

        self.aois = aois.copy()
