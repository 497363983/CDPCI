from utils import sci_round, get_zero_point, one_D_matching, draw
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

alcohol_water = {
    # T-x-y
    'x': [0, 0.02, 0.06, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
    'y': [
        0, 0.134, 0.304, 0.418, 0.578, 0.665, 0.729, 0.779, 0.825, 0.87, 0.915,
        0.958, 1
    ],
    't':
    [100, 96.4, 91.2, 87.7, 81.7, 78, 75.3, 73.1, 71.2, 69.3, 67.6, 66, 64.5],

    # 'p_alcohol': [101.3, 123.3, 140.6, 180.4, 252.6, 349.8],
    # 'p_water': [24.5, 31.2, 38.5, 47.3, 70.1, 101.3],
    # 't_p': [64.5, 70, 75, 80, 90, 100]
}


class Material:

    def __init__(
            self,
            capacity: float | int,  # 10^4t/year
            time: int | float,  # h/year
            w_F: float,  # %
            x_o: float,  # %
            eta: float,  # %
            initial_temp: float | int,  # ℃
            M_solute: float | int = 32.04,  # g/mol
            M_solvent: float | int = 18.02,  # g/mol
            phase_equilibrium: dict = alcohol_water,
            solute: str = "alcohol",
            solvent: str = "water") -> None:
        self.M_solute = M_solute
        self.M_solvent = M_solvent
        self.solvent = solvent
        self.solute = solute
        self.initial_temp = initial_temp
        self.handling_capacity = capacity
        self.time = time
        w_F = w_F if w_F < 1 else w_F / 100
        x_o = x_o if x_o < 1 else x_o / 100
        eta = eta if eta < 1 else eta / 100
        F_kg = sci_round(capacity * 10000 * 1000 / time, 2)
        self.F_kg = F_kg
        self.x_o = x_o
        self.eta = eta
        F = self.F = sci_round(F_kg * w_F / M_solute + F_kg * (1 - w_F) / M_solvent, 2)
        x_F = self.x_F = sci_round((w_F / M_solute) / (w_F / M_solute + (1 - w_F) / M_solvent),
                                   2)
        x_D = self.x_D = sci_round((x_o / M_solute) / (x_o / M_solute + (1 - x_o) / M_solvent),
                                   4)
        D = self.D = sci_round(eta * F * x_F / x_D, 2)
        W = self.W = sci_round(F - D, 2)
        self.x_w = sci_round((F * x_F - D * x_D) / W, 4)
        self.w_F = w_F
        self.equations = {'F': "F=\\frac {} {}"}
        self.phase_equilibrium = phase_equilibrium
        self.t_b, self.t_d = self.get_t_b_t_d()
        self.y_e, self.R_min = self.get_y_e_R_min()

    # def draw_T_x_y(self):
    #     phase_equilibrium = pd.DataFrame(self.phase_equilibrium)
    #     draw_line(phase_equilibrium, ['x', 'y'], 't', 'x/y', 'temp/℃', 'T-x-y')

    def draw_y_x(self, size=(12, 6), save: bool = False, filename: str = None):
        def draw_func():
            phase_equilibrium = self.phase_equilibrium
            y_e = self.y_e
            x = np.array(phase_equilibrium['x'])
            y = np.array(phase_equilibrium['y'])
            x_new, y_smooth = one_D_matching(x, y)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.plot(x, y, 'o')
            plt.plot(x_new, y_smooth, label="相平衡曲线")
            plt.plot([0, 1], [0, 1], linestyle='-')
            plt.plot([self.x_F, self.x_F], [self.x_F, 1],
                     'o',
                     linestyle='-',
                     label="q线")
            plt.plot(self.x_F, y_e, 'o')
            plt.plot([self.x_D, self.x_F], [self.x_D, y_e], 'o', linestyle='-')
            plt.plot([self.x_w, self.x_F], [self.x_w, y_e], 'o', linestyle='-')
            plt.text(self.x_F + 0.01, self.x_F - 0.01, 'f(x_F, x_F)')
            plt.text(self.x_F + 0.02, 1, 'q=1')
            plt.text(self.x_F + 0.01, y_e - 0.01, f'e({self.x_F}, {y_e})')
            plt.text(self.x_D + 0.01, self.x_D - 0.01, 'a(x_D, x_D)')
            plt.text(self.x_w + 0.01, self.x_w - 0.01, 'b(x_w, x_w)')
            plt.legend()
        draw(draw_func=draw_func, title='y-x', size=size, save=save, filename=filename)

    def draw_T_x_y(self,
                   save: bool = False,
                   filename: str = None,
                   size=(12, 6)) -> dict:
        def draw_func():
            phase_equilibrium = self.phase_equilibrium
            bubble_Y = np.array(phase_equilibrium['x'])
            dew_Y = np.array(phase_equilibrium['y'])
            X = np.array(phase_equilibrium['t'])
            x_new, t_smooth_x = one_D_matching(bubble_Y, X)
            y_new, t_smooth_y = one_D_matching(dew_Y, X)
            bubble_temp = self.t_b
            dew_temp = self.t_d
            plt.xlabel('x/y')
            plt.ylabel('temp/℃')
            plt.plot(bubble_Y, X, 'o')
            plt.plot(y_new, t_smooth_y, label="露点线")
            plt.plot(dew_Y, X, 'o')
            plt.plot(x_new, t_smooth_x, label="泡点线")
            plt.plot([self.x_F, self.x_F], [X[0], X[-1]], linestyle='-')
            plt.plot([self.x_F, self.x_F], [bubble_temp, dew_temp], 'o')
            plt.text(self.x_F + 0.02, bubble_temp + 0.02, f't_b({self.x_F}, {bubble_temp})')
            plt.text(self.x_F + 0.02, dew_temp + 0.02, f't_d({self.x_F}, {dew_temp})')
            plt.text(self.x_F, X[-1], 'x_F')
            plt.legend()
        draw(draw_func=draw_func, title="T-x-y", save=save, filename=filename)

    def get_t_b_t_d(self):
        phase_equilibrium = self.phase_equilibrium
        phase_equilibrium = pd.DataFrame.from_dict(phase_equilibrium)
        phase_equilibrium.sort_values(by='t', inplace=True)
        phase_equilibrium = phase_equilibrium.to_dict(orient='list')
        bubble_Y = np.array(phase_equilibrium['x'])
        dew_Y = np.array(phase_equilibrium['y'])
        X = np.array(phase_equilibrium['t'])
        roots_bubble_X = get_zero_point(X, bubble_Y - self.x_F)
        roots_dew_X = get_zero_point(X, dew_Y - self.x_F)
        bubble_temp = sci_round(roots_bubble_X[0], 2)
        dew_temp = sci_round(roots_dew_X[0], 2)
        return (bubble_temp, dew_temp)

    def get_y_e_R_min(self):
        phase_equilibrium = self.phase_equilibrium
        Y = np.array(phase_equilibrium['x'])
        X = np.array(phase_equilibrium['y'])
        y_e = sci_round(get_zero_point(X, Y - self.x_F)[0], 4)
        R_min = sci_round((self.x_D - y_e) / (y_e - self.x_F), 4)
        return (y_e, R_min)
