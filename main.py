##########################################################
# (c) Patrick Dickinson, 2022
#
##########################################################

import sodumap

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mymap = sodumap.cSoduMap()
    mymap.Load()
    mymap.Draw()
    mymap.SolveDeductive()
    mymap.Draw()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
