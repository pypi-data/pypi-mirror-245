from setuptools import setup, find_packages

import os
import glob

#----------------------------------------------
def get_scripts(dir_path):
    l_obj = glob.glob(f'{dir_path}/*')
    l_scr = [ obj for obj in l_obj if os.path.isfile(obj)]

    return l_scr
#----------------------------------------------
setup(
        name              = 'rk_extractor',
        version           = '0.3.6',
        description       = 'Used to extract RK from simultaneous fits',
        scripts           = get_scripts('scripts/jobs') + get_scripts('scripts/offline'),
        long_description  = '',
        package_dir       = {'' : 'src'},
        packages          = [''],
        install_requires  = open('requirements.txt').read().splitlines()
        )

