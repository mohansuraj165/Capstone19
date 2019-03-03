import pip
from pip._internal import main as pipmain


def install_whl(path):
    pipmain(['install', path])


install_whl('S:\Software\\ujson-1.35-cp36-cp36m-win_amd64.whl')

print('done')
