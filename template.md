# 课程设计任务书

## 一、设计题目

甲醇-水混合液连续精馏装置的设计

## 设计原始条件

1. 操作条件：

   精馏塔操作压力：<u>常压</u>

   蒸汽压力（绝压）：<u>{work.p_steam}</u>kgf/cm^2^

   每年生产时间：<u>{time}</u>小时

   冷却水温度：<u>30</u>℃

   冷却水温升：<u>5</u>℃

   产品冷却后温度：<u>40</u>℃

2. 设计数据：

   原料液：<u>甲醇水双组分混合液</u>

   原料液处理量：<u>{material.handling_capacity}</u>万吨/年

   原料液初温：<u>{material.initial_temp}</u>℃

   原料液含甲醇：<u>{material.w_F}</u>% (质量)

   馏出液含甲醇：<u>{material.x_o}</u>% (质量)

   甲醇回收率: <u>{material.eta}</u>% (质量)

## 三、设计任务

    完成精馏工艺设计，运用最优化方法确定最佳操作参数；选用板式塔进行精馏塔设备工艺设计和有关附属设备设计和选用；编写设计说明书和设计计算书；绘制工艺流程图、塔板结构简图、塔板负荷性能图和其他附图。

## 四、设计完成日期

    {complete_time}

## 五、设计者

## 六、指导老师

## 一、工艺流程的选定

1. 根据生产规模和产品质量要求，选用板式塔连续精馏，操作稳定，可用
于工业的大规模生产。

2. 塔板选用筛板塔。按一定尺寸和一定排列方式开圆形筛孔，作为气相通道，气相穿过筛孔进入塔板上液相，进行接触传质，其结构简单，造价低廉，操作稳定，塔板阻力小，板效率高，但也有缺点，小孔易堵塞。

3. 工艺采用自选泵进料。利用泵将原料打入预热器预热，再从预热器进入
精馏塔。

4. 在塔顶安装全凝器，产品经全凝器后为液体，再冷却方便快速。

5. 精馏液体经过全凝器后温度较高，为减少馏出组分的挥发，在全凝器后安装冷却器，降低液体温度。

6. 塔底采用间接水蒸汽。本工艺是分离甲醇-水二元混合物，混合液中含水，可以采用直接蒸汽加热。直接加热的热利用率高，同时不会存在因换热器换热管结垢而出现传热效果不好的情况。但水汽除了作为夹带剂外还作为加热剂，因此水蒸气消耗量较大，而且能耗高，设备负荷大，传质效率降低，故工艺采用间接蒸汽加热，安装再沸器，分离效率高。

7. 泡点进料，可以使精馏段和提馏段的气液负荷（液气比）一致，从而可以采用等径塔，便于加工设计，且可以节能。

8. 塔顶泡点常压出料。

9. 安装转子流量计与阀门，对进料与回流液进行计量，以便合理控制。

## 二、工艺计算

### 1、物料衡算

#### 进料状态

$$
{equations['F'](capacity * 10000, time, material.F_kg, w_F, M_solute, M_solvent, material.F)}
$$

$$
{equations['x_F'](w_F, M_solute, M_solvent, material.x_F)}
$$

#### 塔顶馏出液

$${equations['x_D'](x_o, M_solute, M_solvent, material.x_D)}$$

$${equations['D'](x_w, material.F, material.x_F, material.x_D, material.D)}$$

#### 塔釜馏出液

$${equations['W'](material.F, material.D, material.W)}$$

$$ {equations['x_w'](material.F, material.x_F, material.D, material.x_D, material.W, material.x_w)}$$

### 2、塔板数的确定

#### 理论塔板数的求取

1、求最小回流比

a. 相平衡线的求取
  绘出x-y图

b. q 的求取
  进料处压力为101.3kPa，摩尔组成为$x_F={material.x_F}$,读图得泡点温度为{material.t_b}℃，露点温度为{material.t_d}℃。设进料温度为{material.t_b}℃，q=1，则q线方程为：$x=x_F={material.x_F}$

c. R~min~的求取
精馏段操作线经过点（x~D~，x~D~）以及q 线与平衡线交点即（{material.x_D}, {material.x_D}），
（{material.x_w}, {material.R_min/(1+material.R_min)*material.x_w+material.y_e}），因此得精馏段操作线方程为：y={material.R_min/(1+material.R_min)}x + {material.y_e}。即可求得Rmin={material.R_min}。

2、当R={exampleR_multiple}R~min~时，理论塔板数的计算

当R={exampleR_multiple}R~min~={example_thero['R']}时，精馏段操作线方程为：
$${example_thero['rec_operating_line']}$$
提馏段操作线方程为：
$${example_thero['stripping_operating_line']}$$

{table({'x': example_thero['x'], 'y': example_thero['y']}, type='dict')}

3、板效率E~T~的求取

${equations['P_solute'](solute, work.p_atm, material.x_D, example_thero['x'][0], work.get_p_top_solute(1.2))}$，把$P_{{solute}}^\\circ$ 代入
Antonine 公式，可得塔顶温度T 顶，根据塔顶温度可求得塔顶P 水，因此可得塔
顶α 顶，即：
$${equations['T_antoine']('顶', work.antoine['solute'][0], work.antoine['solute'][1], work.antoine['solute'][2], work.get_p_top_solute(1.2), work.get_t_top(work.get_p_top_solute(1.2)))}$$

$${equations['P_antoine']('水', work.antoine['solvent'][0], work.antoine['solvent'][1], work.get_t_top(work.get_p_top_solute(exampleR_multiple)), work.antoine['solvent'][2], work.get_p_top_solvent(work.get_t_top(work.get_p_top_solute(exampleR_multiple))))}$$
$${equations['alpha']('顶', solute, solvent, work.get_p_top_solute(exampleR_multiple), work.get_p_top_solvent(work.get_t_top(work.get_p_top_solute(exampleR_multiple))), work.get_alpha(work.get_p_top_solute(exampleR_multiple), work.get_p_top_solvent(work.get_t_top(work.get_p_top_solute(exampleR_multiple)))))}$$
同理，塔釜$P_水^\\circ={example_real['p_bottom_solvent']}kPa$，$T_釜={example_real['t_bottom']}℃$，$P^\\circ_{solute}={example_real['p_bottom_solute']}$，$\\alpha_釜={example_real['alpha_bottom']}$。则全塔的相对挥发度为：
$${equations['alpha_average'](example_real['alpha_top'], example_real['alpha_bottom'], example_real['alpha_relate'])}$$
  进料温度为{material.t_b}时，{solvent}的黏度为{example_real['miu_solvent']}，{solute}的黏度为{example_real['miu_solute']}，则进料液的平均摩尔黏度为：

$${equations['miu_relate'](material.x_F, example_real['miu_solute'], example_real['miu_solvent'], example_real['miu_relate'])}$$

由于所用为筛板塔，故f={work.f}，由0’ connell 塔效经验式可知：
$${equations['E_T'](work.f, example_real['alpha_relate'], example_real['miu_relate'], example_real['E_T'])}$$
故实际塔板数为${equations['N_T'](example_thero['number'], example_real['E_T'], example_real['N_real'])}$，圆整为{example_real['N_real_rounded']}块。其中，精馏段理论塔板数为{example_real['N_real_r']}块，加料板在第{example_real['N_real_r'] + 1}块。

### 3、塔径估算

以塔顶第一块板为计算对象，塔顶压力可认为是一个大气压，y1={example_thero['y'][0]}，塔顶温度为（{example_real['t_top']}+273.15）={example_real['t_top']+273.15}K:

$${equations['M']('V', example_thero['y'][0], M_solute, M_solvent, example_D['M_v'])}$$

$${equations['gama']('V', p_atm, example_D['M_v'], example_real['t_top']+273.15, example_D['gama_v'])}$$

查得t={example_real['t_top']}℃时，$\\rho_{{solute}}={example_D['rou_solute']}kg/m^3$，$\\rho_{{solvent}}={example_D['rou_solvent']}kg/m^3$

$${equations['gama_rou']('L', x_o,example_D['rou_solute'], example_D['rou_solvent'], example_D['gama_L'])}$$

$${equations['V'](1.2*material.R_min, material.D, example_D['V'])}$$

$${equations['V_s'](example_D['V'], example_D['M_v'], example_D['gama_v'], example_D['V_s'])}$$

$${equations['M']('L', example_thero['x'][0], M_solute, M_solvent, example_D['M_L'])}$$

$${equations['L'](example_D['V'], material.D, example_D['L'])}$$

$${equations['L_S'](example_D['L'], example_D['M_L'], example_D['gama_L'], example_D['L_s'])}$$

$${equations['L_V'](example_D['L_s'], example_D['V_s'], example_D['gama_L'], example_D['gama_v'], example_D['L_v'])}$$

设板间距为H~T~={H_T}m，液层高度为h~L~={h_L}m，H=H~T~-h~L~={H_T - h_L}m，计算得C~20~={example_D['C_20']}。查得t={example_real['t_top']}℃时，$\\sigma_{{solute}}={example_D['sita_solute']}dyn/cm$，$\\sigma{{solvent}}={example_D['sita_solvent']}dyn/cm$，则平均表面张力为$\\sigma=\\sum x_i\\sigma_i={example_D['sita']}$。

$${equations['C_sita'](example_D['C_20'], example_D['sita'], example_D['C_sita'])}$$

$${equations['w_G'](example_D['C_sita'], example_D['gama_L'], example_D['gama_v'], example_D['u_max'])}$$

一般取$w=（0.6~0.8）w_{{G(max)}}$，则$w={u_multiple}wG(max)={example_D['u']}m/s$，

${equations['D_'](example_D['V_s'], example_D['u'], example_D['D'])}$，圆整后$D={example_D['D_rounded']}$。

则塔体费用$C_D=13290D^{{1.2}}N=13290\\times {example_D['D_rounded']}^{{1.2}}\\times {example_real['N_real_rounded']}={example_D['C_D']}元$

### 4、换热器计算

加热器选取总传热系数$K={K_heat}W/(m^2\\cdot ℃)$，冷却器选取$K={K_cool}W/(m^2\\cdot ℃)$

（1）预热器
利用水蒸气潜热加热原料到${material.t_b}℃$，水蒸气发生相变，温度不变，水蒸气绝压为${work.p_steam}kgf/cm^2$，即$490.35kPa$，由安托因公式，可求得此时水蒸气温度为${example_preheat['T_steam']}℃$，$m_c=\\frac{{F}}{{3600}}={example_preheat['m_c']}kg/s$；
原料液温度为${initial_temp}℃$，平均温度为${example_preheat['T_aveage']}℃$，此温度下查得$c_{{p{solute}}}={example_preheat['c_p_solute']}kJ/(kg\\cdot ℃)$, $c_{{p{solvent}}}={example_preheat['c_p_solvent']}kJ/(kg\\cdot ℃)$，则平均比热容$c_{{pc}}={example_preheat['c_p']}kJ/(kg\\cdot ℃)$，$t_{{c1}}={initial_temp}℃$，$t_{{c2}}={material.t_b}℃$，$\\Delta t_1=t_{{h1}} - t_{{c2}}={example_preheat['T_steam']}-{material.t_b}={example_preheat['delta_t_1']}$，$\\Delta t_2=t_{{h2}} - t_{{c1}}={example_preheat['T_steam']}-{initial_temp}={example_preheat['delta_t_2']}$，则${equations['delta_t_m'](example_preheat['delta_t_1'], example_preheat['delta_t_2'], example_preheat['delta_t_m'])}$，${equations['Q'](example_preheat['m_c'], example_preheat['c_p'], initial_temp, material.t_b, example_preheat['Q'])}$，故${equations['A'](example_preheat['Q'], K_heat, example_preheat['delta_t_m'], example_preheat['A'], loss_Q)}$

${example_preheat['T_steam']}℃$下水蒸气汽化潜热$r={example_preheat['r']}kJ/kg$，故水蒸气用量$m_h=\\frac{{1.05Q}}{{r}}={example_preheat['m_h']}kg/s$。

（2）冷却器

利用${initial_temp}℃（t_{{c1}}）$冷却水冷却塔顶产品到${t_cooled}℃$，冷却水温升为${work.delta_t_water}℃$，则冷却水出口温度为${initial_temp + work.delta_t_water}（t_{{c2}}）℃$，平均温度为${example_cooler['t_water_avarage']}℃$，查得此温度下$c_{{pc}}={example_cooler['c_p_water']}kJ/(kg\\cdot ℃)$。产品进口温度为${example_real['t_top']}℃（t_{{h1}}）$，出口温度${t_cooled}℃（t_{{h2}}）$，平均温度为${example_cooler['t_p']}℃$，此温度下查得$c_{{psolute}}={example_cooler['c_p_solute']}kJ/(kg\\cdot ℃)$，$c_{{psolvent}}={example_cooler['c_p_solvent']}kJ/(kg\\cdot ℃)$，平均比热容$c_{{ph}}={example_cooler['c_p_h']}kJ/(kg\\cdot ℃)$。$\\Delta t_1={example_cooler['delta_t_1']}℃$，$\\Delta t_2={example_cooler['delta_t_2']}℃$，则$\\Delta t_m={example_cooler['delta_t_m']}℃$。$m_h={example_cooler['m_h']}kg/s$，因此${equations['Q'](example_cooler['m_h'], example_cooler['c_p_h'], example_cooler['delta_t_1'], example_cooler['delta_t_2'], example_cooler['Q'])}$，${equations['A'](example_cooler['Q'], K_cool, example_cooler['delta_t_m'], example_cooler['A'], 1)}$。冷却水用量为${equations['m']('c', example_cooler['Q'], example_cooler['c_p_water'], initial_temp, example_cooler['t_water_cooled'], example_cooler['m_c'])}$。

（3）全凝器

利用冷却水冷却塔顶馏出液，产品发生相变，温度不变，$t_{{h1}}=t_{{h2}}={example_real['t_top']}℃$
压力为${work.p_atm}kPa$，$m_h=V\\cdot M_V={example_condenser['m_h']}kg/s$此温度下查得汽化潜热$r_{{solute}}={example_condenser['r_solute']}kJ/kg$，$r_{{solvent}}={example_condenser['r_solvent']}kJ/kg$，平均气话潜热$r={example_condenser['r']}kJ/kg$。

冷却水进口温度为 ${initial_temp}℃$，出口为${example_condenser['t_water_cooled']}℃$，$\\Delta t_1={example_condenser['delta_t_1']}℃$，$\\Delta t_2={example_condenser['delta_t_2']}℃$，，$\\Delta t_m={example_condenser['delta_t_m']}℃$。平均温度为${example_condenser['t_water_average']}℃$，此温度下$c_{{pc}}={example_condenser['c_p_c']}kJ/(kg\\cdot ℃)$。故$Q=m_h\\cdot r={example_condenser['Q']}kW$，冷却水用量${equations['m']('c', example_condenser['Q'], example_condenser['c_p_c'], initial_temp, example_condenser['t_water_cooled'], example_condenser['m_c'])}$。${equations['A'](example_condenser['Q'], K_cool, example_condenser['delta_t_m'], example_condenser['A'], 1)}$。

（5）再沸器

利用水蒸气潜热加热塔釜产品，冷热物流均发生相变，温度不变，水蒸气绝压为$5kgf/cm^2$，即$490.35kPa$，由安托因公式，可求得此时水蒸气温度为${example_reboiler['T_steam']}℃$。$t_{{h1}}=t_{{h2}}={example_reboiler['T_steam']}℃$，$t_{{c1}}=t_{{c2}}={example_reboiler['t_c']}℃$，$V^{{\\prime}}=V-(1-q)F={example_reboiler['V']}kmol/h$，$M_V={example_reboiler['M_v']}$，则$m_c=V^{{\\prime}}\\cdot M_V={example_reboiler['m_c']}kg/s$。，产品进出温度为${example_reboiler['t_c']}℃$，此温度下查得$r_{{solute}}={example_reboiler['r_solute']}kJ/kg$，$r_{{solvent}}={example_reboiler['r_solvent']}kJ/kg$，则$r_c={example_reboiler['r_c']}kJ/kg$。${example_reboiler['T_steam']}℃$下水的汽化潜热$r_h={example_reboiler['r_water']}kJ/kg$。故$Q=m_cr_c={example_reboiler['Q']}kW$，水蒸气用量为$m_h=\\frac{{1.05Q}}{{r_h}}={example_reboiler['m_h']}kg/s$。$\\Delta t_m = t_h - t_c = {example_reboiler['delta_t_m']}℃$，${equations['A'](example_reboiler['Q'], K_heat, example_reboiler['delta_t_m'], example_reboiler['A'], loss_Q)}$

### 5、总费用计算

（1）换热器费用：$C_F={fee_C_F}A={fee_C_F}\\times ({example_preheat['A']} + {example_cooler['A']} + {example_condenser['A']} + {example_reboiler['A']}) = {example_whole_cost['C_F']}元$

（2）蒸汽费用：$C_S={fee_steam}W_{{steam}}={fee_steam}\\times ({example_preheat['m_h']} + {example_reboiler['m_h']})/1000 \\times 3600 \\times {time}={example_whole_cost['C_S']}元$

（3）冷却水费用：$C_W={fee_cool_water}W_{{water}}={fee_cool_water}\\times ({example_cooler['m_c']} + {example_condenser['m_c']})/1000 \\times 3600 \\times {time}={example_whole_cost['C_S']}元$

（4）塔体费用：$C_D={example_D['C_D']}元$

年总费用：$C=0.33(C_D+C_F)+(C_S+C_W)={example_whole_cost['C']}万元$

{table({'R': cost_R['R'], '总费用C': cost_R['cost']}, type='dict', column_num=4)}

## 三、塔板和塔体主要工艺尺寸的设计计算

### 1、优化后塔径求取

由回流比-总费用关系图可知：当R={cost_R['min'][0]}时，总费用处于最低范围内，可认为是最佳回流比。

$${equations['L_'](cost_R['min'][0], material.D, tower_diameter['L'])}$$

$${equations['V'](cost_R['min'][0], material.D, tower_diameter['V'])}$$

$${equations['V_'](tower_diameter['V'], material.F, 1, tower_diameter['V'])}$$

$${equations['L__'](tower_diameter['L'], 1, material.F, tower_diameter['L']+material.F)}$$

$${equations['V_s'](tower_diameter['V'], tower_diameter['M_v'], tower_diameter['gama_v'], tower_diameter['V_s'])}$$

$${equations['L_S'](tower_diameter['L'], tower_diameter['M_L'], tower_diameter['gama_L'], tower_diameter['L_s'])}$$

$${equations['L_V'](tower_diameter['L_s'], tower_diameter['V_s'], tower_diameter['gama_L'], tower_diameter['gama_v'], tower_diameter['L_v'])}$$

取板间距为$H_T={H_T}m$，液层高度为$h_L={0.05}m$，$H=H_T-h_L={H_T - h_L}m$，计算得$C_{{20}}={tower_diameter['C_20']}$，查得$t={best_real['t_top']}℃$时，$\\sigma_{{solute}}={tower_diameter['sita_solute']}dyn/cm$，$\\sigma_{{solvent}}={tower_diameter['sita_solvent']}dyn/cm$，则平均表面张力$\\sigma={tower_diameter['sita']}dyn/cm$，${equations['C_sita'](tower_diameter['C_20'], tower_diameter['sita'], tower_diameter['C_sita'])}$，${equations['w_G'](tower_diameter['C_sita'], tower_diameter['gama_L'], tower_diameter['gama_v'], tower_diameter['u_max'])}$，一般取$w=（0.6-0.8）wG(max)$，则$w={u_multiple}wG(max)={tower_diameter['u']}m/s$，${equations['D_'](tower_diameter['V_s'], tower_diameter['u'], tower_diameter['D'])}$，圆整后$D={tower_diameter['D_rounded']}m$。

### 2、塔板的主要工艺尺寸计算

由逐板计算得每块塔板组成如下：

{table({'板编号': range(1, len(best_thero['x'])+1),'x': best_thero['x'], 'y': best_thero['y']}, type='dict')}

1、精馏段第一块板：

（1）已知条件：

{show_material_parmaters(example_material)}

（2）塔径初步核算：
a. 雾沫夹带
取$l_w={calculation.l_w}m$，$A_T={calculation.A_T}m^2$，$A_f={calculation.A_f}m^2$，${equations['w_G_'](example_material['V_s'], calculation.A_T, calculation.A_f, calculation.w_G)}$，$h_f=2.5h_L$，${equations['e_v'](example_material['sita'], calculation.w_G, calculation.H_T, 2.5 * h_L, calculation.e_v)}<0.1kg/kg气$

b. 停留时间

${equations['t'](calculation.A_f, calculation.H_T, example_material['L_s'], calculation.t)}>5s$

自以上两项初步认为塔径应取${calculation.D}m$。

（3）塔板结构形式选取

采用单流型。

（4）堰及降液管设计

a. 堰的确定：取$l_w={calculation.l_w}m$

b. 堰上清液层how 的计算：

选取平堰，取E=1：

$${equations['h_ow'](example_material['L_s'], calculation.l_w, example_plate['weir_and_downcomer']['h_ow'], 1)}$$

c. 液面梯度

${equations['b'](calculation.l_w, calculation.D, example_plate['weir_and_downcomer']['b'])}$，$W_d={calculation.W_d}m$，${equations['Z_1'](calculation.D, calculation.W_d, example_plate['weir_and_downcomer']['Z_1'])}$，${equations['Delta'](example_plate['weir_and_downcomer']['b'], calculation.h_f, example_material['miu'], example_material['L_s'], example_plate['weir_and_downcomer']['Z_1'], example_material['gama_L'], example_plate['weir_and_downcomer']['Delta'])}$

d. 板上清液层高度$h_L$的计算

设$h_L^\\prime={h_L}m$，$h_w=h_L^\\prime - h_{{ow}}={example_plate['weir_and_downcomer']['h_w']}$，取$h_w$为${example_plate['weir_and_downcomer']['h_w_rounded']*1000}mm$，则$h_L=h_w+h_{{ow}}={example_plate['weir_and_downcomer']['h_L']}m$

e. 降液管底部距下一板的间距$h_0$

${equations['h_0'](example_plate['weir_and_downcomer']['h_w'], example_plate['weir_and_downcomer']['h_o'])}$，圆整为${example_plate['weir_and_downcomer']['h_o_rounded']}m$。

（5）孔布置

a. 筛孔选择取$d_0={d_o *1000}mm$，$\\frac{{t}}{{d_0}}={t_div_d_o}$则$t={d_o* 1000 * t_div_d_o}mm$，$\\frac{{A_0}}{{A_a}}=\\frac{{0.907}}{{\\left(\\frac{{t}}{{d_0}}\\right)^2}}={example_plate['hole']['A_o_div_A_a']}$

b. 边缘区确定取$W_s={W_s}m$，$W_c={W_c}m$，${equations['x'](calculation.D, calculation.W_d, calculation.W_s, example_plate['hole']['x'])}$，${equations['r'](calculation.D, calculation.W_c, example_plate['hole']['r'])}$，$\\frac{{x}}{{r}}={example_plate['hole']['x']/example_plate['hole']['r']}$，计算得${equations['A_a'](example_plate['hole']['x'], example_plate['hole']['r'], example_plate['hole']['A_a'])}$，则$A_0={example_plate['hole']['A_o']}m^2$。

c. 孔数n

${equations['n'](example_plate['hole']['t'], example_plate['hole']['A_a'], example_plate['hole']['n'])}$

（6）干板压降

取板厚$\\delta={delta * 1000}mm$，$d_0/\\delta={d_o/delta}$查图得$C_0={C_o}$，${equations['w_0'](example_material['V_s'],example_plate['hole']['A_o'], example_plate['w_o'])}$

（7）稳定性

${equations['h_sita'](example_material['sita'], example_material['gama_L'], d_o, example_plate['h_sita'])}$，${equations['w_0m'](C_o, example_plate['weir_and_downcomer']['h_L'], example_plate['h_sita'], example_material['gama_L'], example_material['gama_v'], example_plate['w_om'])}$，$K=\\frac{{w_0}}{{w_{{0m}}}}={example_plate['K']}$

（8）塔板压降$h_p$

${equations['F_o'](example_plate['w_o'], example_material['gama_v'], example_plate['F_o'])}$，读图得$h_l={example_plate['h_l']}m液柱$，$h_p=h_c+h_l={example_plate['h_p']}m液柱$。

（9）液泛情况

${equations['h_d'](example_material['L_s'], calculation.l_w, example_plate['weir_and_downcomer']['h_o_rounded'], example_plate['h_d'])}$，${equations['H_d'](example_plate['H_d'])}$，$2H_d={example_plate['H_d'] *2}m液柱 {'<' if example_plate['H_d']* 2 < calculation.H_T + example_plate['h_w'] else '>'} (H_T + h_w)={calculation.H_T + example_plate['h_w']}m液柱$，故{'不' if example_plate['H_d'] * 2 < calculation.H_T + example_plate['h_w'] else ''}会产生液泛现象。

${equations['w_f'](example_material['L_s'], calculation.A_f, example_plate['w_f'])}<0.1m/s$，${equations['t'](calculation.A_f, calculation.H_T, example_material['L_s'], example_plate['t'])}>5s$

（10）雾沫夹带
${equations['e_v'](example_material['sita'], calculation.w_G, calculation.H_T, 2.5 * example_plate['weir_and_downcomer']['h_L'], example_plate['e_v'])}<0.1kg/kg气$

{show_design_result_table(0)}

2、提馏段第一块板，即第{best_thero['N_r']+1}块板

{show_design_material(best_thero['N_r'])}

{show_design_result_table(best_thero['N_r'])}

3、精馏段最后一块板，即第{best_thero['N_r']}块板

{show_design_material(best_thero['N_r']-1)}

{show_design_result_table(best_thero['N_r']-1)}

4、提馏段最后一块板，即第{best_thero['number']}块板

{show_design_material(best_thero['number'] - 1)}

{show_design_result_table(best_thero['number']-1)}


第一块

{show_design_material(0)}

### 3、描绘负荷性能图（精馏段第一块板）

a. 漏液线

根据式${equations['V_s_load']()}$，$h_L=h_w+h_{{ow}}$，${equations['h_ow_load']()}$，${equations['h_sita_load']()}$

b. 过量雾沫夹带线

${equations['V_excess']()}$，$h_f=2.5(h_w+h_{{ow}})$，${equations['h_ow_load']()}$

c. 液相下限线

$L=\\frac{{0.006 \\times 1000}}{{2.84}}^{{1/3.2}}\\times l_w / 3600={example_plate['load_performance']['L_min']}m^3/s$

d. 液相上限线

$L=A_fH_T / 5={example_plate['load_performance']['L_max']}m^3/s$

e. 液泛线

$V=A_oC_o\\sqrt((0.5(H_T - h_w) - h_ow - h_d - h_l)\\gamma_L / (0.051 * \\gamma_V))$，${equations['h_ow_load']()}$，$h_d=0.153(L_s / (l_w\\cdot h_o))^2$

根据以上五条已知条件通过线性插值法，得到五条Vs-Ls 关系线，再将原点与操作点连线，即得到精馏段第一块板的负荷性能图，如下：

计算精馏段第一块板操作弹性：$\\frac{{V_{{max}}}}{{V_{{min}}}}={example_plate['load_performance']['V_max_div_V_min']}$，
$\\frac{{L_{{max}}}}{{L_{{min}}}}={example_plate['load_performance']['L_max_div_L_min']}$

同理，可得其他三块板的操作弹性：

{showOperationalResiliency()}

可见四块板气液相操作弹性均大于1.5，说明设计合理。

## 四、辅助设备的设计

### 1、塔高的设计

整个精馏塔所需的总理论板数为{best_thero['number']}块（不含塔釜再沸器），其中精馏段的理论塔板数为{best_thero['N_r']}块。实际塔板数{best_real['N_real_rounded']}块，精馏段理论塔板数为{best_real['N_real_r']}块，加料板在第{best_real['N_real_r'] + 1}块板，板间距$H_T$为{calculation.H_T}m；进料处取板间距${H_in}m$，在第{human_hole_str()}块板之间开人孔，取$Φ={D_human * 1000}mm$，开人孔处板间距${H_human}m$；第一块塔板到塔顶的距离${H_top}m$，最后一块塔板到塔底的距离${H_bottom}m$；间接蒸气加热裙座高度${H_heat}m$。综上求得全塔高度为${tower.H}m$，进料处高度为${tower.input_H}m$。

### 2、换热器的设计及选型

甲醇-水体系为一般体系，换热器材料选择碳钢。

冷却器选用

根据前面计算得到冷却器的面积${example_cooler['A']}m^2$ ，一般选用换热器的实际传热面积比计算所需传热面积大10%~25%，此处取20%，故$A={(1 + cooler.A_margin)*example_cooler['A']}$。选取换热器：换热管直径Φ=25×2mm（管心距32mm），公称直径为${cooler_choose['GN']}mm$，公称压力为${cooler_choose['PN']}MPa$，管程数$N={cooler_choose['N']}$，管子根数$n={cooler_choose['n']}$，中心排管数为${cooler_choose['c_n']}$，管程流通面积为${cooler_choose['A_tube']}m^2$，换热管长度为${cooler_choose['L']}mm$，换热面积为${cooler_choose['A']}m^2$。

预热器选用

根据前面计算得到冷却器的面积${example_preheat['A']}m^2$ ，一般选用换热器的实际传热面积比计算所需传热面积大10%~25%，此处取20%，故$A={(1 + 0.2)*example_preheat['A']}$。选取换热器：换热管直径Φ=25×2mm（管心距32mm），公称直径为${preheat_choose['GN']}mm$，公称压力为${preheat_choose['PN']}MPa$，管程数$N={preheat_choose['N']}$，管子根数$n={preheat_choose['n']}$，中心排管数为${preheat_choose['c_n']}$，管程流通面积为${preheat_choose['A_tube']}m^2$，换热管长度为${preheat_choose['L']}mm$，换热面积为${preheat_choose['A']}m^2$。

再沸器选用

根据前面计算得到冷却器的面积${example_reboiler['A']}m^2$ ，一般选用换热器的实际传热面积比计算所需传热面积大10%~25%，此处取20%，故$A={(1 + 0.2)*example_reboiler['A']}$。选取换热器：换热管直径Φ=25×2mm（管心距32mm），公称直径为${reboiler_choose['GN']}mm$，公称压力为${reboiler_choose['PN']}MPa$，管程数$N={reboiler_choose['N']}$，管子根数$n={reboiler_choose['n']}$，中心排管数为${reboiler_choose['c_n']}$，管程流通面积为${reboiler_choose['A_tube']}m^2$，换热管长度为${reboiler_choose['L']}mm$，换热面积为${reboiler_choose['A']}m^2$。

冷凝器选用

a. 选型：

冷却水走管程，塔顶馏出液走壳程，取间壁外侧污垢热阻$R_{{so}}=3.08\\times 10^{{-4}}m^2\\cdot K/W$，间壁外侧污垢热阻$R_{{si}}=1.72\\times 10^{{-4}}m^2\\cdot K/W$。

计算换热面积：

$t_{{h1}}=t_{{h2}}={best_real['t_top']}℃$
压力为${work.p_atm}kPa$，$m_h=V\\cdot M_V={condenser.m_h}kg/s$此温度下查得汽化潜热$r_{{solute}}={condenser.r_solute}kJ/kg$，$r_{{solvent}}={condenser.r_solvent}kJ/kg$，平均气话潜热$r={condenser.r}kJ/kg$。

冷却水进口温度为 ${initial_temp}℃$，出口为${condenser.t_c2}℃$，$\\Delta t_1={condenser.delta_t_1}℃$，$\\Delta t_2={condenser.delta_t_2}℃$，，$\\Delta t_m={condenser.delta_t_m}℃$。平均温度为${condenser.t_avc}℃$，此温度下$c_{{pc}}={condenser.c_pc}kJ/(kg\\cdot ℃)$。故$Q=m_h\\cdot r={condenser.Q}kW$，冷却水用量${equations['m']('c', condenser.Q, condenser.c_pc, initial_temp, condenser.t_c2, condenser.m_c)}$。${equations['A'](condenser.Q, K_cool, condenser.delta_t_m, condenser.A, 1)}$。

确定管长、管程数：设管程管内流速u=1.5m/s，管径Φ=25×2mm。公称直径为${condenser_choose['GN']}mm$，公称压力为${condenser_choose['PN']}MPa$，管程数$N={condenser_choose['N']}$，管子根数$n={condenser_choose['n']}$，中心排管数为${condenser_choose['c_n']}$，管程流通面积为${condenser_choose['A_tube']}m^2$，换热管长度为${condenser_choose['L']}mm$，换热面积为${condenser_choose['A']}m^2$。

b. 校核

ⅰ 管程冷却水的对流传热系数$\\alpha_i$：查得${condenser.t_avc}℃$时水的导热系数为$\\lambda={condenser.landa_water}W/(m\\cdot K)$，$\\mu={condenser.miu_water}cP$，$\\c_p={condenser.c_pc}kJ/(kg\\cdot ℃)$，$\\c_p={condenser.c_pc}kJ/(kg\\cdot ℃)$，$\\rho={condenser.rou_water} kg/m^3$，$u=\\frac{{m_c}}{{\\rho\\cdot \\A}}={condenser_check['u']}m/s$，则$Re=\\frac{{du\\rho}}{{\\mu}}={condenser_check['Re']}$，$Pr=\\frac{{c_p\\mu}}{{\\lambda}}={condenser_check['Pr']}$，$\\alpha_i=0.023\\frac{{\\lambda}}{{d}}Re^{{0.8}}Pr^{{0.4}}={condenser_check['alpha_i']}W/(m^2\\cdot K)$。

ⅱ 壳程蒸汽冷凝的对流传热系数：$r={condenser_check['r']}kJ/kg$，假设壁温为{int(condenser.t_h1) - 1}，则平均温度为${condenser_check['t_av']}℃$，此温度下，$\\rho={condenser_check['rou']}kg/m^3$，$\\mu={condenser_check['miu']}cP$，$\\lambda={condenser_check['landa']}W/(m\\cdot K)$。$\\alpha_o=0.725\\left(\\frac{{r\\rho^2 g\\lambda^3}}{{\\mu d_o\\Delta t}}\\right)^{{0.25}}={condenser_check['alpha_o']}W/(m^2\\cdot K)$。

校核壁温：$t_h-\\frac{{Q}}{{\\alpha_o A_o}} - t_{{wh}}={condenser_check['dis']}℃<1℃$，所以合理。

ⅲ 求K：$\\frac{{1}}{{K}}=\\frac{{1}}{{\\alpha_i}}\\frac{{d_o}}{{d_i}}+R_{{si}}\\frac{{A_o}}{{A_i}}+\\frac{{b}}{{\\lambda}}\\frac{{d_o}}{{d_m}}+R_{{so}}+\\frac{{1}}{{\\alpha_o}}\\rightarrow K={condenser_check['K']}W/(m^2\\cdot K)$

ⅳ重新计算换热面积：$A_1=\\frac{{Q}}{{K\\Delta t_m}}={condenser_check['A']}m^2$

ⅴ富裕度计算：$F=\\frac{{A_o-A_1}}{{A_1}}={condenser_check['F']}$

### 3、泵的设计及选型

进料泵（2 个，一个备用泵）：
采用离心泵强制进料。进料处高度为{tower.input_H}m，原料液高度为0.35m，设总管长12m。根据进料管选择结果，液体流速

### 4、接管尺寸的设计

a. 进料管：直接进料。查得${initial_temp}℃$时，$\\rho={input_pipe.rou}$。设流速$u=1m/s$，$Q={input_pipe.Q}$,则$d=\\sqrt{{\\frac{{4Q}}{{\pi u}}}}={input_pipe.d}m$，圆整后
选择冷拔无缝钢管，尺寸为${input_pipe.fai['D_o']}\\times {input_pipe.fai['b']}$

b. 回流管：设流速$u=1m/s$，$Q={re_pipe.Q}$,则$d=\\sqrt{{\\frac{{4Q}}{{\pi u}}}}={re_pipe.d}m$，圆整后选择冷拔无缝钢管，尺寸为${re_pipe.fai['D_o']}\\times {re_pipe.fai['b']}$

c. 釜液出口管：查得${best_real['t_bottom']}℃$时，$\\rho={bottom_pipe.rou}$。设流速$u=1m/s$，$Q={bottom_pipe.Q}$,则$d=\\sqrt{{\\frac{{4Q}}{{\pi u}}}}={bottom_pipe.d}m$，圆整后选择冷拔无缝钢管，尺寸为${bottom_pipe.fai['D_o']}\\times {bottom_pipe.fai['b']}$

d. 塔顶蒸汽管：设流速$u=20m/s$，$Q={top_pipe.Q}$,则$d=\\sqrt{{\\frac{{4Q}}{{\pi u}}}}={top_pipe.d}m$，圆整后选择冷拔无缝钢管，尺寸为${top_pipe.fai['D_o']}\\times {top_pipe.fai['b']}$

e. 塔釜蒸汽管：设流速$u=20m/s$，$Q={b_steam_pipe.Q}$,则$d=\\sqrt{{\\frac{{4Q}}{{\pi u}}}}={b_steam_pipe.d}m$，圆整后选择冷拔无缝钢管，尺寸为${b_steam_pipe.fai['D_o']}\\times {b_steam_pipe.fai['b']}$

### 5、贮槽的设计

a.原料槽（1 个，上个车间进入原料槽）：体积V=；

b.产品槽（1 个，产品进入下一车间）：体积V=；

c.回流槽（1 个）：体积V=。

高度设计：利用回流槽自然回流，设管长为1.5m，根据伯努利方程：$gz_1 + \\frac{{u_1^2}}{{2}}+\\frac{{p_1}}{{\\rho}}+w_e=gz_2 + \\frac{{u_2^2}}{{2}}+\\frac{{p_2}}{{\\rho}}+w_f$，选取回流槽液面与回流管出口截面进行计算，其中$u_1=u_2=0$无缝钢管$\\epsilon=0.05/mm$

### 6、重新计算总费用

（1）换热器费用：$C_F={fee_C_F}A=2000\\times ({cooler.A} + {preheat.A} + {Reboiler.A}+{condenser.A})={2000*(cooler.A + preheat.A + Reboiler.A+condenser.A)}元$

（3）蒸汽费用：$C_S={fee_steam}W_{{steam}}={fee_steam}\\times ({example_preheat['m_h']} + {example_reboiler['m_h']})/1000 \\times 3600 \\times {time}={example_whole_cost['C_S']}元$

（4）塔体费用：$C_D={cost_R['min'][1]}元$
