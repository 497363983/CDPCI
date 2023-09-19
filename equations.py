"""generate equations in latex format
"""
equations = {
    'F':
    lambda capacity, time, F_kg, w_F, M_solute, M_solvent, F:
    'F = \\frac{%s \\times 1000kg}{%sh} = %s kg/h = \\frac{%s \\times %s}{%s} + \\frac{%s \\times %s}{%s} = %s kmol/h'
    % (capacity, time, F_kg, F_kg, w_F, M_solute, F_kg, 1 - w_F, M_solvent, F),
    'x_F':
    lambda w_F, M_solute, M_solvent, x_F:
    'x_F = \\frac{%s / %s}{%s / %s + %s / %s} = %s' %
    (w_F, M_solute, w_F, M_solute, 1 - w_F, M_solvent, x_F),
    'x_D':
    lambda x_o, M_solute, M_solvent, x_D:
    'x_D = \\frac{ %s / %s }{%s / %s + %s / %s} = %s' %
    (x_o, M_solute, x_o, M_solute, 1 - x_o, M_solvent, x_D),
    'D':
    lambda eta, F, x_F, x_D, D:
    'D = \\frac{\\eta F x_F}{x_D} = \\frac{%s \\times %s \\times %s }{%s} =%s kmol/h'
    % (eta, F, x_F, x_D, D),
    'W':
    lambda F, D, W: 'W = F - D = %s - %s = %s kmol/h' % (F, D, W),
    'x_w':
    lambda F, x_F, D, x_D, W, x_w:
    'x_w = \\frac{ F \\cdot x_F - D \\cdot x_D }{W} = \\frac{ %s \\times %s - %s \\times %s }{%s} = %s'
    % (F, x_F, D, x_D, W, x_w),
    'P_solute':
    lambda name, p_atm, x_D, x_i, P_solute:
    'P_{%s}^{\\circ} = p_{atm} \\cdot x_D/x = %s \\times %s / %s = %s kPa' %
    (name, p_atm, x_D, x_i, P_solute),
    'T_antoine':
    lambda sub, A, B, C, P, T, log='lg', unit='℃':
    'T_{%s}=\\frac{B}{A - \\%s P^{\\circ}} - C = \\frac{%s}{%s - \\%s%s} - %s = %s%s'
    % (sub, log, B, A, log, P, C, T, unit),
    'P_antoine':
    lambda sub, A, B, C, T, P:
    'P_{%s}^\\circ = e^{A-\\frac{B}{T+C}} = e^{%s-\\frac{%s}{%s+%s}} = %s kPa'
    % (sub, A, B, T, C, P),
    'alpha':
    lambda sub, solute, solvent, P_solute, P_solvent, alpha:
    '\\alpha_{%s}=\\frac{P^\\circ_{%s}}{P^\\circ_{%s}}=\\frac{%s}{%s}=%s' %
    (sub, solute, solvent, P_solute, P_solvent, alpha),
    'alpha_average':
    lambda alpha_top, alpha_bottom, alpha:
    '\\overline{\\alpha}=\\sqrt{\\alpha_顶 \\cdot \\alpha_釜}=\\sqrt{%s \\cdot %s} = %s'
    % (alpha_top, alpha_bottom, alpha),
    'miu_relate':
    lambda x_solute, miu_solute, miu_solvent, miu:
    '\\lg\\overline{\\mu}=\\sum x_i lg\\mu_i=%s\\times\\lg%s+%s\\times\\lg%s\\rightarrow\\overline{\\mu}=%s'
    % (x_solute, miu_solute, 1 - x_solute, miu_solvent, miu),
    'E_T':
    lambda f, alpha, miu, E_T:
    'E_T=0.49f(\\overline{\\alpha}\\cdot\\overline{\\mu})^{-0.245}=0.49\\times%s\\times(%s\\times%s)^{-0.245}=%s'
    % (f, alpha, miu, E_T),
    'N_T':
    lambda N, E_T, N_T: 'N_T=\\frac{N}{E_T}=\\frac{%s}{%s}=%s块' %
    (N, E_T, N_T),
    'M':
    lambda sub, x_solute, M_solute, M_solvent, M:
    'M_{%s}=%s\\times%s+%s\\times%s=%skg/kmol' %
    (sub, x_solute, M_solute, 1 - x_solute, M_solvent, M),
    'gama':
    lambda sub, p, M, T, gama, R=8.314:
    '\\gamma_%s=\\frac{pM}{RT}=\\frac{%s\\times%s}{%s\\times%s}=%skg/m^3' %
    (sub, p, M, R, T, gama),
    'gama_rou':
    lambda sub, x, rou_solute, rou_solvent, gama:
    '\\gamma_{%s}=\\frac{1}{%s/%s+%s/%s}=%skg/m^3' %
    (sub, x, rou_solute, 1 - x, rou_solvent, gama),
    'V':
    lambda R, D, V: 'V=(R+1)\\cdot D=(%s+1)\\times%s=%skmol/h' % (R, D, V),
    'V_s':
    lambda V, M_v, gama_v, V_s:
    'V_S=\\frac{VM_V}{3600\\gamma_V}=\\frac{%s\\times%s}{3600\\times%s}=%sm^3/s'
    % (V, M_v, gama_v, V_s),
    'L':
    lambda V, D, L: 'L=V-D=%s-%s=%skmol/h' % (V, D, L),
    'L_S':
    lambda L, M_L, gama_L, L_s:
    'L_S=\\frac{LM_L}{3600\\gamma_L}=\\frac{%s\\times%s}{3600\\times%s}=%sm^3/s'
    % (L, M_L, gama_L, L_s),
    'L_V':
    lambda L_S, V_S, gama_L, gama_V, L_V:
    '\\frac{L_S}{V_S}\\left(\\frac{\\gamma_L}{\\gamma_V}\\right)^{0.5}=\\frac{%s}{%s}\\left(\\frac{%s}{%s}\\right)^{0.5}=%s'
    % (L_S, V_S, gama_L, gama_V, L_V),
    'C_sita':
    lambda C_20, sita, C_sita:
    'C_{\\sigma}=\\frac{C_{20}}{\\left(\\frac{20}{\\sigma}\\right)^{0.2}}=\\frac{%s}{\\left(\\frac{20}{%s}\\right)^{0.2}}=%s'
    % (C_20, sita, C_sita),
    'w_G':
    lambda C_sita, gama_L, gama_V, w_G:
    'w_{G(max)}=C_{\\sigma}\\sqrt{\\frac{\\gamma_L - \\gamma_V}{\\gamma_V}}=%s\\sqrt{\\frac{%s - %s}{%s}}=%sm/s'
    % (C_sita, gama_L, gama_V, gama_V, w_G),
    'D_':
    lambda V_s, w, D:
    'D^{\\prime}=\\sqrt{\\frac{V_S}{0.785w}}=\\sqrt{\\frac{%s}{0.785 \\times %s}}=%sm'
    % (V_s, w, D),
    'delta_t_m':
    lambda t1, t2, t:
    '\\Delta t_m = \\frac{\\Delta t_2 - \\Delta t_1}{\ln \\frac{\\Delta t_2}{\\Delta t_1}}=\\frac{%s - %s}{\ln \\frac{%s}{%s}}=%s℃'
    % (t2, t1, t2, t1, t),
    'Q':
    lambda m, c_p, t_1, t_2, Q:
    'Q=mc_p\\Delta t=%s\\times %s\\times (%s-%s)=%skW' % (m, c_p, t_2, t_1, Q),
    'A':
    lambda Q, K, delta_t, A, loss_Q=1.05:
    'A=\\frac{%sQ}{K\\Delta t_m}=\\frac{%s\\times %s}{%s\\times %s}=%sm^2' %
    (loss_Q, loss_Q, Q, K, delta_t, A),
    'm':
    lambda sub, Q, c, t1, t2, m:
    'm_{%s}=\\frac{Q}{c_p\\Delta t}=\\frac{%s}{%s\\times (%s-%s)}=%skg/s' %
    (sub, Q, c, t2, t1, m),
    'L_':
    lambda R, D, L: 'L=RD=%s\\times %s=%skmol/h' % (R, D, L),
    'V_':
    lambda V, F, q, V_: 'V^{\\prime}=V-(1-q)F=%s-(1-%s)\\times%s=%skmol/h' %
    (V, q, F, V_),
    'L__':
    lambda L, q, F, L__: 'L^{\\prime}=L+qF=%s+%s\\times %s=%skmol/h' %
    (L, q, F, L__),
    'w_G_':
    lambda V_S, A_T, A_f, w_G:
    'w_G=\\frac{V_S}{A_T-A_f}=\\frac{%s}{%s-%s}=%sm/s' % (V_S, A_T, A_f, w_G),
    'e_v':
    lambda sita, w_G, H_T, h_f, e_v:
    'e_V=0.22\\left(\\frac{73}{\\sigma}\\right)\\left(\\frac{w_G}{12(H_T-h_f)}\\right)^{3.2}=0.22\\times \\left(\\frac{73}{%s}\\right)\\left(\\frac{%s}{12\\times (%s-%s)}\\right)^{3.2}=%skg/kg气'
    % (sita, w_G, H_T, h_f, e_v),
    't':
    lambda A_f, H_T, L_s, t:
    '\\tau=\\frac{A_f\\cdot H_T}{L_S}=\\frac{%s\\times %s}{%s}=%ss' %
    (A_f, H_T, L_s, t),
    'h_ow':
    lambda L_s, l_w, h_ow, E=1:
    'h_{ow}=\\frac{2.84}{1000}\\left(\\frac{L_S}{l_w}\\right)^{\\frac{2}{3}}E=\\frac{2.84}{1000}\\left(\\frac{%s}{%s}\\right)^{\\frac{2}{3}}\\times %s=%sm'
    % (L_s, l_w, E, h_ow),
    'b':
    lambda l_w, D, b: 'b=\\frac{l_w+D}{2}=\\frac{%s+%s}{2}=%s' % (l_w, D, b),
    'Z_1':
    lambda D, W_d, Z_1: 'Z_1=D-2W_d=%s-2\\times %s=%sm' % (D, W_d, Z_1),
    'Delta':
    lambda b, h_f, miu, L_s, Z_1, gama_L, Delta:
    '\\Delta=\\frac{0.215(250b+1000h_f)^2\\mu (3600L_S)Z_1}{(1000bh_f)^3\\gamma_L}=\\frac{0.215\\times (250\\times %s+1000\\times %s)^2\\times %s \\times (3600\\times %s)\\times %s}{(1000\\times %s \\times %s)^3\\times %s}=%sm'
    % (b, h_f, miu, L_s, Z_1, b, h_f, gama_L, Delta),
    'h_0':
    lambda h_w, h_0: 'h_0=h_w-0.01=%s-0.01=%sm' % (h_w, h_0),
    'x':
    lambda D, W_d, W_s, x: 'x=\\frac{D}{2}-(W_d+W_s)=\\frac{%s}{2}-(%s+%s)=%sm'
    % (D, W_d, W_s, x),
    'r':
    lambda D, W_c, r: 'r=\\frac{D}{2}-W_c=\\frac{%s}{2}-%s=%sm' % (D, W_c, r),
    'A_a':
    lambda x, r, A_a:
    'A_a = 2\\left(x\\sqrt{r^2 - x^2} + r^2arcsin(\\frac{x}{r})\\right)=2\\times\\left(%s\\times\\sqrt{%s^2 - %s^2} + %s^2\\times arcsin(\\frac{%s}{%s})\\right)=%sm^2'
    % (x, r, x, r, x, r, A_a),
    'n':
    lambda t, A_a, n:
    'n=1158 \\times 1000 / (t \\times 1000)^2 \\times A_a=1158 \\times 1000 / (%s \\times 1000)^2 \\times %s=%s个'
    % (t, A_a, n),
    'w_0':
    lambda V_s, A_o, w_0: 'w_0=\\frac{V_S}{A_0}=\\frac{%s}{%s}=%sm/s' %
    (V_s, A_o, w_0),
    'h_c':
    lambda d_o, h_c:
    'h_c = 0.051(w_o / C_o)^2(\\gamma_v / \\gamma_L)(1 - (A_o/A_a)^2)=%sm液柱' %
    (h_c) if d_o < 0.012 else
    'h_c = 0.051(w_o /(C_o\\beta))^2(\\gamma_V /\\gamma_L)(1 - (A_0/A_a)^2)=%sm液柱'
    % (h_c),
    'h_sita':
    lambda sita, gama_L, d_0, h_sita:
    'h_\\sigma=\\frac{4\\sigma}{9810\\gamma_Ld_0}=\\frac{4\\times %s}{9810\\times %s \\times %s}=%s'
    % (sita, gama_L, d_0, h_sita),
    'w_0m':
    lambda C_o, h_L, h_sita, gama_L, gama_v, w_0m:
    'w_{0m}=4.4C_0\\sqrt{(0.0056 + 0.13h_L - h_\\sigma)\\gamma_L / \\gamma_v}=4.4\\times %s\\sqrt{(0.0056 + 0.13\\times %s - %s)\\times %s / %s}=%sm/s'
    % (C_o, h_L, h_sita, gama_L, gama_v, w_0m),
    'F_o':
    lambda w_o, gama_v, F_o: 'F_0=w_0\\sqrt{\\gamma_V}=%s\\times \\sqrt{%s}=%s'
    % (w_o, gama_v, F_o),
    'h_d':
    lambda L_s, l_w, h_0, h_d:
    'h_d=0.153(L_s / (l_wh_o))^2=0.153\\times (%s / (%s\\times %s))^2=%sm液柱' %
    (L_s, l_w, h_0, h_d),
    'H_d':
    lambda H_d: 'H_d=h_d + h_p + h_L=%sm液柱' % (H_d),
    'w_f':
    lambda L_s, A_f, w_f: 'w_f=\\frac{L_s}{A_f}=\\frac{%s}{%s}=%sm/s' %
    (L_s, A_f, w_f),
    'V_s_load':
    lambda:
    'V=4.4A_0KC_0\\sqrt{(0.0056 + 0.13h_L - h_\\sigma)\\gamma_L / \\gamma_v}',
    'h_ow_load':
    lambda:
    'h_{ow}=\\frac{2.84}{1000}\\left(\\frac{L_S}{l_w}\\right)^{\\frac{2}{3}}E',
    'h_sita_load':
    lambda:
    'h_\\sigma=\\frac{4\\sigma}{9810\\gamma_Ld_0}',
    'V_excess':
    lambda:
    'V=((0.1sita) / 0.0057)^(1 / 3.2)(A_T - A_f)(H_T - h_f)'
}
