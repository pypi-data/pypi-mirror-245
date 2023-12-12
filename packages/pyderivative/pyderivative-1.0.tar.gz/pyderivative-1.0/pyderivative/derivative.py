class Derivative():
    def __init__(self, func, e=0.01, grid=False):
        self.func = func
        self.e = e
        self.grid = grid

    def tailor_app(self, x0):
        '''
        :param x0: the point of calculation of the derivative by Tailor approximation
        :return: derivative
        '''
        if self.grid:
            raise Exception('The function is set by the grid!')
        try:
            return (self.func(x0 + self.e) - self.func(x0 - self.e)) / (2 * self.e)
        except:
            raise Exception('error using the function!')

    def polinom_app(self, x0):
        '''
        :param x0: the point of calculation of the derivative by polinom approximation
        :return: derivative
        '''
        if self.grid:
            raise Exception('The function is set by the grid!')
        try:
            return (self.func(x0 + self.e) - self.func(x0)) / self.e
        except:
            raise Exception('error using the function!')

    def second_derivative(self, x0):
        '''
        :param x0: the point of calculation of the second derivative
        :return: derivative
        '''
        if self.grid:
            raise Exception('The function is set by the grid!')
        try:
            return (self.func(x0 - self.e) - 2 * self.func(x0) + self.func(x0 + self.e)) / self.e ** 2
        except:
            raise Exception('error using the function!')

    '''
    point patterns
    '''
    def threepoint_pattern(self, x0, second_deriv = False):
        '''
        :param x0: the point of calculation
        :param second_deriv: boolean value indicating the degree of the derivative
        :return: first or second derivative
        '''
        if not self.grid:
            raise Exception('The function is set by the grid!')
        try:
            lst = list(self.func.keys())
            i = lst.index(x0)
            h = abs(lst[i] - lst[i + 1])
            if not second_deriv:
                return (self.func[lst[i+1]] - self.func[lst[i-1]]) / (2 * h)
            else:
                return (self.func[lst[i-1]] - 2 * self.func[lst[i]] + self.func[lst[i+1]]) / h ** 2
        except:
            raise Exception('error using the function!')
