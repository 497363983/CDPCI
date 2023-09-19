from material import Material
import pandas as pd
from work import Work
from calculation import Calculation
from utils import table, draw
from tower import Tower, Plate

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
t_cooled = 40
print("-------输入参数--------")
print("原料液处理量=", capacity, "万吨/年")
print("年生产时间=", time, "h/年")
print("原料液中溶质含量=", w_F * 100, "%")
print("馏出液溶质含量=", x_o * 100, "%")
print("溶质回收率=", x_w * 100, "%")
print("原料液初温=", initial_temp, "℃")
print("溶质分子量=", M_solute, "g/mol")
print("溶剂分子量=", M_solvent, "g/mol")
print("溶质=", solute)
print("溶剂=", solvent)
print("----------------------")

test_material = Material(capacity, time, w_F, x_o, x_w, initial_temp)
test_work = Work(test_material, t_cooled, delta_t_water=5, t_water_initial=30)
print('-------物料衡算--------')
print('F=', test_material.F, 'kmol/h')
print('F_kg=', test_material.F_kg, 'kg/h')
print('x_F=', test_material.x_F)
print('x_D=', test_material.x_D)
print('D=', test_material.D, 'kmol/h')
print('W=', test_material.W, 'kmol/h')
print('x_w=', test_material.x_w)
print("-----------------------")

print("-------塔板数确定--------")
# print(pd.DataFrame(test_material.phase_equilibrium))
print('t_b=', test_material.t_b, '℃')
print('t_d=', test_material.t_d, '℃')
print('R_min=', test_material.R_min)
print(f'以{example_R}R_min为例: ')

exam = test_work.get_thero_plates(1.2)
print('R=', example_R * test_material.R_min)
print('精馏段操作线方程：', exam['rec_operating_line'])
print('提馏段操作线方程：', exam['stripping_operating_line'])
print('理论塔板数：', exam['number'])
print('精馏段塔板数N_r：', exam['N_r'])
print('提馏段塔板数N_s：', exam['N_s'])
print('塔板浓度分布：')
print(
    table(
        {
            '塔板数': list(range(1,
                              len(exam['y']) + 1)),
            'x': exam['x'],
            'y': exam['y']
        },
        type='dict'))
real = test_work.get_real_plates(1.2)
print('板效率E_T=', real['E_T'])
print('实际塔板数=', real['N_real'])
print('精馏段塔板数N_r：', real['N_real_r'])
print('---------------------------------')

print('-------塔径估算--------')

tower_diameter = test_work.get_tower_diameter(1.2, u_multiple)
print("D=", tower_diameter['D_rounded'], 'm')
print("---------------------")

print("-------换热器计算--------")
print("1. 预热器")
preheat = test_work.get_preheat()
print("A=", preheat['A'], 'm^2')
print("2. 冷却器")
# cooler = test_work.get_cooler()

print("------------------------")


cost_R = test_work.get_cost_R(K_heat=500,
                              loss_Q=1.05,
                              K_cool=350,
                              K_condenser=350,
                              K_reboiler=500,
                              num=150,
                              R_multiple_max=1.5,
                              u_multiple=u_multiple,
                              H_T=H_T,
                              h_L=h_L,)
best_R = cost_R['min'][0]


print("best R=", cost_R['min'][0])
print('---------------------------------')
test_calculation = Calculation(test_work, best_R, u_multiple=u_multiple, H_T=H_T, h_L=h_L, h_n=h_n, d_o=d_o, W_s=W_s, W_c=W_c, delta=delta, weir_type=weir_type)
print('----塔板和塔体主要工艺尺寸的设计计算--------')
print('优化后塔径求取：')
print('塔径D=', test_calculation.D, 'm')
print('N_r=', test_calculation.thero_plates['N_r'])
print('N_s=', test_calculation.thero_plates['N_s'])
print('塔板的主要工艺尺寸计算：')
print('1. 精馏段第一块板：')
plate_0 = test_calculation.get_n_plate(0)
material_0 = test_calculation.calculate_material_parmaters(0)
print('（1）已知条件：')
print('L_s=', test_calculation.L_s, 'm^3/s')
print('V_s=', test_calculation.V_s, 'm^3/s')
print('sita=', material_0['sita'], 'dyn/cm')
print('gama_v=', material_0['gama_v'], 'kg/m^3')
print('gama_L=', material_0['gama_L'], 'kg/m^3')
print('miu=', material_0['miu'], 'cP')
print('miu_solute=', material_0['miu_solute'], 'cP')
print('miu_solvent=', material_0['miu_solvent'], 'cP')
print('（2）塔径初步核算：')
print('a. 雾沫夹带')
print('l_w=', test_calculation.l_w)
print('A_T=', test_calculation.A_T)
print('A_f=', test_calculation.A_f)
print('w_G=', test_calculation.w_G)
print('e_v=', test_calculation.e_v, 'kg/kg气')
print('停留时间 t=', test_calculation.t, 's')
print('（3）塔板结构形式的选取：')
print('单流型')
print('（4）堰及降液管设计：')
print('a. 堰的确定：', 'l_w=', test_calculation.l_w, 'm')
print('b. 堰上清液层how 的计算：')
if weir_type == 1:
    print('采用齿形堰，h_n=', h_n, 'm')
elif weir_type == 0:
    print('采用平堰')
print('h_ow=', plate_0['weir_and_downcomer']['h_ow'], 'm')
print('c. 液面梯度：')
print('b=', plate_0['weir_and_downcomer']['b'])
print('Z_1=', plate_0['weir_and_downcomer']['Z_1'], 'm')
print('Delta=', plate_0['weir_and_downcomer']['Delta'], 'm')
print('d. 板上清液层h_L的计算：')
print('h_w=', plate_0['weir_and_downcomer']['h_w_rounded'], 'm')
print('h_L=', plate_0['weir_and_downcomer']['h_L'], 'm')
print('e. 降液管底部距下一板的间距h_o')
print('h_o=', plate_0['weir_and_downcomer']['h_o_rounded'], 'm')
print('（5）孔布置')
print(
    f"a. 筛孔选择d_o={d_o * 1000}mm, t/d_o={t_div_d_o}， 则t={d_o * 1000 * t_div_d_o}mm, A_o/A_a={plate_0['hole']['A_o_div_A_a']}"
)
print(f"b. 边缘区确定取W_s={W_s * 1000}mm，W_c={W_c * 1000}mm")
print("x=", plate_0['hole']['x'])
print("r=", plate_0['hole']['r'])
print("A_a=", plate_0['hole']['A_a'])
print("A_o=", plate_0['hole']['A_o'])
print("c. 孔数n")
print("n=", plate_0['hole']['n'])
print("（6）干板压降")
print("板厚delta=", delta, 'm')
print("d_o/delta=", d_o / delta)
print("C_o=", C_o)
print("w_o=", plate_0['w_o'], 'm/s')
print("h_c=", plate_0['h_c'], 'm液柱')
print("（7）稳定性")
print("h_sita=", plate_0['h_sita'])
print("w_oM=", plate_0['w_om'], 'm/s')
print("K=", plate_0['K'])
print("（8）塔板压降h_p")
print("h_l=", plate_0['h_l'], 'm液柱')
print("h_p=", plate_0['h_p'], 'm液柱')
print("（9）液泛情况")
print("h_d=", plate_0['h_d'], 'm液柱')
print("H_d=", plate_0['H_d'], 'm液柱')
judge = test_calculation.H_T + plate_0['h_w']
H_d2 = plate_0['H_d'] * 2
print(f"2H_d={H_d2}m液柱 {'<' if H_d2 < judge else '>'} (H_T + h_w)={judge}m液柱，故{'不' if H_d2 < judge else ''}会产生液泛现象")
print(f"w_f={plate_0['w_f']}m/s {'<' if plate_0['w_f'] < 0.1 else '>'} 0.1m/s")
print(f"t={plate_0['t']}s {'<' if plate_0['t'] < 5 else '>'} 5s")
print("（10）雾沫夹带")
print(f"e_v={plate_0['e_v']}kg/kg气 {'<' if plate_0['e_v'] < 0.1 else '>'} 0.1kg/kg气")
print("V_max/V_min=", plate_0['load_performance']['V_max_div_V_min'])
print('--------------------------------')
# for i in range(test_calculation.thero_plates['number']):
#     draw_func = test_calculation.draw_load_perdormance(i)
#     draw(draw_func, subplots=False)

print("-------辅助设备的设计--------")
print("一、塔高的设计")
x = test_calculation.thero_plates['x']
y = test_calculation.thero_plates['y']
plates = [Plate(x[i], y[i], i, None) for i in range(test_calculation.thero_plates['number'])]
N_real = test_calculation.real_plates['N_real']
N_r = test_calculation.real_plates['N_real_r']
N_s = test_calculation.real_plates['N_real'] - test_calculation.real_plates['N_real_r']
H_T = test_calculation.H_T
H_bottom = 1
H_top = 0.7
H_in = 0.8
H_human = 0.8
H_heat = 3
D_human = 0.5
N_human_dis = 10
human_start = 4
h_in = 0.3
tower = Tower(plates, N_r, N_s, H_T, H_bottom, H_top, H_in, H_human, H_heat, D_human, N_human_dis, human_start, h_in)
print("理论塔板数为", test_calculation.thero_plates['number'])
print("实际塔板数为", N_real)
print("精馏段实际塔板数为", N_r)
print("提馏段实际塔板数为", N_s)
print("加料板在第", N_r + 1, "块板")

print("板间距H_T=", H_T, "m")
print("进料处板间距", H_in, "m")
print("开人孔处间距", H_human, "m")
print("第一快板到塔顶距离", H_top, "m")
print("最后一块板到塔底的距离", H_bottom, "m")
print("间接蒸汽加热裙座", H_heat, "m")
print("人孔直径", D_human, "m")
print("塔高H=", tower.H, "m")
print("二、换热器的设计")
print("1. 预热器")
preheat = test_calculation.work.get_preheat()
print("A=", preheat["A"], "m^2")
print("2. 冷却器")
cooler = test_calculation.work.get_cooler(test_calculation.R_multiple)
print("A=", cooler["A"], "m^2")
print("3. 全凝器")
condenser = test_calculation.work.get_condenser(test_calculation.R_multiple, 500)
print("A=", condenser["A"], "m^2")
print("----------------------")

# test_material.draw_T_x_y()
# test_material.draw_y_x()
# test_work.draw_thero_plates(1.2)
# test_work.draw_operating_line(1.2)
# test_work.draw_thero_plates(1.2)

# test_work.draw_cost_R(K_heat=500,
#                       loss_Q=1.05,
#                       K_cool=350,
#                       K_condenser=350,
#                       K_reboiler=500,
#                       num=150,
#                       R_multiple_max=1.5)

tower_diameter = test_work.get_tower_diameter(best_R / test_material.R_min,
                                              0.8)

D_best = tower_diameter['D']
D_best_rounded = tower_diameter['D_rounded']
best_thero_plates = test_work.get_thero_plates(best_R / test_material.R_min)
best_x_y = {'x': best_thero_plates['x'], 'y': best_thero_plates['y']}
best_real_plates = test_work.get_real_plates(best_R / test_material.R_min)

print(pd.DataFrame.from_dict(best_x_y))
