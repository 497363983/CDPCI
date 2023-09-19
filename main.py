import os
from utils import readTextFile
from material import Material
from work import Work
from equations import equations
from utils import table, draw
from tower import Tower, Plate, Cooler, PreHeat, Condenser, reboiler, Pipe, Heat_Exchanger
from calculation import Calculation

capacity = 4.4304
time = 8000
w_F = 0.7
x_o = 0.998
x_w = 0.999
initial_temp = 30
M_solute = 32.04
M_solvent = 18.02
solute = '甲醇'
solvent = '水'
example_R = 1.2
H_T = 0.35
h_L = 0.05
h_n = 0.01
d_o = 0.005
W_s = 0.08
W_c = 0.05
t_div_d_o = 4
delta = 0.003
C_o = 0.79
weir_type = 0
u_multiple = 0.6
p_atm = 101.3
t_cooled = 40
complete_time = "2023 年 8 月 18 日 星期五"

R_example = 1.2
K_heat = 500
K_cool = 500
loss_Q = 1.05
fee_C_F = 2000
fee_steam = 300  # yuan/t
fee_cool_water = 0.6  # yuan/t

H_bottom = 1
H_top = 0.7
H_in = 0.8
H_human = 0.8
H_heat = 3
D_human = 0.5
N_human_dis = 10
human_start = 4
h_in = 0.3

material = Material(capacity, time, w_F, x_o, x_w, initial_temp)
work = Work(material,
            t_cooled,
            delta_t_water=5,
            t_water_initial=30,
            p_atm=p_atm)

exampleR_multiple= 1.8
example_thero = work.get_thero_plates()
example_real = work.get_real_plates(exampleR_multiple)
example_D = work.get_tower_diameter(exampleR_multiple, u_multiple, H_T, h_L)
example_preheat = work.get_preheat(K_heat, loss_Q)
example_cooler = work.get_cooler(exampleR_multiple, K_cool)
example_condenser = work.get_condenser(exampleR_multiple, K_cool)
example_reboiler = work.get_reboiler(exampleR_multiple, loss_Q, K_heat)
example_whole_cost = work.get_whole_cost(exampleR_multiple, u_multiple, H_T, h_L, K_heat,
                                         loss_Q, K_cool, K_cool, K_heat)
cost_R = work.get_cost_R(R_multiple=None,
                         u_multiple=u_multiple,
                         H_T=H_T,
                         h_L=h_L,
                         K_heat=K_heat,
                         loss_Q=loss_Q,
                         K_cool=K_cool,
                         K_condenser=K_cool,
                         K_reboiler=K_heat,
                         R_multiple_min=1.001,
                         R_multiple_max=1.4,
                         num=200)
work.draw_cost_R()
material.draw_T_x_y()
material.draw_y_x()

whole_cost = work.get_whole_cost(cost_R['min'][0]/material.R_min, u_multiple, H_T, h_L, K_heat, loss_Q, K_cool, K_cool, K_heat)
print("whole",whole_cost)
calculation = Calculation(
    work,
    cost_R['min'][0],
    u_multiple=u_multiple,
    H_T=H_T,
    h_L=h_L,
    h_n=h_n,
    d_o=d_o,
    W_s=W_s,
    W_c=W_c,
    t_div_d_o=t_div_d_o,
    delta=delta,
    C_o=C_o,
    weir_type=0  # 0: 平堰, 1: 齿形堰
)

best_thero = work.get_thero_plates(cost_R['min'][0] / material.R_min)
best_real = work.get_real_plates(cost_R['min'][0] / material.R_min)
tower_diameter = calculation.tower_diameter
calculate_example = 29
example_material = calculation.calculate_material_parmaters(calculate_example)
example_plate = calculation.get_n_plate(calculate_example)

for i in [0, best_thero['N_r']-1, best_thero['N_r'], best_thero['number']-1]:
    draw_func = calculation.draw_load_performance(i)
    draw(draw_func, subplots=False)
tower = Tower([
    Plate(example_thero['x'][i], example_thero['y'][i], i,
          calculation.get_n_plate(i)['load_performance'])
    for i in range(len(example_thero['x']))
], best_real['N_real_r'], best_real['N_real_rounded'] - best_real['N_real_r'],
              calculation.H_T, H_bottom, H_top, H_in, H_human, H_heat, D_human,
              N_human_dis, human_start, h_in)

cooler = Cooler(example_real['t_top'], t_cooled, initial_temp,
                initial_temp + work.delta_t_water, x_o, K_cool,
                example_cooler['m_h'])

preheat = PreHeat(example_preheat['T_steam'], example_preheat['T_steam'],
                  initial_temp, material.t_b, w_F, K_heat,
                  example_preheat['m_c'])

Reboiler = reboiler(example_reboiler['T_steam'], example_reboiler['T_steam'],
                    example_reboiler['t_c'], example_reboiler['t_c']-1,
                    best_thero['x'][-1], K_heat, example_reboiler['m_c'],
                    example_reboiler['M_v'])

cooler_choose = cooler.choose_from_data((1 + 0.2) * example_cooler['A'])
preheat_choose = preheat.choose_from_data((1 + 0.2) * example_preheat['A'])
reboiler_choose = Reboiler.choose_from_data((1 + 0.2) * example_reboiler['A'])

condenser = Condenser(best_real['t_top'], best_real['t_top'], initial_temp,
                      initial_temp + 5, best_thero['x'][0], 2000,
                      example_condenser['m_h'], "全凝器", 1.5)
condenser_choose = condenser.choose_from_data(condenser.A * 1.2)

condenser_check = condenser.check(condenser_choose)

input_pipe = Pipe(1, best_thero["x"][best_thero['N_r']])
re_pipe = Pipe(1, best_thero["x"][0], best_real['t_top'])
bottom_pipe = Pipe(1, best_thero["x"][-1], best_real['t_bottom'])
top_pipe = Pipe(20, 0, best_real['t_top'])
b_steam_pipe = Pipe(20, 0, best_real['t_bottom'])


def show_material_parmaters(p):
    return f"""
\\gamma_V={p['gama_v']}kg/m^3，\\gamma_L={p['gama_L']}kg/m^3，L_S={p['L_s']}m^3/s，
V_S={p['V_s']}m^3/s，\\sigma={p['sita']}dyn/cm，\\mu={p['miu']}cP
"""


def show_design_result_table(n):
    plate = calculation.get_n_plate(n)
    project = [
        "塔径$D$", "塔板间距$H_T$", "塔板型式", "空塔速度", "堰长$l_w$", "外堰高$h_w$",
        "板上清液层高度$h_L$", "降液管底与板距离$h_0$", "孔径$d_0$", "孔间距$t$",
        "开孔区边缘与塔壁距离$W_C$", "开孔区边缘与堰距离$W_s$", "孔数$n$", "开孔面积$A_0$", "塔板压降",
        "液体在降液管中的停留时间$\\tau$", "降液管内清夜层高度$H_d$", "雾沫夹带$e_v$"
    ]
    index = range(1, len(project) + 1)
    value = [
        str(calculation.D) + '$m$',
        str(calculation.H_T) + '$m$', "单流型",
        str(calculation.w_G) + "$m/s$",
        str(calculation.l_w) + "$m$",
        str(plate["h_w"]) + "$m$",
        str(plate["weir_and_downcomer"]["h_L"]) + "$m$",
        str(plate["weir_and_downcomer"]["h_o"]) + "$m$",
        str(d_o * 1000) + "$mm$",
        str(plate["hole"]["t"] * 1000) + "$mm$",
        str(W_c) + "$m$",
        str(W_s) + "$m$",
        str(plate["hole"]["n"]) + "个",
        str(plate["hole"]["A_o"]) + "$m^2$",
        str(plate["h_p"]) + "$m液柱$",
        str(plate["t"]) + "$s$",
        str(plate["H_d"]) + "$m液柱$",
        str(plate["e_v"]) + "$kg/kg气$"
    ]
    return table({"序号": index, "项目": project, "值": value}, type="dict")


def show_design_material(n):
    plate_material = calculation.calculate_material_parmaters(n)
    return f"""
$P={p_atm} + h_p\\times {n} \\times 9.807={plate_material['p']}kPa$，
$P_{{solute}}^\\circ=p\\times \\frac{{y}}{{x}}={plate_material['P_solute']}kPa$，
${equations['T_antoine']('顶', work.antoine['solute'][0],work.antoine['solute'][1],work.antoine['solute'][2],plate_material['P_solute'], plate_material['t'])}$，
查得此温度下，$\\rho_{{solute}}={plate_material['rou_solute']}kg/m^3$，$\\rho_{{solvent}}={plate_material['rou_solvent']}kg/m^3$，
$\\mu_{{solute}}={plate_material['miu_solute']}cP$，$\\mu_{{solvent}}={plate_material['miu_solvent']}cP$，
$\\sigma_{{solute}}={plate_material['sita_solute']}dyn/cm$，$\\sigma_{{solvent}}={plate_material['sita_solvent']}dyn/cm$，
$M_V={plate_material['M_v']}kg/kmol$，$M_L={plate_material['M_L']}kg/kmol$，
$\\gamma_V={plate_material['gama_v']}$，$\\gamma_L={plate_material['gama_L']}$,
$\\sigma={plate_material['sita']}dyn/cm$
$\\mu={plate_material['miu']}cP$
$
"""


def showOperationalResiliency():
    name = ["精馏段第一块", "精馏段最后一块", "提馏段第一块", "提馏段最后一块"]
    index = [0, best_thero['N_r'], best_thero['N_r'], best_thero['number'] - 1]
    plate = [calculation.get_n_plate(n) for n in index]
    V = [i['load_performance']["V_max_div_V_min"] for i in plate]
    L = [i['load_performance']["L_max_div_L_min"] for i in plate]
    return table({
        "板": name,
        "$V_{max}/V_{min}$": V,
        "L_{max}/L_{min}": L
    },
                 type="dict")


def human_hole_str():
    res = ""
    for i in tower.floors:
        if i.is_human:
            res += f"{i.plates[0] + 1}-{i.plates[1] + 1}，"
    return res[:-1]


# print(condenser_check)
content = readTextFile("./template.md")
content = "content=f\"\"\"" + content + "\"\"\""
# print(cooler_choose, preheat_choose, reboiler_choose)
exec(content)
print(content)
