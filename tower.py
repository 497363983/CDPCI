from typing import Optional
import matplotlib.pyplot as plt
import numpy as np
from utils import sci_round, get_c_p_by_t, get_latent_heat_t, get_landa_by_t, get_miu_by_t, get_rou_by_t
from heat_tubes import heat_tubes
from abc import abstractmethod
from pipe import pipe


class Plate:

    def __init__(self,
                 x,
                 y,
                 index: int,
                 load_perdormance,
                 type: str = "enriching"):
        self.x = x
        self.y = y
        self.index = index
        self.type = type
        self.load_perdormance = load_perdormance

    def draw_load_perdormance(self):

        def draw_func(fig=None, ax=None):
            load_performance = self.load_perdormance
            leaky_line = load_performance['leaky_line']
            excess_fog_line = load_performance['excess_fog_line']
            flooding_line = load_performance['flooding_line']
            operating_line = load_performance['operating_line']
            L_min = load_performance['L_min']
            L_max = load_performance['L_max']
            L_s = load_performance['L_s']
            V_s = load_performance['V_s']
            plt.xlabel('$\mathregular{L/(m^2/s)}$')
            plt.ylabel('$\mathregular{V/(m^3/s)}$')
            plt.xlim(0, L_max + 0.001)
            plt.ylim(leaky_line['V'][0] - 0.1,
                     max(flooding_line['V'][0], excess_fog_line['V'][0]) + 0.1)
            plt.plot(leaky_line['L'], leaky_line['V'], label='漏液线')
            plt.plot(excess_fog_line['L'],
                     excess_fog_line['V'],
                     label='过量雾沫夹带线')
            plt.plot(flooding_line['L'], flooding_line['V'], label='液泛线')
            plt.axvline(x=L_min, color='r', linestyle='-', label='液相下限线')
            plt.axvline(x=L_max, color='r', linestyle='-', label='液相上限线')
            plt.plot(operating_line['L'], operating_line['V'], label='操作线')
            plt.plot(L_s, V_s, 'o', label='操作点')
            plt.legend()
            plt.title(
                f"n={self.index + 1}, V_max/V_min={load_performance['V_max_div_V_min']}"
            )

        return draw_func


class Floor:

    def __init__(self,
                 plates: tuple[int, int],
                 H: Optional[float],
                 index,
                 is_human=False):
        self.plates = plates
        self.H = H
        self.is_human = is_human
        self.index = index


class Tower:

    def __init__(
            self,
            plates: list[Plate],
            N_r,  # 精馏段塔板数
            N_s,  # 提馏段塔板数
            H_T=0.35,  # m 塔板间距
            H_bottom=1,  # m 最后一块板到塔底的距离
            H_top=0.7,  # m 第一块板到塔顶距离
            H_in=0.8,  # m 进料处板间距
            H_human=0.8,  # m 开人孔处间距
            H_heat=3,  # m 间接蒸汽加热裙座高度
            D_human=0.5,  # m 人孔直径
            N_human_dis=10,  # 块板 人孔间距
            human_start=4,  # 人孔开始的层数
            h_in=0.3,  # 进料口距离进料段底部高度
    ) -> None:
        self.plates = plates
        self.N_r = N_r
        self.N_s = N_s
        self.N = N_r + N_s
        self.H_T = H_T
        self.H_bottom = H_bottom
        self.H_top = H_top
        self.H_in = H_in
        self.H_human = H_human
        self.H_heat = H_heat
        self.D_human = D_human
        self.N_human_dis = N_human_dis
        self.human_start = human_start
        self.h_in = h_in
        self.floors = self.get_floors()
        self.H = sci_round(self.get_H())
        self.input_H = sci_round(self.get_input_H())

    def get_H(self):
        floor_H = np.sum([floor.H for floor in self.floors])
        H = floor_H + self.H_bottom + self.H_heat
        return H

    def get_input_H(self):
        input_H = np.sum([
            floor.H for floor in self.floors if floor.index > self.N_r
        ]) + self.H_bottom + self.H_heat + self.h_in
        return input_H

    def get_floors(self):
        floors = []
        for i in range(self.N - 1):
            is_human = False
            H = self.H_T
            if (i + 1 == self.human_start) or (i == self.N - 2) or (
                (i + 1 > self.human_start) and
                (i + 1 - self.human_start) % self.N_human_dis == 0):
                is_human = True
                H = self.H_human
            if i + 1 == self.N_r:
                H = self.H_in
            if i == 0:
                H = self.H_top
            floor = Floor(plates=(i, i + 1),
                          H=H,
                          index=i + 1,
                          is_human=is_human)
            floors.append(floor)
        return floors

    def __str__(self):
        return f"Tower is {self.H} meters tall"

    def __len__(self):
        return len(self.plates)


alcohol_c_p = {
    't': [25, 50, 75, 100, 125, 150],
    'c_p': [1.32, 1.72, 2.17, 2.63, 3.09, 3.53]
}

alcohol_latent_heat = {
    't': [
        0, 10, 20, 25, 30, 40, 50, 60, 64.7, 70, 80, 90, 100, 110, 120, 130,
        140, 150, 160, 170, 180, 190, 200
    ],
    'latent_heat': [
        1201.854, 1190.2172500000001, 1177.0115, 1169.82025,
        1162.3675000000003, 1146.2852500000001, 1128.8955, 1110.3290000000002,
        1101.1765000000003, 1093.07, 1069.40425, 1047.17675,
        1023.6417499999999, 998.53775, 971.7340000000002, 943.09975,
        912.2427500000001, 878.77075, 842.0300000000001, 801.4975,
        755.9965000000001, 704.481, 644.859
    ]
}

water_c_p = {
    't': [0, 20, 50, 100, 150],
    'c_p': [4.215, 4.181, 4.180, 4.215, 4.310]
}

steam_latent_heat = {
    't': [
        0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85,
        90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 160, 170
    ],
    'latent_heat': [
        2491.3, 2480, 2468.6, 2457.8, 2446.3, 2433.9, 2426.7, 2412.6, 2401.1,
        2389.5, 2378.1, 2366.5, 2355.1, 2343.4, 2331.2, 2315.7, 2307.3, 2295.3,
        2283.1, 2271, 2258.4, 2245.5, 2232.4, 2221, 2205.2, 2193.1, 2177.6,
        2166, 2148.7, 2137.5, 2118.5, 2087.1, 2054
    ]
}

landa_water = {
    't': [0, 5, 10, 15, 20, 25, 30],
    'landa': [0.622, 0.615, 0.605, 0.595, 0.585, 0.574, 0.563]
}

water_rou_t = {
    't': [
        5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0,
        11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0,
        17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0,
        23.5, 24.0, 24.5, 25.0, 25.5, 26.0, 26.5, 27.0, 27.5, 28.0, 28.5, 29.0,
        29.5, 30.0, 30.5, 31.0, 31.5, 32.0, 32.5, 33.0, 33.5, 34.0, 34.5
    ],
    'rou': [
        999.992, 999.982, 999.968, 999.951, 999.930, 999.905, 999.876, 999.844,
        999.809, 999.770, 999.728, 999.682, 999.633, 999.580, 999.525, 999.466,
        999.404, 999.339, 999.271, 999.200, 999.126, 999.050, 998.970, 998.888,
        998.802, 998.714, 998.623, 998.530, 998.433, 998.334, 998.232, 998.128,
        998.021, 997.911, 997.799, 997.685, 998.567, 997.448, 997.327, 997.201,
        997.074, 996.944, 996.813, 996.679, 996.542, 996.403, 996.262, 996.119,
        995.974, 995.826, 995.676, 995.524, 995.369, 995.213, 995.054, 994.894,
        994.731, 994.566, 994.399, 994.230
    ]
}


class Heat_Exchanger:

    def __init__(
            self,
            t_h1,
            t_h2,
            t_c1,
            t_c2,
            x,
            K,
            name="换热器",
            u=1.5,  # m/s 管内流速
            R_SO=0.000308,  # m^2K/W
            R_Si=0.000172,  # m^2K/W
            pi=np.pi,
            A_margin=0.2,
            k_loss=1,
            M_solute=32.04,
            M_solvent=18.02,
            solute_c_p_dict: str | dict = alcohol_c_p,
            solvent_c_p_dict: str | dict = water_c_p,
            cooling_c_p_dict: str | dict = water_c_p,
            solute_r_dict: str | dict = alcohol_latent_heat,
            solvent_r_dict: str | dict = steam_latent_heat,
            steam_r_dict: str | dict = steam_latent_heat,
            heat_tubes: dict = heat_tubes,
            landa_water: dict = landa_water) -> None:
        # self.V = V
        # self.M_v = M_v
        self.k_loss = k_loss
        self.K = K
        self.u = u
        self.name = name
        self.t_c1 = t_c1
        self.t_c2 = t_c2
        self.R_SO = R_SO
        self.R_Si = R_Si
        self.pi = pi
        self.t_h1 = t_h1
        self.t_h2 = t_h2
        self.x = x
        self.M_solute = M_solute
        self.M_solvent = M_solvent
        self.A_margin = A_margin
        self.solute_c_p_dict = solute_c_p_dict
        self.solvent_c_p_dict = solvent_c_p_dict
        self.cooling_c_p_dict = cooling_c_p_dict
        self.solute_r_dict = solute_r_dict
        self.solvent_r_dict = solvent_r_dict
        self.steam_r_dict = steam_r_dict
        self.heat_tubes = heat_tubes
        self.landa_water = landa_water
        self.tubes_ruler = [(min(tube["A"]), max(tube["A"]))
                            for tube in heat_tubes]
        self.t_avc = sci_round(np.mean([t_c1, t_c2]))
        self.t_avh = sci_round(np.mean([t_h1, t_h2]))
        # average_temp = self.average_temp = sci_round(np.mean([t_c1, t_c2]))
        # self.c_p_solute = sci_round(get_c_p_by_t(solute_c_p_dict, average_temp))
        # self.c_p_solvent = sci_round(get_c_p_by_t(solvent_c_p_dict, average_temp))
        delta_t_1 = self.delta_t_1 = sci_round(t_h1 - t_c2)
        delta_t_2 = self.delta_t_2 = sci_round(t_h2 - t_c1)
        self.delta_t_m = sci_round(self.get_delta_t_m(delta_t_1, delta_t_2))
        # self.r_solute = sci_round(get_latent_heat_t(solute_r_dict, average_temp))
        # self.r_solvent = sci_round(get_latent_heat_t(solvent_r_dict, average_temp))

    def get_average(self, p: list, x: list):
        assert len(p) == len(x), "The length of p and x must be equal"
        return np.sum([p[i] * x[i] for i in range(len(p))])

    def get_delta_t_m(self, delta_t1, delta_t2):
        return (delta_t2 - delta_t1) / np.log(delta_t2 / delta_t1)

    def get_K(self, alpha_i, alpha_o, d_o, d_i, d_m, A_o, A_i, landa, b, R_si,
              R_so):
        return 1 / (1 / alpha_i * d_o / d_i + R_si * A_o / A_i +
                    b / landa * d_o / d_m + R_so + 1 / alpha_o)

    def choose_from_data(self, A):
        # A = sci_round(A * (1 + self.A_margin))
        for (index, r) in enumerate(self.tubes_ruler):
            if A > r[1]:
                if index == len(self.tubes_ruler) - 1:
                    print("提供的换热管数据中没有满足换热面积的型号")
                    return None
                pass
            else:
                tube = self.heat_tubes[index]
                GN = tube['GN']
                PN = tube['PN'][0]
                N = tube['N']
                n = tube['n']
                c_n = tube['c_n']
                fai_25_2 = tube['fai_25_2']
                fai_25_2dot5 = tube['fai_25_2dot5']
                # print(tube)
                A_list = np.array(tube['A'])
                A_list.sort()
                A_list = list(A_list)
                for (i, a) in enumerate(A_list):
                    if a > A:
                        L_list = np.array(tube['L'])
                        L_list.sort()
                        L_list = list(L_list)
                        L = L_list[i]
                        A_tube = a
                        return {
                            'GN': GN,
                            'PN': PN,
                            'N': N,
                            'n': n,
                            'c_n': c_n,
                            'fai_25_2': fai_25_2,
                            'fai_25_2dot5': fai_25_2dot5,
                            'L': L,
                            'A_tube': A_tube,
                            'A': A
                        }

    def get_alpha_i(self, Re, Pr, landa, d):
        return 0.023 * landa / d * Re**0.8 * Pr**0.4

    def get_alpha_o(self, r, rou, landa, miu, d, delta_t, g=9.81):
        return 0.725 * (r * rou**2 * g * landa**3 / (miu * d * delta_t))**0.25

    @abstractmethod
    def check(self):
        pass

    @abstractmethod
    def get_A(self) -> float:
        pass


class PreHeat(Heat_Exchanger):

    def __init__(
            self,
            t_h1,
            t_h2,
            t_c1,
            t_c2,
            x,
            K,
            m_c,
            name="预热器",
            u=1.5,  # m/s 管内流速
            R_SO=0.000308,  # m^2K/W
            R_Si=0.000172,  # m^2K/W
            pi=np.pi,
            A_margin=0.2,
            k_loss=1.05,
            M_solute=32.04,
            M_solvent=18.02,
            solute_c_p_dict: str | dict = alcohol_c_p,
            solvent_c_p_dict: str | dict = water_c_p,
            cooling_c_p_dict: str | dict = water_c_p,
            solute_r_dict: str | dict = alcohol_latent_heat,
            solvent_r_dict: str | dict = steam_latent_heat,
            steam_r_dict: str | dict = steam_latent_heat,
            heat_tubes: dict = heat_tubes,
            landa_water: dict = landa_water):
        super().__init__(t_h1, t_h2, t_c1, t_c2, x, K, name, u, R_SO, R_Si, pi,
                         A_margin, k_loss, M_solute, M_solvent,
                         solute_c_p_dict, solvent_c_p_dict, cooling_c_p_dict,
                         solute_r_dict, solvent_r_dict, steam_r_dict,
                         heat_tubes, landa_water)
        self.m_c = m_c
        self.c_p_solute = sci_round(get_c_p_by_t(solute_c_p_dict, self.t_avc))
        self.c_p_solvent = sci_round(get_c_p_by_t(solvent_c_p_dict,
                                                  self.t_avc))
        self.c_pc = sci_round(
            self.get_average([self.c_p_solute, self.c_p_solvent], [x, 1 - x]))
        self.Q = sci_round(self.c_pc * m_c * (self.t_c2 - self.t_c1))
        self.r = sci_round(get_latent_heat_t(self.steam_r_dict, self.t_h1))
        self.m_h = sci_round(self.k_loss * self.Q / self.r)
        self.A = sci_round(self.get_A())

    def get_A(self):
        return self.k_loss * self.Q * 1000 / (self.K * self.delta_t_m)


class Cooler(Heat_Exchanger):

    def __init__(
            self,
            t_h1,
            t_h2,
            t_c1,
            t_c2,
            x,
            K,
            m_h,
            name="冷却器",
            u=1.5,  # m/s 管内流速
            R_SO=0.000308,  # m^2K/W
            R_Si=0.000172,  # m^2K/W
            pi=np.pi,
            A_margin=0.2,
            k_loss=1,
            M_solute=32.04,
            M_solvent=18.02,
            solute_c_p_dict: str | dict = alcohol_c_p,
            solvent_c_p_dict: str | dict = water_c_p,
            cooling_c_p_dict: str | dict = water_c_p,
            solute_r_dict: str | dict = alcohol_latent_heat,
            solvent_r_dict: str | dict = steam_latent_heat,
            steam_r_dict: str | dict = steam_latent_heat,
            heat_tubes: dict = heat_tubes,
            landa_water: dict = landa_water):
        super().__init__(t_h1, t_h2, t_c1, t_c2, x, K, name, u, R_SO, R_Si, pi,
                         A_margin, k_loss, M_solute, M_solvent,
                         solute_c_p_dict, solvent_c_p_dict, cooling_c_p_dict,
                         solute_r_dict, solvent_r_dict, steam_r_dict,
                         heat_tubes, landa_water)
        self.m_h = m_h
        self.c_pc = sci_round(get_c_p_by_t(cooling_c_p_dict, self.t_avc))
        self.c_p_solute = sci_round(get_c_p_by_t(solute_c_p_dict, self.t_avh))
        self.c_p_solvent = sci_round(get_c_p_by_t(solvent_c_p_dict,
                                                  self.t_avh))
        self.c_ph = sci_round(
            self.get_average([self.c_p_solute, self.c_p_solvent], [x, 1 - x]))
        self.Q = sci_round(m_h * self.c_ph * (t_h1 - t_h2))
        self.m_c = sci_round(self.Q / (self.c_pc * (t_c2 - t_c1)))
        self.A = sci_round(self.get_A())

    def get_A(self) -> float:
        return self.Q * 1000 / (self.K * self.delta_t_m)


water_miu_t = {
    't': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150],
    'miu': [
        1.7921, 1.3077, 1.0050, 0.8007, 0.656, 0.5494, 0.4688, 0.4061, 0.3565,
        0.3165, 0.2838, 0.2589, 0.2373, 0.2177, 0.2010, 0.1863
    ]
}

alcohol_rou_t = {
    't': [
        -80, -60, -40, -20, 0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200,
        220, 240
    ],
    'rou': [
        899.4, 881.8, 863.6, 844.8, 825.2, 804.8, 783.5, 761.1, 737.4, 712,
        684.7, 654.9, 621.6, 583.4, 537.1, 474.2, 310
    ]
}

alcohol_landa_t = {
    't': [
        0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150,
        160, 170, 180, 190, 200
    ],
    'landa': [
        0.20492, 0.20302, 0.20112, 0.19922, 0.19732, 0.19541, 0.19349, 0.19157,
        0.18963, 0.18768, 0.18572, 0.18377, 0.18182, 0.17989, 0.17799, 0.17613,
        0.17431, 0.17255, 0.17085, 0.16919, 0.16756
    ]
}

alchohol_miu_t = {
    't': [-80, -60, -40, -20, 0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200],
    'miu': [
        5.55, 2.98, 1.78, 1.16, 0.799, 0.580, 0.439, 0.344, 0.277, 0.228,
        0.196, 0.163, 0.107, 0.083, 0.062
    ]
}


class Condenser(Heat_Exchanger):

    def __init__(self,
                 t_h1,
                 t_h2,
                 t_c1,
                 t_c2,
                 x,
                 K,
                 m_h,
                 name="换热器",
                 u=1.5,
                 R_SO=0.000308,
                 R_Si=0.000172,
                 pi=np.pi,
                 A_margin=0.2,
                 k_loss=1,
                 M_solute=32.04,
                 M_solvent=18.02,
                 solute_c_p_dict: str | dict = alcohol_c_p,
                 solvent_c_p_dict: str | dict = water_c_p,
                 cooling_c_p_dict: str | dict = water_c_p,
                 solute_r_dict: str | dict = alcohol_latent_heat,
                 solvent_r_dict: str | dict = steam_latent_heat,
                 steam_r_dict: str | dict = steam_latent_heat,
                 heat_tubes: dict = heat_tubes,
                 landa_water: dict = landa_water,
                 miu_water_dict: dict = water_miu_t,
                 rou_water_dict: dict = water_rou_t,
                 rou_solute_dict: dict = alcohol_rou_t,
                 rou_solvent_dict: dict = water_rou_t,
                 landa_solute_dict: dict = alcohol_landa_t,
                 landa_solvent_dict: dict = landa_water,
                 miu_solute_dict: dict = alchohol_miu_t,
                 miu_solvent_dict: dict = water_miu_t) -> None:
        super().__init__(t_h1, t_h2, t_c1, t_c2, x, K, name, u, R_SO, R_Si, pi,
                         A_margin, k_loss, M_solute, M_solvent,
                         solute_c_p_dict, solvent_c_p_dict, cooling_c_p_dict,
                         solute_r_dict, solvent_r_dict, steam_r_dict,
                         heat_tubes, landa_water)
        self.miu_water_dict = miu_water_dict
        self.rou_water_dict = rou_water_dict
        self.rou_solute_dict = rou_solute_dict
        self.rou_solvent_dict = rou_solvent_dict
        self.landa_solute_dict = landa_solute_dict
        self.landa_water_dict = landa_water
        self.landa_solvent_dict = landa_solvent_dict
        self.miu_solute_dict = miu_solute_dict
        self.miu_solvent_dict = miu_solvent_dict
        self.m_h = m_h
        self.r_solute = sci_round(get_latent_heat_t(solute_r_dict, t_h1))
        self.r_solvent = sci_round(get_latent_heat_t(solvent_r_dict, t_h1))
        self.r = sci_round(
            self.get_average([self.r_solute, self.r_solvent], [x, 1 - x]))
        self.c_pc = sci_round(get_c_p_by_t(cooling_c_p_dict, self.t_avc))
        self.Q = sci_round(m_h * self.r)
        self.m_c = sci_round(self.Q / (self.c_pc * (t_c2 - t_c1)))
        self.A = sci_round(self.get_A())
        self.landa_water = sci_round(
            get_landa_by_t(self.landa_water_dict, self.t_avc))
        self.miu_water = sci_round(get_miu_by_t(miu_water_dict, self.t_avc))
        self.c_pc = sci_round(get_c_p_by_t(cooling_c_p_dict, self.t_avc))
        self.rou_water = sci_round(get_rou_by_t(rou_water_dict, self.t_avc))

    def get_A(self) -> float:
        return self.Q * 1000 / (self.K * self.delta_t_m)

    def check(self, choose, fai='fai_25_2', limit=(0.15, 0.2)):
        u = sci_round(self.m_c / (self.rou_water * choose[fai]))
        d_i = fai.replace('dot', '.').split('_')[1:]
        d_o = float(d_i[0]) / 1000
        b = float(d_i[1]) / 1000
        d_i = sci_round(d_o - 2 * b)
        d_m = np.mean([d_o, d_i])
        Re = sci_round(self.rou_water * u * choose[fai] /
                       (self.miu_water / 1000))
        Pr = sci_round(self.c_pc * self.miu_water / self.landa_water)
        alpha_i = sci_round(self.get_alpha_i(Re, Pr, self.landa_water, d_i))
        r = sci_round(
            self.get_average([self.r_solute, self.r_solvent],
                             [self.x, 1 - self.x]))
        alpha_o = None
        t_wh = int(self.t_h1) - 1
        A_o = sci_round(self.pi * choose['L'] * d_o * choose['n'])

        def check_alpha_o(t_wh):
            t_av = sci_round(np.mean([t_wh, self.t_h1]))
            rou_solute = sci_round(get_rou_by_t(self.rou_solute_dict, t_av))
            rou_solvent = sci_round(get_rou_by_t(self.rou_solvent_dict, t_av))
            rou = sci_round(
                self.get_average([rou_solute, rou_solvent],
                                 [self.x, 1 - self.x]))
            landa_solute = sci_round(
                get_landa_by_t(self.landa_solute_dict, t_av))
            landa_solvent = sci_round(
                get_landa_by_t(self.landa_solvent_dict, t_av))
            landa = sci_round(
                self.get_average([landa_solute, landa_solvent],
                                 [self.x, 1 - self.x]))
            miu_solute = sci_round(
                get_miu_by_t(self.miu_solute_dict, self.t_avc))
            miu_solvent = sci_round(
                get_miu_by_t(self.miu_solvent_dict, self.t_avc))
            miu = sci_round(
                self.get_average([miu_solute, miu_solvent],
                                 [self.x, 1 - self.x]))
            alpha_o = sci_round(
                self.get_alpha_o(r, rou, landa, miu, d_o, self.t_h1 - t_wh))
            if self.t_h1 - self.Q * 1000 / (alpha_o * A_o) - t_wh < 1:
                dis = self.t_h1 - self.Q * 1000 / (alpha_o * A_o) - t_wh
                return alpha_o, t_wh, landa, t_av, rou, miu, landa, dis
            else:
                return None, t_wh, landa

        alpha_o, t_wh, landa, t_av, rou, miu, landa, dis = check_alpha_o(t_wh)
        while True:
            alpha_o, t_wh, landa, t_av, rou, miu, landa, dis = check_alpha_o(
                t_wh + 0.1)
            if alpha_o is None:
                pass
            else:
                break
        A_i = choose['A_tube']
        K = self.get_K(alpha_i, alpha_o, d_o, d_i, d_m, A_o, A_i, landa, b,
                       self.R_Si, self.R_SO)
        A = sci_round(self.Q / (K * self.delta_t_m))
        F = sci_round((A_i - A) / A)
        min_, max_ = limit
        if F < min_:
            return -1
        elif F > max_:
            return {
                'u': u,
                'd_i': d_i,
                'd_o': d_o,
                'd_m': d_m,
                'b': b,
                'Re': Re,
                'Pr': Pr,
                'alpha_i': alpha_i,
                'r': r,
                'alpha_o': alpha_o,
                't_wh': t_wh,
                'A_o': A_o,
                'A_i': A_i,
                'K': K,
                'F': F,
                'A': A,
                'r': r,
                't_av': t_av,
                'rou': rou,
                'miu': miu,
                'landa': landa,
                'dis': dis
            }
        else:
            return {
                'u': u,
                'd_i': d_i,
                'd_o': d_o,
                'd_m': d_m,
                'b': b,
                'Re': Re,
                'Pr': Pr,
                'alpha_i': alpha_i,
                'r': r,
                'alpha_o': alpha_o,
                't_wh': t_wh,
                'A_o': A_o,
                'A_i': A_i,
                'K': K,
                'F': F,
                'A': A,
            }


class reboiler(Heat_Exchanger):

    def __init__(self,
                 t_h1,
                 t_h2,
                 t_c1,
                 t_c2,
                 x,
                 K,
                 m_c,
                 M_v,
                 name="再沸器",
                 u=1.5,
                 R_SO=0.000308,
                 R_Si=0.000172,
                 pi=np.pi,
                 A_margin=0.2,
                 k_loss=1,
                 M_solute=32.04,
                 M_solvent=18.02,
                 solute_c_p_dict: str | dict = alcohol_c_p,
                 solvent_c_p_dict: str | dict = water_c_p,
                 cooling_c_p_dict: str | dict = water_c_p,
                 solute_r_dict: str | dict = alcohol_latent_heat,
                 solvent_r_dict: str | dict = steam_latent_heat,
                 steam_r_dict: str | dict = steam_latent_heat,
                 heat_tubes: dict = heat_tubes,
                 landa_water: dict = landa_water,
                 miu_water_dict: dict = water_miu_t,
                 rou_water_dict: dict = water_rou_t,
                 rou_solute_dict: dict = alcohol_rou_t,
                 rou_solvent_dict: dict = water_rou_t,
                 landa_solute_dict: dict = alcohol_landa_t,
                 landa_solvent_dict: dict = landa_water,
                 miu_solute_dict: dict = alchohol_miu_t,
                 miu_solvent_dict: dict = water_miu_t) -> None:
        super().__init__(t_h1, t_h2, t_c1, t_c2, x, K, name, u, R_SO, R_Si, pi,
                         A_margin, k_loss, M_solute, M_solvent,
                         solute_c_p_dict, solvent_c_p_dict, cooling_c_p_dict,
                         solute_r_dict, solvent_r_dict, steam_r_dict,
                         heat_tubes, landa_water)
        self.miu_water_dict = miu_water_dict
        self.rou_water_dict = rou_water_dict
        self.rou_solute_dict = rou_solute_dict
        self.rou_solvent_dict = rou_solvent_dict
        self.landa_solute_dict = landa_solute_dict
        self.landa_water_dict = landa_water
        self.landa_solvent_dict = landa_solvent_dict
        self.miu_solute_dict = miu_solute_dict
        self.miu_solvent_dict = miu_solvent_dict
        self.m_c = m_c
        self.M_v = M_v
        self.r_solute = sci_round(get_latent_heat_t(solute_r_dict, t_h1))
        self.r_solvent = sci_round(get_latent_heat_t(solvent_r_dict, t_h1))
        self.r_c = sci_round(x * M_solute / M_v * self.r_solute +
                             (1 - x) * M_solvent / M_v * self.r_solvent)
        self.r_h = sci_round(get_latent_heat_t(steam_r_dict, t_h1))
        self.Q = sci_round(m_c * self.r_c)
        self.m_h = sci_round(k_loss * self.Q / self.r_h)
        self.A = sci_round(self.get_A())

    def get_A(self):
        return self.k_loss * self.Q * 1000 / (self.K * self.delta_t_m)


class Pipe:

    def __init__(self, u, x, t=30, pi=np.pi, name='', pipes=pipe):
        self.u = u
        # self.V = V
        self.x = x
        self.pi = pi
        self.name = name
        self.rou_solute = sci_round(get_rou_by_t(alcohol_rou_t, t))
        self.rou_solvent = sci_round(get_rou_by_t(water_rou_t, t))
        self.rou = sci_round(x * self.rou_solute + (1 - x) * self.rou_solvent)
        self.Q = 100 * (x * 32 + (1 - x) * 18) / self.rou / 3600
        self.pipes = pipes
        self.D_i = [[(pipe['D_o'] - 2 * b) / 1000 for b in pipe['b']]
                    for pipe in pipes]
        self.pipe_ruler = [(min(d_i), max(d_i)) for d_i in self.D_i]
        self.d = self.get_d(self.Q, u)
        self.fai = self.choose()

    def choose(self):
        for (index, t) in enumerate(self.pipe_ruler):
            if self.d <= t[1]:
                pipe = self.pipes[index]
                for a in pipe['b']:
                    d_i = (pipe['D_o'] - 2 * a) / 1000
                    if d_i >= self.d:
                        return {
                            'D_o': pipe['D_o'] / 1000,
                            'b': a / 1000,
                        }
            else:
                pass
        print("提供的管道数据中没有满足流速的型号")
        return None

    def get_d(self, V, u):
        return (4 * V / (self.pi * u))


class Pump:

    def __init__(
            self,
            u,
            p_v,
            p_s,
            rou,
            h_f_se,
            z_1,  # 原料液高度
            z_2,  # 进料高度
            delta_h=2.5,
            name="离心泵",
            g=9.81) -> None:
        self.u = u
        self.p_v = p_v
        self.p_s = p_s
        self.rou = rou
        self.h_f_se = h_f_se
        self.name = name
        self.g = g
        self.delta_h = delta_h
        self.z_1 = z_1
        self.z_2 = z_2
        self.z = self.get_z()

    def get_z(self):
        return self.p_s / (self.rou * self.g) + self.p_v / (
            self.rou * self.g) - self.h_f_se - self.delta_h


tower = Tower([], 32, 12, H_bottom=0.7)

floors = tower.get_floors()
print(tower.H, "m")
print(tower.input_H, "m")
print(np.pi)

print()

# for floor in floors:
#     print(floor.index, floor.is_human, floor.H, floor.plates)
