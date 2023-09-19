import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm, rcParams
import os
import pandas as pd
from scipy import interpolate
import numpy as np

sns.set_style(style="whitegrid")


def sci_notation_2_float(number: str) -> str:
    is_minus = False
    if number.startswith('-'):
        is_minus = True
        number = number[1:]
    if 'e' in number or 'E' in number:
        number = number.split('e') if 'e' in number else number.split('E')
        if '-' in number[1]:
            number[1] = int(number[1].replace('-', ''))
            return '-' if is_minus else '' + '0.' + '0' * (
                number[1] - 1) + number[0].replace('.', '')
        else:
            number[1] = int(number[1])
            split_number = number[0].split('.')
            if len(split_number) == 1:
                return '-' if is_minus else '' + number[0] + '0' * number[1]
            else:
                return '-' if is_minus else '' + split_number[
                    0] + split_number[1] + '0' * (number[1] -
                                                  len(split_number[1]))
    else:
        return number


def if_add(number: str, index: int) -> bool:
    assert number[
        index] != '.', "The index of the number should not be the decimal point."
    assert number[
        index] != '-', "The index of the number should not be the negative sign."
    assert number[
        index] != '+', "The index of the number should not be the positive sign."
    assert number[
        index] != 'e', "The index of the number should not be the scientific notation."
    assert number[
        index] != 'E', "The index of the number should not be the scientific notation."
    assert number[index], "The index of the number should not be empty."
    if type(number) != str:
        number = str(number)
    else:
        number = sci_notation_2_float(number)
    # print(number)
    digit = int(number[index])
    judge_digit = int(number[index + 1])
    # print(digit, judge_digit)
    if judge_digit >= 6:
        return True
    elif judge_digit <= 4:
        return False
    else:
        if digit % 2 == 0:
            return False
        else:
            return True


def is_number(number: str):
    try:
        float(number)
        return True
    except ValueError:
        pass
    return False


def add_digit(number: str):
    assert type(number) == str, 'number must to be str'
    if len(number) == 0:
        return number
    last_digit = number[-1]
    number = number[:-1]
    if not is_number(last_digit):
        return add_digit(number) + last_digit
    else:
        last_digit = int(last_digit)
    if last_digit + 1 >= 10:
        # print(add_digit(number), number)
        return add_digit(number) + str((last_digit + 1) % 10)
    else:
        return number + str(last_digit + 1)


def sci_round(number: float, n: int = 2) -> float:
    is_minus = False
    number = float(number)
    if n is None:
        return number
    if number < 0:
        is_minus = True
        number = -number
    # print(number)
    number = sci_notation_2_float(str(number))
    # print(number)
    temp = str(number).split('.')
    if len(temp) <=1:
        return number
    else:
        integer, decimals = temp
    # print(integer, decimals)
    decimals = '0.' + decimals
    # print(decimals)
    str_decimals = str(decimals)[2:]
    if int(integer) == 0:
        start = 0
        for index, digit in enumerate(str_decimals):
            if digit != '0':
                start = index
                break
        not_zero = str_decimals[start:]
        if len(not_zero) <= n:
            return float(('-' if is_minus else '') + '0.' + str_decimals)
        # print('start', start)
        str_decimals = '0.' + str_decimals[0:start + n + 1]
        if if_add(str_decimals, start + n + 1):
            # str_decimals = str_decimals[0:start + n + 1] + str(
            #     int(str_decimals[start + n + 1]) + 1)
            str_decimals = add_digit(str_decimals[0:start + n + 2])
        else:
            str_decimals = str_decimals[0:start + n + 2]
        return float(('-' if is_minus else '') + str_decimals)
    else:
        str_integer = str(int(integer))
        if len(str_decimals) > n:
            str_decimals = '0.' + str_decimals[0:n + 1]
            if if_add(str_decimals, n + 1):
                # str_decimals = str_decimals[0:n + 1] + str(
                #     int(str_decimals[n + 1]) + 1)
                str_decimals = add_digit(str_integer + str_decimals[1:n + 2])
            else:
                str_decimals = str_integer + str_decimals[1:n + 2]
            return float(('-' if is_minus else '') + str_decimals)
        else:
            return float(('-' if is_minus else '') + str_integer + '.' +
                         str_decimals)


def one_D_matching(x, y, k: int = 3, n: int = 300):
    x_new = np.linspace(x.min(), x.max(), n)
    y_smooth = interpolate.make_interp_spline(x=x, y=y, k=k)(x_new)
    return (x_new, y_smooth)


def get_zero_point(X, Y, k: int = 3):
    tck = interpolate.make_interp_spline(x=X, y=Y, k=k)
    piecewise_polynomial = interpolate.PPoly.from_spline(tck, extrapolate=None)
    roots = piecewise_polynomial.roots()
    return roots


def mmHg_2_kPa(mmHg: float) -> float:
    return mmHg * 0.133322


def kgf_to_kPa(kgf: float) -> float:
    return kgf * 0.9678 * 101.325  # kPa


def kPa_to_kgf(kPa: float) -> float:
    return kPa / 0.9678 / 101.325  # kgf/cm^2


def kPa_2_mmHg(kPa: float) -> float:
    return kPa / 0.133322


def kgf_to_mmHg(kgf: float) -> float:
    return kPa_2_mmHg(kgf_to_kPa(kgf))


def get_miu():
    pass


def draw(draw_func,
         title='',
         size=(12, 6),
         save=False,
         filename=None,
         dpi=500,
         subplots=False):
    assert draw, "draw must be given"
    fpath = os.path.abspath("./fonts/STSONG.TTF")
    fe = fm.FontEntry(fname=fpath, name='STSONG')
    fm.fontManager.ttflist.insert(0, fe)  # or append is fine
    rcParams['font.family'] = fe.name  # = 'your custom ttf font name'
    # prop = fm.FontProperties(fname=fpath)
    if not subplots:
        plt.figure(figsize=size, dpi=dpi)
        plt.title(title)
        draw_func()
    else:
        fig, ax = plt.subplots(1, 1, figsize=size)
        draw_func(fig, ax)
    if save:
        assert filename, "filename must be given"
        plt.savefig(filename)
    # plt.close()


def temp_to_K(temp: float) -> float:
    return temp + 273.15


def temp_to_C(temp: float) -> float:
    return temp - 273.15


def ge_y_by_x(X, Y, x):
    y = np.interp(x, X, Y)
    return y


def get_rou_by_t(rou_t_dict, t):
    df = pd.DataFrame.from_dict(rou_t_dict)
    df.sort_values(by='rou', inplace=True)
    rou_t_dict = df.to_dict(orient='list')
    t_list = np.array(rou_t_dict['t'])
    rou_list = np.array(rou_t_dict['rou'])
    rou = get_zero_point(rou_list, t_list - t)[0]
    return rou


def get_miu_by_t(miu_t_dict, t):
    df = pd.DataFrame.from_dict(miu_t_dict)
    df.sort_values(by='miu', inplace=True)
    miu_t_dict = df.to_dict(orient='list')
    t_list = np.array(miu_t_dict['t'])
    miu_list = np.array(miu_t_dict['miu'])
    # miu = get_zero_point(miu_list, t_list - t)
    miu = np.interp(t, t_list, miu_list)
    # print('miu', miu)
    return miu


def get_sita_by_t(sita_t_dict, t):
    df = pd.DataFrame.from_dict(sita_t_dict)
    df.sort_values(by='sita', inplace=True)
    sita_t_dict = df.to_dict(orient='list')
    t_list = np.array(sita_t_dict['t'])
    sita_list = np.array(sita_t_dict['sita'])
    rou = get_zero_point(sita_list, t_list - t)[0]
    return rou


def D_round(D, standard=None):    
    if standard is None:
        standard = [0.6, 0.7, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4]
    for i in standard:
        if D <= i:
            return i
    return D


def get_C_20(H, L_v):
    """
    Parameters
    ----------
    H: float
    L_v : float

    Reference
    ---------
    [1] :cite:`浙江工业大学化工原理教研室: 化工原理课程设计资料——板式塔指导书, 39, 2017
    """
    C_20 = np.exp(-4.531 + 1.6562 * H + 5.5496 * H**2 - 6.4695 * H**3 +
                  (-0.474675 + 0.079 * H - 1.39 * H**2 + 1.3212 * H**3) *
                  np.log(L_v) +
                  (-0.07291 + 0.088307 * H - 0.49123 * H**2 + 0.43196 * H**3) *
                  (np.log(L_v))**2)
    return C_20


alcohol_c_p = {
    't': [25, 50, 75, 100, 125, 150],
    'c_p': [1.32, 1.72, 2.17, 2.63, 3.09, 3.53]
}

water_c_p = {
    't': [0, 20, 50, 100, 150],
    'c_p': [4.215, 4.181, 4.180, 4.215, 4.310]
}


def get_c_p_by_t(cp_dict, t):
    t_list = np.array(cp_dict['t'])
    cp_list = np.array(cp_dict['c_p'])
    cp = np.interp(t, t_list, cp_list)
    return cp


def get_latent_heat_t(latent_heat_dict, t):
    t_list = np.array(latent_heat_dict['t'])
    latent_heat_list = np.array(latent_heat_dict['latent_heat'])
    latent_heat = np.interp(t, t_list, latent_heat_list)
    return latent_heat


def get_landa_by_t(landa_dict, t):
    t_list = np.array(landa_dict['t'])
    landa_list = np.array(landa_dict['landa'])
    landa = np.interp(t, t_list, landa_list)
    return landa


def get_temp_by_p(antoine_factor, p, log=np.log10):
    return antoine_factor[1] / (antoine_factor[0] - log(p)) - antoine_factor[2]


def get_p_by_temp(antoine_factor, t, back=10):
    return back**(antoine_factor[0] - antoine_factor[1] /
                  (t + antoine_factor[2]))


def find_by_key(array, key, value):
    for item in array:
        if item[key] == value:
            return item


def get_value_of_key(array, key):
    value = []
    for item in array:
        value.append(item[key])
    return value


def five_round(num, type_='up', multiple=1000):
    assert type_ in ['up', 'down'], "type_ must be 'up' or 'down'"
    num = np.ceil(num * multiple)
    judge = num % 10
    if judge == 5 or judge == 0:
        return num / multiple
    elif judge > 5:
        add = 10 if type_ == 'up' else 5
        return (num - judge + add) / multiple
    else:
        add = 5 if type_ == 'up' else 0
        return (num - judge + add) / multiple


def table(data, column_num=None, row_num=None, type='list'):
    """Geneate a table in markdown format.
 
    Parameters
    ----------
    data : list
        data to be shown in table.
    column_num : int
        number of columns.
    row_num : int
        number of rows.
    type : str
        type of data, 'list' or 'dict'.

    Returns
    -------
    table : str
        table in markdown format.
  
    Examples
    --------
    >>> list_data = [{'a': 1, 'b': 2}, {'a': 3, 'b': 456}]
    >>> table(liat_data, type='list')
    |  a  |  b  |
    |-----|-----|
    |  1  |  2  |
    |  3  | 456 |
    >>> dict_data = {'a': [1, 3], 'b': [2, 456]}
    >>> table(dict_data, type='dict')
    |  a  |  b  |
    |-----|-----|
    |  1  |  2  |
    |  3  | 456 |
    """
    if type == 'list':
        # assert column_num is not None and row_num is not None, \
        #     'column_num and row_num must be given.'
        keys = list(data[0].keys())
        if row_num is None:
            row_num = len(data)
        if column_num is None:
            column_num = len(keys)
        table = '|'
        for key in keys:
            table += ' ' + str(key) + ' |'
        table += '\n|'
        for i in range(column_num):
            table += '---|'
        table += '\n'
        for i in range(row_num):
            row = '|'
            for j in range(column_num):
                row += ' ' + str(data[i][keys[j]]) + ' |'
            table += row + '\n'
        return table
    elif type == 'dict':
        # assert column_num is None and row_num is None, \
        #     'column_num and row_num must be None.'
        table = '|'
        for key in data.keys():
            table += '  ' + str(key) + ' |'
        table += '\n|'
        for i in range(len(data.keys())):
            table += '---|'
        table += '\n'
        for i in range(len(data[list(data.keys())[0]])):
            row = '|'
            for key in data.keys():
                row += ' ' + str(data[key][i]) + ' |'
            table += row + '\n'
        return table
    else:
        raise ValueError('type must be list or dict.')


def find_intersections(X1: list, Y1: list, X2: list, Y2: list, k: int=3):
    [X1, Y1, X2, Y2] = [np.array(X1), np.array(Y1), np.array(X2), np.array(Y2)]
    if np.all(np.diff(X1) > 0) and np.all(np.diff(X2) > 0):
        pass
    else:
        raise ValueError('X1 and X2 must be monotonically increasing.')

    def find_common_definition_domain(X1: np.ndarray, X2: np.ndarray):
        X1.sort()
        X2.sort()
        a = np.max([X1[0], X2[0]])
        b = np.min([X1[-1], X2[-1]])
        X = np.array(list(set(np.append(X1, X2))))
        X.sort()
        X = X[np.logical_and(X >= a, X <= b)]
        return X

    X_new = find_common_definition_domain(X1, X2)
    Y1_new = np.interp(X_new, X1, Y1)
    Y2_new = np.interp(X_new, X2, Y2)
    Y_new = Y1_new - Y2_new
    tck = interpolate.splrep(X_new, Y_new, k=k)
    poly = interpolate.PPoly.from_spline(tck, extrapolate=None)
    X_intersections = poly.roots()
    X_intersections = X_intersections[np.logical_and(X_intersections >= X_new[0], X_intersections <= X_new[-1])]
    Y_intersections = np.interp(X_intersections, X1, Y1)
    return {'X': X_intersections, 'Y': Y_intersections}


def readTextFile(file, encoding="utf-8") -> str:
    assert os.path.exists(file), f"File {file} does not exist."
    with open(file, "r", encoding=encoding) as f:
        return f.read()