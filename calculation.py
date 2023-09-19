from work import Work
from utils import (get_sita_by_t, sci_round, D_round, get_value_of_key,
                   find_by_key, get_temp_by_p, get_rou_by_t, kPa_2_mmHg,
                   get_miu_by_t, five_round, find_intersections)
from tray_paramater import tray_paramater
import numpy as np
import matplotlib.pyplot as plt

h_l_h_L = {
    'h_L': [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1],
    'h_l_1':
    [0.019, 0.029, 0.035, 0.04, 0.044, 0.047, 0.05, 0.052, 0.056, 0.0601],
    'h_l_2':
    [0.019, 0.025, 0.031, 0.037, 0.04, 0.043, 0.045, 0.049, 0.052, 0.058]
}


class Calculation:

    def __init__(self,
                 work: Work,
                 R,
                 tray_paramater=tray_paramater,
                 h_l_h_L=h_l_h_L,
                 u_multiple=0.6,
                 H_T=0.35,
                 h_L=0.05,
                 h_n=0.01,
                 d_o=0.005,
                 W_s=0.08,
                 W_c=0.05,
                 t_div_d_o=4,
                 delta=0.003,
                 C_o=0.79,
                 weir_type=0  # 0: 平堰, 1: 齿形堰
                 ):
        self.work = work
        self.R = R
        R_multiple = self.R_multiple = R / work.material.R_min
        self.thero_plates = work.get_thero_plates(R_multiple)
        self.real_plates = work.get_real_plates(R_multiple)
        tower_diameter = self.tower_diameter = work.get_tower_diameter(
            R / work.material.R_min, 0.6)
        self.D_rounded = tower_diameter['D_rounded']
        self.tray_paramater = tray_paramater
        self.standard_D = get_value_of_key(tray_paramater, 'D')
        self.h_l_h_L = h_l_h_L
        self.u_multiple = u_multiple
        self.H_T = H_T
        self.h_L = h_L
        self.weir_type = weir_type
        if weir_type == 1:
            self.h_n = h_n
        self.d_o = d_o
        self.W_s = W_s
        self.W_c = W_c
        self.delta = delta
        self.t_div_d_o = t_div_d_o
        self.C_o = C_o
        D_calculated = self.calculate_D()
        self.D = D_calculated['D']
        self.A_T = D_calculated['A_T']
        self.A_f = D_calculated['A_f']
        self.h_f = D_calculated['h_f']
        self.l_w = D_calculated['l_w']
        self.W_d = D_calculated['W_d']
        self.H_T = D_calculated['H_T']
        self.L_s = D_calculated['L_s']
        self.V_s = D_calculated['V_s']
        self.e_v = D_calculated['e_v']
        self.t = D_calculated['t']
        self.w_G = D_calculated['w_G']
        plate_0 = self.get_n_plate(0)
        self.h_P = plate_0['h_p']
        # self.A_T_div_A_f = D_calculated[''],

    def get_e_v(self, sita, w_G, H_T, h_f):
        e_v = 0.22 * (73 / sita) * (w_G / (12 * (H_T - h_f)))**3.2
        return e_v

    def calculate_D(self, n=0):
        work = self.work
        material = work.material
        H_T = self.H_T
        h_L = self.h_L
        u_multiple = self.u_multiple
        R_min = material.R_min
        R_multiple = self.R / R_min
        tower_diameter = work.get_tower_diameter(R_multiple,
                                                 u_multiple,
                                                 h_L=h_L,
                                                 H_T=H_T)
        V_s = tower_diameter['V_s']
        L_s = tower_diameter['L_s']
        sita = tower_diameter['sita']
        D = tower_diameter['D_rounded']

        def calculate(D):
            tray = find_by_key(self.tray_paramater, 'D', D)
            A_T = tray['A_T']
            for i in range(len(tray['H_T'])):
                H_T = tray['H_T'][i]
                for k in range(len(tray['A_f'])):
                    A_f = tray['A_f'][k]
                    w_G = V_s / (A_T - A_f)
                    h_f = 2.5 * h_L
                    e_v = self.get_e_v(sita, w_G, H_T, h_f)
                    if e_v < 0.1:
                        A_f = tray['A_f'][i]
                        t = H_T * A_f / L_s
                        if t > 5:
                            return {
                                'e_v': sci_round(e_v, 4),
                                't': sci_round(t, 2),
                                'H_T': H_T,
                                'A_T': A_T,
                                'A_f': A_f,
                                'w_G': sci_round(w_G),
                                'h_f': h_f,
                                'L_s': L_s,
                                'V_s': V_s,
                                'sita': sci_round(sita),
                                'D': D,
                                'l_w': tray['l_w'][k],
                                'W_d': tray['W_d'][k],
                                # 'l_w/D': tray['l_w/D'][k],
                                # 'A_f/A_T': tray['A_f/A_T'][k],
                            }
            D = D_round(D + 0.01, standard=self.standard_D)
            if D < max(self.standard_D):
                return calculate(D)

        return calculate(D)

    def get_h_ow(self, L_s, l_w, h_n=None, E=1):
        if self.weir_type == 1:
            if h_n is None:
                h_n = 0.01
            h_ow = 1.17 * (L_s * h_n / l_w)**(2 / 5)
        elif self.weir_type == 0:
            h_ow = 2.84 / 1000 * (L_s / l_w)**(2 / 3) * E
        return h_ow
        # H_ow = np.linspace(0, 0.05, 100)
        # L = 0.735 * (l_w / h_n) * (H_ow**(5 / 2) - (H_ow - h_n)**(5 / 2))
        # h_ow = np.interp(L_s, L, H_ow)
        # return h_ow

    def get_F_o(self, w_o, gama_v):
        F_o = w_o * np.sqrt(gama_v)
        return F_o

    def get_Delta(self, b, h_f, miu, L_s, Z_1, gama_L):
        delta = (0.215 * (250 * b + 1000 * h_f)**2 * miu *
                 (3600 * L_s) * Z_1) / ((1000 * b * h_f)**3 * gama_L)
        return delta

    def get_b(self, l_w, D):
        b = (l_w + D) / 2
        return b

    def get_Z_1(self, D, W_d):
        Z_1 = D - 2 * W_d
        return Z_1

    def calculate_weir_and_downcomer(self,
                                     l_w,
                                     W_d,
                                     D,
                                     L_s,
                                     h_f,
                                     gama_L,
                                     miu,
                                     h_L=0.05,
                                     h_n=0.01):
        h_ow = sci_round(self.get_h_ow(L_s, l_w, h_n), 4)
        b = self.get_b(l_w, D)
        Z_1 = self.get_Z_1(D, W_d)
        Delta = self.get_Delta(b, h_f, miu, L_s, Z_1, gama_L)
        h_w = h_L - h_ow
        h_w_rounded = five_round(h_w, 'up')
        h_L = sci_round(h_w + h_w_rounded, 4)
        h_o = h_w_rounded - 0.01
        return {
            'Delta': Delta,
            'h_ow': h_ow,
            'h_w': h_w,
            'h_w_rounded': h_w_rounded,
            'h_L': h_L,
            'Z_1': Z_1,
            'h_o_rounded': five_round(h_o, 'down'),
            'h_o': h_o,
            'b': b,
            'Z_1': Z_1,
        }

    def get_A_a(self, x, r):
        A_a = 2 * (x * np.sqrt(r**2 - x**2) + r**2 * np.arcsin(x / r))
        return A_a

    def get_A_o_div_A_a(self, t_div_d_o):
        A_o_div_A_a = 0.907 / t_div_d_o**2
        return A_o_div_A_a

    def get_hole(self, d_o, D, W_d, t_div_d_o=4, W_s=0.08, W_c=0.05):
        t = d_o * t_div_d_o
        A_o_div_A_a = self.get_A_o_div_A_a(t_div_d_o)
        x = sci_round(D / 2 - (W_d + W_s), 4)
        r = sci_round(D / 2 - W_c, 4)
        A_a = sci_round(self.get_A_a(x, r), 4)
        A_o = sci_round(A_a * A_o_div_A_a, 4)
        n = sci_round(1158 * 1000 / (t * 1000)**2 * A_a, 1)
        return {
            'A_o': A_o,
            'A_a': A_a,
            'n': n,
            'A_o_div_A_a': A_o_div_A_a,
            't': t,
            'x': x,
            'r': r
        }

    def get_h_c(self,
                d_o,
                w_o,
                gama_v,
                gama_L,
                delta,
                C_o,
                A_o_div_A_a=0,
                beta=1.15):
        """
        @reference: 浙江工业大学化工原理教研室: 化工原理课程设计资料——板式塔指导书, 34, 2017
        """
        if C_o is None:
            x = d_o / delta
            # TODO: auto calculate C_o
            pass
        h_c = None
        if d_o < 0.012:
            h_c = 0.051 * (w_o / C_o)**2 * (gama_v / gama_L) * (1 -
                                                                A_o_div_A_a**2)
        else:
            h_c = 0.051 * (w_o /
                           (C_o * beta))**2 * (gama_v /
                                               gama_L) * (1 - A_o_div_A_a**2)
        return {'h_c': h_c, 'C_o': C_o}

    def get_w_o(self, V_s, A_o):
        w_o = V_s / A_o
        return w_o

    def get_w_om(self, C_o, h_L, h_sita, gama_L, gama_v, d_o, beta=1.15):
        # if d_o < 0.003 or h_L < 0.03:
        #     w_om = 4.4 * C_o * np.sqrt((0.0051 + 0.05 * h_L) * gama_L / gama_v)
        # elif d_o > 0.012:
        #     w_om = 4.4 * beta * C_o * np.sqrt(
        #         (0.01 + 0.13 * h_L - h_sita) * gama_L / gama_v)
        # else:
        #     w_om = 4.4 * C_o * np.sqrt(
        #         (0.0056 + 0.13 * h_L - h_sita) * gama_L / gama_v)
        w_om = 4.4 * C_o * np.sqrt(
            (0.0056 + 0.13 * h_L - h_sita) * gama_L / gama_v)
        return w_om

    def get_h_sita(self, sita, gama_L, d_o):
        h_sita = (4 * sita) / (9810 * gama_L * d_o)
        return h_sita

    def get_K(self, w_o, w_om):
        K = w_o / w_om
        return K

    def get_h_l(self, F_o, h_L):
        """
        @reference: 浙江工业大学化工原理教研室: 化工原理课程设计资料——板式塔指导书, 34, 2017
        """
        h_l_h_L = self.h_l_h_L
        X = h_l_h_L['h_L']
        h_l = None
        if F_o < 17:
            Y = h_l_h_L['h_l_1']
            h_l = np.interp(h_L, X, Y)
        else:
            Y = h_l_h_L['h_l_2']
            h_l = np.interp(h_L, X, Y)
        return h_l

    def get_h_p(self, h_l, h_c):
        h_p = h_l + h_c
        return h_p

    def get_h_d(self, L_s, l_w, h_o):
        h_d = 0.153 * (L_s / (l_w * h_o))**2
        return h_d

    def get_H_d(self, h_d, h_p, h_L):
        H_d = h_d + h_p + h_L
        return H_d

    def get_h_f(self, h_L):
        h_f = 2.5 * h_L
        return h_f

    def get_w_f(self, L_s, A_f):
        w_f = L_s / A_f
        return w_f

    def get_t(self, H_T, w_f):
        t = H_T / w_f
        return t

    def get_w_Gm(self, sita, H_T, h_f):
        """
        @formula: $ w_{G,m} = 2.16 \sita^0.312 (H_T - h_f)$

        @reference: 浙江工业大学化工原理教研室: 化工原理课程设计资料——板式塔指导书, 38, 2017    
        """
        w_Gm = 2.16 * sita**0.312 * (H_T - h_f)
        return w_Gm

    def calculate_material_parmaters(self, n):
        work = self.work
        plates = self.thero_plates
        x = plates['x'][n]
        y = plates['y'][n]
        p = sci_round((work.p_atm + self.h_P * n * 9.807) if n > 0 else work.p_atm)
        P_solute = sci_round( p * y / x)
        t = sci_round(get_temp_by_p(work.antoine['solute'], kPa_2_mmHg(P_solute)))
        rou_solute = sci_round(get_rou_by_t(work.solute_rou_t, t))
        rou_solvent = sci_round(get_rou_by_t(work.solvent_rou_t, t))
        sita_solute = sci_round(get_sita_by_t(work.solute_sita_t, t))
        sita_solvent = sci_round(get_sita_by_t(work.solvent_sita_t, t))
        miu_solute = sci_round(get_miu_by_t(work.solute_miu_t, t))
        miu_solvent = sci_round(get_miu_by_t(work.solvent_miu_t, t))
        M_v = sci_round(work.get_M_v(y))
        M_L = sci_round(work.get_M_L(x))
        gama_v = sci_round(work.get_gama_v(p, M_v, t))
        gama_L = sci_round(work.get_gama_L(self.R_multiple))
        sita = sci_round(sita_solute * x + sita_solvent * (1 - x), 4)
        miu = sci_round(work.get_average_miu(miu_solute, miu_solvent), 4)
        L = sci_round(self.R * self.work.material.D, 4)
        L_s = sci_round(L * M_L/3600/gama_L, 4)
        V = sci_round((self.R + 1) * self.work.material.D, 4)
        V_s = sci_round(V * M_v/3600/gama_v, 4)
        return {
            'P_solute': P_solute,
            't': t,
            'rou_solute': rou_solute,
            'rou_solvent': rou_solvent,
            'sita_solute': sita_solute,
            'sita_solvent': sita_solvent,
            'miu_solute': miu_solute,
            'miu_solvent': miu_solvent,
            'M_v': M_v,
            'M_L': M_L,
            'gama_v': gama_v,
            'gama_L': gama_L,
            'sita': sita,
            'miu': miu,
            'x': x,
            'y': y,
            'p': p,
            'L': L,
            'L_s': L_s,
            'V': V,
            'V_s': V_s
        }

    def get_n_plate(self, n):
        material_parmaters = self.calculate_material_parmaters(n)
        # D_calculation = self.calculate_D()
        l_w = self.l_w
        W_d = self.W_d
        D = self.D
        H_T = self.H_T
        h_L = self.h_L
        h_n = self.h_n if self.weir_type == 1 else None
        h_f = self.h_f
        gama_L = material_parmaters['gama_L']
        miu = material_parmaters['miu']
        L_s = self.L_s
        weir_and_downcomer = self.calculate_weir_and_downcomer(
            l_w, W_d, D, L_s, h_f, gama_L, miu, h_L, h_n)
        d_o = self.d_o
        W_s = self.W_s
        W_c = self.W_c
        t_div_d_o = self.t_div_d_o
        hole = self.get_hole(d_o, D, W_d, t_div_d_o, W_s, W_c)
        gama_v = material_parmaters['gama_v']
        delta = self.delta
        V_s = self.V_s
        A_o = hole['A_o']
        w_o = V_s / A_o
        A_o_div_A_a = self.get_A_o_div_A_a(self.t_div_d_o)
        C_o = self.C_o
        h_c = sci_round(
            self.get_h_c(d_o,
                         w_o,
                         gama_v,
                         gama_L,
                         delta,
                         C_o,
                         A_o_div_A_a=A_o_div_A_a)['h_c'], 4)
        sita = material_parmaters['sita']
        h_sita = sci_round(self.get_h_sita(sita, gama_L, d_o), 4)
        w_om = sci_round(self.get_w_om(C_o, h_L, h_sita, gama_L, gama_v, d_o),
                         4)
        K = sci_round(self.get_K(w_o, w_om), 4)
        h_w = weir_and_downcomer['h_w_rounded']
        A_T = self.A_T
        A_f = self.A_f
        F_o = sci_round(self.get_F_o(w_o, gama_v), 4)
        h_l = sci_round(self.get_h_l(F_o, h_L), 4)
        h_o = weir_and_downcomer['h_o_rounded']
        load_performance = self.get_load_performance(A_o, C_o, K, h_w, h_n,
                                                     l_w, sita, gama_L, gama_v,
                                                     d_o, A_T, A_f, H_T, h_l,
                                                     h_o, h_sita)
        h_p = sci_round(self.get_h_p(h_l, h_c), 4)
        h_d = sci_round(self.get_h_d(L_s, l_w, h_o), 4)
        H_d = sci_round(self.get_H_d(h_d, h_p, h_L), 4)
        w_f = sci_round(self.get_w_f(L_s, A_f), 4)
        t = sci_round(A_f * H_T / L_s, 4)
        w_G = self.w_G
        e_v = sci_round(self.get_e_v(sita, w_G, H_T, h_f), 4)
        return {
            'weir_and_downcomer': weir_and_downcomer,
            'hole': hole,
            'h_c': h_c,
            'h_sita': h_sita,
            'w_om': w_om,
            'K': K,
            'delta': delta,
            'load_performance': load_performance,
            'w_o': w_o,
            'h_l': h_l,
            'F_o': F_o,
            'h_p': h_p,
            'h_d': h_d,
            'H_d': H_d,
            'h_w': h_w,
            'w_f': w_f,
            't': t,
            'e_v': e_v
        }

    def draw_load_performance(self, n):
        def draw_func(fig=None, ax=None):
            n_plate = self.get_n_plate(n)
            load_performance = n_plate['load_performance']
            leaky_line = load_performance['leaky_line']
            excess_fog_line = load_performance['excess_fog_line']
            flooding_line = load_performance['flooding_line']
            operating_line = load_performance['operating_line']
            L_min = load_performance['L_min']
            L_max = load_performance['L_max']
            plt.xlabel('$\mathregular{L/(m^2/s)}$')
            plt.ylabel('$\mathregular{V/(m^3/s)}$')
            plt.xlim(0, L_max + 0.001)
            plt.ylim(leaky_line['V'][0] - 0.1, max(flooding_line['V'][0], excess_fog_line['V'][0])  + 0.1)
            plt.plot(leaky_line['L'], leaky_line['V'], label='漏液线')
            plt.plot(excess_fog_line['L'],
                     excess_fog_line['V'],
                     label='过量雾沫夹带线')
            plt.plot(flooding_line['L'], flooding_line['V'], label='液泛线')
            plt.axvline(x=L_min, color='r', linestyle='-', label='液相下限线')
            plt.axvline(x=L_max, color='r', linestyle='-', label='液相上限线')
            plt.plot(operating_line['L'],
                     operating_line['V'],
                     label='操作线')
            plt.plot(self.L_s, self.V_s, 'o', label='操作点')
            plt.legend()
            plt.title(f"n={n + 1}, V_max/V_min={load_performance['V_max_div_V_min']}")
        return draw_func

    def get_leaky_line(self, A_o, C_o, K, h_w, h_n, l_w, h_sita, gama_L,
                       gama_v, d_o, L_start, L_end):
        # h_sita = self.get_h_sita(sita, gama_L, d_o)

        def get_V(L):
            h_ow = self.get_h_ow(L, l_w, h_n)
            h_L = h_ow + h_w
            w_om = self.get_w_om(C_o, h_L, h_sita, gama_L, gama_v, d_o)
            V = K * A_o * w_om
            return V

        L = np.linspace(L_start, L_end, 100).tolist()
        V = list(map(get_V, L))

        return {
            'L': L,
            'V': V,
        }

    def get_excess_fog_line(self, A_T, A_f, H_T, l_w, h_w, h_n, sita, L_start,
                            L_end):

        def get_V(L):
            h_ow = self.get_h_ow(L, l_w, h_n)
            h_L = h_w + h_ow
            h_f = self.get_h_f(h_L)
            V = ((0.1 * sita) / 0.0057)**(1 / 3.2) * (A_T - A_f) * (H_T - h_f)
            return V

        L = np.linspace(L_start, L_end, 100).tolist()
        V = list(map(get_V, L))
        return {
            'L': L,
            'V': V,
        }

    def get_lower_L_line(self, l_w, h_n=None, E=1):
        if self.weir_type == 1:
            if h_n is None:
                h_n = 0.01
            L_min = (0.006 / 1.17)**2.5 * (l_w / h_n)
        elif self.weir_type == 0:
            L_min = np.power(0.006 * 1000 / 2.84 / E, 1 / 3.2) * l_w / 3600
        return L_min

    def get_upper_L_line(self, A_f, H_T):
        L_max = A_f * H_T / 5
        return L_max

    def get_flooding_line(self, H_T, h_w, h_l, gama_L, gama_v, A_o, C_o, l_w,
                          h_n, h_o, L_start, L_end):

        def get_V(L):
            h_ow = self.get_h_ow(L, l_w, h_n)
            h_d = self.get_h_d(L, l_w, h_o)
            V = A_o * C_o * np.sqrt(
                (0.5 *
                 (H_T - h_w) - h_ow - h_d - h_l) * gama_L / (0.051 * gama_v))
            return V

        L = np.linspace(L_start, L_end, 100).tolist()
        V = list(map(get_V, L))
        return {
            'L': L,
            'V': V,
        }

    def get_operating_line(self, end=0.1):
        L_s = self.L_s
        V_s = self.V_s
        k = V_s / L_s
        L = np.linspace(0, end, 100).tolist()
        V = list(map(lambda x: k * x, L))
        return {
            'L': L,
            'V': V,
        }

    def get_load_performance(self, A_o, C_o, K, h_w, h_n, l_w, sita, gama_L,
                             gama_v, d_o, A_T, A_f, H_T, h_l, h_o, h_sita):
        L_min = self.get_lower_L_line(l_w, h_n)
        L_max = self.get_upper_L_line(self.A_f, self.H_T)
        leaky_line = self.get_leaky_line(A_o, C_o, K, h_w, h_n, l_w, h_sita,
                                         gama_L, gama_v, d_o, 0, L_max + 0.001)
        excess_fog_line = self.get_excess_fog_line(A_T, A_f, H_T, l_w, h_w,
                                                   h_n, sita, 0, L_max + 0.001)
        flooding_line = self.get_flooding_line(H_T, h_w, h_l, gama_L, gama_v,
                                               A_o, C_o, l_w, h_n, h_o, 0,
                                               L_max + 0.001)
        operating_line = self.get_operating_line(L_max)
        intersection_1 = find_intersections(operating_line['L'], operating_line['V'], leaky_line['L'], leaky_line['V'])
        intersection_2 = find_intersections(operating_line['L'], operating_line['V'], excess_fog_line['L'], excess_fog_line['V'])
        intersection_3 = find_intersections(operating_line['L'], operating_line['V'], flooding_line['L'], flooding_line['V'])
        V_min = np.min([intersection_1['Y'][0], intersection_3['Y'][0]])
        V_max = np.min([intersection_2['Y'][0], intersection_3['Y'][0]])
        return {
            'L_min': L_min,
            'L_max': L_max,
            'L_max_div_L_min': sci_round(L_max / L_min),
            'leaky_line': leaky_line,
            'excess_fog_line': excess_fog_line,
            'flooding_line': flooding_line,
            'operating_line': operating_line,
            'V_min': V_min,
            'V_max': V_max,
            'V_max_div_V_min': sci_round(V_max / V_min),
            'L_s': self.L_s,
            'V_s': self.V_s,
        }
