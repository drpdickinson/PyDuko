##########################################################
# (c) Patrick Dickinson, 2022
#
##########################################################

import sodumap

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mymap = sodumap.cSoduMap()
    mymap.Load('kagglepuzzles.txt', 4)
    mymap.Draw()
    mymap.SolveUsingConstrints()
    mymap.ValidityCheck()
    mymap.Draw()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
