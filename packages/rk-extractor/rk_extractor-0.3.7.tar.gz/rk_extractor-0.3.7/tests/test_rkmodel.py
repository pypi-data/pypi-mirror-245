import ROOT
import zfit
import numpy

from rk_model   import rk_model
from mc_reader  import mc_reader as mc_rdr
from np_reader  import np_reader as np_rdr
from cs_reader  import cs_reader as cs_rdr

import matplotlib.pyplot as plt
import rk.utilities      as rkut
import pytest
import pprint
import os

#-----------------------------
def delete_all_pars():
    d_par = zfit.Parameter._existing_params
    l_key = list(d_par.keys())

    for key in l_key:
        del(d_par[key])
#----------------------------------------------------
def rename_keys(d_data, use_txs=True):
    d_rename = {}
    if use_txs:
        d_rename[  'r1_TOS'] = d_data['d1']
        d_rename[  'r1_TIS'] = d_data['d1']

        d_rename['r2p1_TOS'] = d_data['d2']
        d_rename['r2p1_TIS'] = d_data['d2']

        d_rename['2017_TOS'] = d_data['d3']
        d_rename['2017_TIS'] = d_data['d3']

        d_rename['2018_TOS'] = d_data['d4']
        d_rename['2018_TIS'] = d_data['d4']
    else:
        d_rename[  'r1']     = d_data['d1']
        d_rename['r2p1']     = d_data['d2']
        d_rename['2017']     = d_data['d3']
        d_rename['2018']     = d_data['d4']

    return d_rename
#-----------------------------
def skip_test():
    try:
        uname = os.environ['USER']
    except:
        pytest.skip()

    if uname in ['angelc', 'campoverde']:
        return

    pytest.skip()
#----------------------
def test_simple():
    d_eff = {'d1' :   (0.5, 0.4), 'd2' :   (0.4, 0.3), 'd3' :   (0.3, 0.2), 'd4' :   (0.2, 0.1)}
    d_nent= {'d1' :          1e3, 'd2' :          1e3, 'd3' :          1e3, 'd4' :          1e3}
    d_mcmu= {'d1' : (5000, 4900), 'd2' : (5100, 4900), 'd3' : (5100, 4800), 'd4' : (5200, 5100)}
    d_mcsg= {'d1' :      (2,  4), 'd2' :     (1, 1.8), 'd3' :       (2, 3), 'd4' :       (3, 4)}

    d_eff =rename_keys(d_eff)
    d_nent=rename_keys(d_nent, use_txs=False)
    d_mcmu=rename_keys(d_mcmu)
    d_mcsg=rename_keys(d_mcsg)

    mod         = rk_model(preffix='simple', d_eff=d_eff, d_mcmu=d_mcmu, d_mcsg=d_mcsg, d_nent=d_nent)
    d_mod       = mod.get_model()

    delete_all_pars()
#----------------------
def test_data():
    d_eff = {'d1' :   (0.5, 0.4), 'd2' :   (0.4, 0.3), 'd3' :   (0.3, 0.2), 'd4' :   (0.2, 0.1)}
    d_nent= {'d1' :          1e3, 'd2' :          1e3, 'd3' :          1e3, 'd4' :          1e3}
    d_mcmu= {'d1' : (5000, 4900), 'd2' : (5100, 4900), 'd3' : (5100, 4800), 'd4' : (5200, 5100)}
    d_mcsg= {'d1' :      (2,  4), 'd2' :     (1, 1.8), 'd3' :       (2, 3), 'd4' :       (3, 4)}

    d_eff =rename_keys(d_eff)
    d_nent=rename_keys(d_nent, use_txs=False)
    d_mcmu=rename_keys(d_mcmu)
    d_mcsg=rename_keys(d_mcsg)

    mod         = rk_model(preffix='data', d_eff=d_eff, d_mcmu=d_mcmu, d_mcsg=d_mcsg, d_nent=d_nent)
    d_mod       = mod.get_data()

    delete_all_pars()
#----------------------
def test_rseed():
    d_eff = {'d1' :   (0.5, 0.4), 'd2' :   (0.4, 0.3), 'd3' :   (0.3, 0.2), 'd4' :   (0.2, 0.1)}
    d_nent= {'d1' :          1e3, 'd2' :          1e3, 'd3' :          1e3, 'd4' :          1e3}
    d_mcmu= {'d1' : (5000, 4900), 'd2' : (5100, 4900), 'd3' : (5100, 4800), 'd4' : (5200, 5100)}
    d_mcsg= {'d1' :      (2,  4), 'd2' :     (1, 1.8), 'd3' :       (2, 3), 'd4' :       (3, 4)}

    d_eff =rename_keys(d_eff)
    d_nent=rename_keys(d_nent, use_txs=False)
    d_mcmu=rename_keys(d_mcmu)
    d_mcsg=rename_keys(d_mcsg)

    mod_1   = rk_model(preffix='data1', d_eff=d_eff, d_mcmu=d_mcmu, d_mcsg=d_mcsg, d_nent=d_nent)
    d_dat_1 = mod_1.get_data(rseed=0)

    mod_2   = rk_model(preffix='data2', d_eff=d_eff, d_mcmu=d_mcmu, d_mcsg=d_mcsg, d_nent=d_nent)
    d_dat_2 = mod_2.get_data(rseed=0)

    plt_dir = f'tests/rk_model/rseed'
    os.makedirs(plt_dir, exist_ok=True)
    for index in [0, 1]:
        kind = 'mm' if index == 0 else 'ee'
        for key in d_dat_1:
            arr_dat_1 = d_dat_1[key][index].numpy().flatten()
            arr_dat_2 = d_dat_2[key][index].numpy().flatten()

            close = numpy.allclose(arr_dat_1, arr_dat_2, atol=1e-5)
            assert(close)

            min_x, max_x = min(arr_dat_1), max(arr_dat_1)

            plt.hist(arr_dat_1, bins=30, range=(min_x, max_x), histtype='step', linestyle='-', label='First')
            plt.hist(arr_dat_2, bins=30, range=(min_x, max_x), histtype='step', linestyle=':', label='Second')
            plt.legend()
            plt.savefig(f'{plt_dir}/{key}_{kind}.png')
            plt.close('all')

    delete_all_pars()
#----------------------
def test_cons():
    d_eff = {'d1' :   (0.5, 0.4), 'd2' :   (0.4, 0.3), 'd3' :   (0.3, 0.2), 'd4' :   (0.2, 0.1)}
    d_nent= {'d1' :          1e3, 'd2' :          1e3, 'd3' :          1e3, 'd4' :          1e3}
    d_mcmu= {'d1' : (5000, 4900), 'd2' : (5100, 4900), 'd3' : (5100, 4800), 'd4' : (5200, 5100)}
    d_mcsg= {'d1' :      (2,  4), 'd2' :     (1, 1.8), 'd3' :       (2, 3), 'd4' :       (3, 4)}

    d_eff =rename_keys(d_eff)
    d_nent=rename_keys(d_nent, use_txs=False)
    d_mcmu=rename_keys(d_mcmu)
    d_mcsg=rename_keys(d_mcsg)

    mod         = rk_model(preffix='cons', d_eff=d_eff, d_mcmu=d_mcmu, d_mcsg=d_mcsg, d_nent=d_nent)
    d_mod       = mod.get_cons()

    delete_all_pars()
#----------------------
def main():
    test_rseed()
    test_cons()
    test_simple()
    test_data()
#----------------------
if __name__ == '__main__':
    main()

