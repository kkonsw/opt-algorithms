# выполнил: Кузнецов Константин
# группа: 381503-3


import math
from tabulate import tabulate
from py_expression_eval import Parser
import matplotlib.pyplot as plt


class Function:
    def __init__(self, s):
        self.parser = Parser()
        self.s = s
        self.expr = self.parser.parse(s)

    def eval(self, x):
        return self.expr.evaluate({'x': x})


class FunctionPlotter:
    def __init__(self, f, a, b, step=0.01):
        self.func = f
        self.f = f.eval
        self.a = a
        self.b = b
        self.step = step

    def plot_function(self):
        xs = []
        ys = []
        x = self.a
        xs.append(x)
        ys.append(self.f(x))

        while x < self.b:
            x += self.step
            xs.append(x)
            ys.append(self.f(x))

        plt.plot(xs, ys, 'b', label='function')
        plt.ylabel('f(x)')
        plt.xlabel('x')
        plt.suptitle(self.func.s)

    def plot_minimum(self, min):
        plt.plot(min, self.f(min), 'D', label='minimum')

    def legend(self):
        plt.legend()

    def show(self):
        plt.show()

    def clear(self):
        plt.clf()


# метод золотого сечения
def gss(f, a, b, eps, n, table):
    step = 0
    table[step] = [step, a, b, f(a), f(b)]

    gr = (math.sqrt(5) + 1) / 2.0  # золотое сечение
    x1 = b - (b - a) / gr
    x2 = a + (b - a) / gr

    while b - a > eps and step < n:
        step += 1

        if f(x1) < f(x2):
            b = x2
        else:
            a = x1

        table[step] = [step, a, b, f(a), f(b)]
        x1 = b - (b - a) / gr
        x2 = a + (b - a) / gr

    return [(b + a) / 2.0, step]


# метод дихотомии-2
def dichotomy(f, a, b, eps, n, table):
    step = 0
    table[step] = [step, a, b, f(a), f(b)]

    c  = (a + b) / 2.0
    x1 = (a + c) / 2.0
    x2 = (c + b) / 2.0

    while b - a > eps and step < n:
        step += 1
        valc = f(c)
        val1 = f(x1)
        val2 = f(x2)

        if val1 <= valc and valc < val2:
            b = c
            c = x1
        else:
            if val1 > valc and valc <= val2:
                a = x1
                b = x2
                c = (a + b) / 2.0
            else:
                a = c
                c = x2

        table[step] = [step, a, b, f(a), f(b)]
        x1 = (a + c) / 2.0
        x2 = (c + b) / 2.0

    return [(b + a) / 2.0, step]


def menu():
    print('введите функцию: [например (x-1)^2]')
    f = Function(input('f(x) = '))
    a = float(input('[левая граница]  a = '))
    b = float(input('[правая граница] b = '))
    max_steps = int(input('[макс. шагов]    n = '))
    eps = float(input('[точность]     eps = '))

    print('\n[1] дихотомия-2 \n[2] метод золотого сечения', )
    method = input('выберите метод: ')
    table = {0: [0, 0, 0, 0, 0]}
    min = []
    if method == '1':
        min = dichotomy(f.eval, a, b, eps, max_steps, table)
    else:
        min = gss(f.eval, a, b, eps, max_steps, table)
    print('найден минимум ф-ии', f.eval(min[0]), 'в точке', min[0], 'за', min[1], 'шагов')

    # печать таблицы
    print(tabulate(list(table.values()), headers=['step', 'a', 'b', 'f(a)', 'f(b)']))

    # график функции и точки минимума
    plot = FunctionPlotter(f, a, b)
    plot.clear()
    plot.plot_function()
    plot.plot_minimum(min[0])
    plot.legend()
    plot.show()


if __name__ == '__main__':
    menu()
    while input('повторить? [y/n]: ').lower().strip()[0] == 'y':
        print()
        menu()
