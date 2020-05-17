"""
This script fills up the scenario parameter matrix with demand values, renewable energy potential and CO2 emissions
"""
from __future__ import division
from __future__ import print_function

import os
import re
import pandas
from xlsxwriter import Workbook
import csv

__author__ = "Daren Thomas"
__copyright__ = "Copyright 2019, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Daren Thomas"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


if __name__ == '__main__':
    project_path = r'D:\MVP_Crosspedestal\outputs'
    results_file = r'C:\Users\HHM\Desktop\pv_results.csv'
    scenarios = []
    pv_roof = []
    pv_walls_E = []
    pv_walls_W = []
    pv_walls_N = []
    pv_walls_S = []
    pv_walls_sum = []



    swidth = [15, 31, 45]
    far = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
    pick_scenario = "01"
    columns = ["PV_roofs_top_E_kWh", "PV_walls_east_E_kWh", "PV_walls_west_E_kWh",
               "PV_walls_north_E_kWh", "PV_walls_south_E_kWh"]
    columns_for_sum = ["PV_walls_east_E_kWh", "PV_walls_west_E_kWh",
               "PV_walls_north_E_kWh", "PV_walls_south_E_kWh"]
    rename_to = ['PV_roofs_top_E_MWh', 'PV_walls_east_E_MWh', 'PV_walls_west_E_MWh',
                 'PV_walls_north_E_MWh', 'PV_walls_south_E_MWh']

    rename_dict = dict(zip(columns, rename_to))
    results = list()
    for sw in swidth:
        for f in far:
            pattern = r'[a-z]{1,}_%s_%s_%s' %(sw, str(f).zfill(2), pick_scenario)
            regex = re.compile(pattern)
            for scenario in os.listdir(project_path):
                if regex.match(scenario):
                    df = pandas.read_csv(os.path.join(project_path, scenario, r'outputs\data\potentials\solar\PV_total_buildings.csv'),
                                         header=0, index_col=0)
                    sums = df.sum(axis=0) / 1e3
                    sums_renamed = sums[columns].rename(rename_dict)
                    sums_renamed["PV_walls_sum"] = sums[columns_for_sum].sum()
                    sums_renamed.name = scenario
                    results.append(sums_renamed)

    output = pandas.concat(results, axis=1)
    output.to_csv(results_file, header=True, index=True)
    print("######################################")
    print("#  wrote output file to %s" %results_file)
    print("######################################\n")
    print(output)
    # output.plot()
    # import matplotlib.pyplot as plt
    # plt.show()
    print("######################################")

    exit(0)

    #get list of paths to different scenarios
    for scenario in os.listdir(project_path):
        scenarios.append(os.path.join(project_path, scenario))
        scenarios = sorted(scenarios)
    print(scenarios)
    #save needed workbooks
    for scenario in scenarios:
        workbook_pv = os.path.join(scenario, r'outputs\data\potentials\solar\PV_total_buildings.csv')
        #read total pv production
        with open(workbook_pv) as pv:
            headerline = pv.next()
            header = headerline.split(",")

            search_for_roof = "PV_roofs_top_E_kWh"
            search_for_walls_E = "PV_walls_east_E_kWh"
            search_for_walls_W = "PV_walls_west_E_kWh"
            search_for_walls_N = "PV_walls_north_E_kWh"
            search_for_walls_S = "PV_walls_south_E_kWh"
            col_roof = header.index(search_for_roof)
            col_E = header.index(search_for_walls_E)
            col_W = header.index(search_for_walls_W)
            col_N = header.index(search_for_walls_N)
            col_S = header.index(search_for_walls_S)

            sum_pv_roof = 0
            sum_pv_E = 0
            sum_pv_W = 0
            sum_pv_N = 0
            sum_pv_S = 0
            sum_walls = 0

            for row in csv.reader(pv):
                sum_pv_roof += float(row[col_roof])/1000 #in MWh
                sum_pv_E += float(row[col_E]) / 1000  # in MWh
                sum_pv_W += float(row[col_W]) / 1000  # in MWh
                sum_pv_N += float(row[col_N]) / 1000  # in MWh
                sum_pv_S += float(row[col_S]) / 1000  # in MWh
            #sum_pv = sum_pv * 2.78
            pv_roof.append(sum_pv_roof)
            pv_walls_E.append(sum_pv_E)
            pv_walls_N.append(sum_pv_N)
            pv_walls_S.append(sum_pv_S)
            pv_walls_W.append(sum_pv_W)
            pv_walls_sum.append(sum_pv_E + sum_pv_N + sum_pv_S + sum_pv_W)
            #print(sum_pv)


    #write results into excel file
    results = Workbook(results_file)
    results_sheet = results.add_worksheet()
    results_sheet.write(0, 0, 'Scenario')
    results_sheet.write(0, 1, 'PV_roofs_top_E_MWh')
    results_sheet.write(0, 2, 'PV_walls_east_E_MWh')
    results_sheet.write(0, 3, 'PV_walls_west_E_MWh')
    results_sheet.write(0, 4, 'PV_walls_south_E_MWh')
    results_sheet.write(0, 5, 'PV_walls_north_E_MWh')
    results_sheet.write(0, 6, 'PV_walls_sum')
    results_sheet.write_column(1, 0, scenarios)
    results_sheet.write_column(1, 1, pv_roof)
    results_sheet.write_column(1, 2, pv_walls_E)
    results_sheet.write_column(1, 3, pv_walls_W)
    results_sheet.write_column(1, 4, pv_walls_S)
    results_sheet.write_column(1, 5, pv_walls_N)
    results_sheet.write_column(1, 6, pv_walls_sum)
    results.close()



