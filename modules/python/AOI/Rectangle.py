class Rectangle:
    def __init__(self, x0, x1, y0, y1):
        """
        Создаёт прямоугольник с углами в заданных координатах
        """
        if x0 == x1 or y0 == y1:
            print('Rectangle must not be zero area.')

        if x0 > x1:
            x1, x0 = x0, x1
        if y0 > y1:
            y1, y0 = y0, y1

        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1

    def includes(self, x, y, include_border=False):
        """
        Проверяет попадание заданной точки в данный прямоугольник
        """

        def between(val, min_, max_, includes=False):
            """
            Проверка попадания в интервал
            """
            if includes:
                return (val > min_) & (val <= max_)
            else:
                return (val > min_) & (val < max_)

        x_is_in = between(x, self.x0, self.x1, include_border)
        y_is_in = between(x, self.y0, self.y1, include_border)

        return x_is_in & y_is_in