"""
This script fills up the scenario parameter matrix with demand values, renewable energy potential and CO2 emissions
"""
from __future__ import division
from __future__ import print_function

import os
import datetime

import xlrd
from xlsxwriter import Workbook
import pandas as pd
import csv
from shutil import copyfile, move
import cea.config
import cea.inputlocator
import cea.scripts

__author__ = "Daren Thomas"
__copyright__ = "Copyright 2019, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Daren Thomas"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


if __name__ == '__main__':
    project_path = r'D:\MVP_Podium\outputs\podium'
    results_file = r'C:\Users\HHM\Desktop\Thesis\Results\results.xlsx'
    scenarios = []
    pv_values = []
    demand_values = []
    demand_values_intensity = []
    res_values = []
    grid_co2_values = []
    co2_values = []
    co2_values_intensity = []
    grid_values = []
    new_sum_grid = []
    #get list of paths to different scenarios
    for scenario in os.listdir(project_path):
        scenarios.append(os.path.join(project_path, scenario))
        scenarios = sorted(scenarios)
    print(scenarios)
    #save needed workbooks
    for scenario in scenarios:
        workbook_demand = os.path.join(scenario, r'outputs\data\demand\Total_demand.csv')
        workbook_pv = os.path.join(scenario, r'outputs\data\potentials\solar\PV_total_buildings.csv')
        workbook_lca = os.path.join(scenario, r'outputs\data\emissions\Total_LCA_operation.csv')

        #read total pv production
        with open(workbook_pv) as pv:
            headerline = pv.next()

            header = headerline.split(",")

            search_for_string = "E_PV_gen_kWh"
            col = header.index(search_for_string)

            sum_pv = 0
            for row in csv.reader(pv):
                sum_pv += float(row[col])/1000 #in MWh
            sum_pv = sum_pv * 2.78
            pv_values.append(sum_pv)
            #print(sum_pv)

        #read total consumption from grid
        with open(workbook_demand) as d:
            headerline = d.next()
            sum_grid = 0
            sum_demand = 0
            for row in csv.reader(d):
                sum_grid += float(row[23])
                sum_demand += float(row[23]) + float(row[139]) #MWh
            grid_values.append(sum_grid)
        res_values.append(sum_pv/sum_demand*100 + 2.9) #in %
        new_sum_grid.append(sum_grid-sum_pv) #in MWh
        grid_co2_values.append((sum_grid-sum_pv)*0.47156) #in ton

        # read co2 from district cooling, area
        with open(workbook_demand) as c:
            headerline = c.next()
            sum_area = 0
            sum_dc_co2 = 0
            for row in csv.reader(c):
                sum_area += float(row[1])
                sum_dc_co2 += float(row[8])

        demand_values.append(sum_demand) #in MWh
        demand_values_intensity.append(sum_demand/sum_area*1000) #in kWh/m2
        co2_values.append((sum_grid-sum_pv)*0.47156 + sum_dc_co2) #in ton
        co2_values_intensity.append(((sum_grid-sum_pv)*0.47156 + sum_dc_co2)/sum_area*1000) #in kg/m2

    print(grid_values)
    print(pv_values)
    print(new_sum_grid)
    print(grid_co2_values)
    print(co2_values)
    print(co2_values_intensity)
    print(demand_values)

#write results into excel file
    results = Workbook(results_file)
    results_sheet = results.add_worksheet()
    results_sheet.write(0, 0, 'Scenario')
    results_sheet.write(0, 1, 'Demand [kWh/m2]')
    results_sheet.write(0, 2, 'RES [%]')
    results_sheet.write(0, 3, 'CO2_intensity [kg/m2]')
    results_sheet.write(0, 4, 'PV_generation [MWh]')
    results_sheet.write(0, 5, 'Demand [MWh]')
    results_sheet.write(0, 6, 'CO2 [t]')
    results_sheet.write_column(1, 0, scenarios)
    results_sheet.write_column(1, 1, demand_values_intensity)
    results_sheet.write_column(1, 2, res_values)
    results_sheet.write_column(1, 3, co2_values_intensity)
    results_sheet.write_column(1, 4, pv_values)
    results_sheet.write_column(1, 5, demand_values)
    results_sheet.write_column(1, 6, co2_values)
    results.close()


    # """Set workbook names"""
    # workbook_names = os.path.join(path, r'file_names.xlsx')
    # excel_names = xlrd.open_workbook(workbook_names)
    # sheet_with_scenarios_names = excel_names.sheet_by_index(1)
    # scenarios_names = sheet_with_scenarios_names.col_values(3)
    # """Get files"""
    # zones_directory = os.path.join(path, r'slab\zones')
    # surroundings_directory = os.path.join(path, r'slab\surroundings')
    # typologies_directory = os.path.join(path, r'slab\typologies_dbf')
    # zone_files = []
    # surroundings_files = []
    # typology_files = []
    # for zone_file in os.listdir(zones_directory):
    #     if zone_file.endswith('.shp'):
    #         zone_files.append(os.path.join(zones_directory, zone_file))
    # zone_files = sorted(zone_files)
    # print(zone_files)
    # for surroundings_file in os.listdir(surroundings_directory):
    #     if surroundings_file.endswith('.shp'):
    #         surroundings_files.append(os.path.join(surroundings_directory, surroundings_file))
    # surroundings_files = sorted(surroundings_files)
    # print(surroundings_files)
    # for typology_file in os.listdir(typologies_directory):
    #     typology_files.append(os.path.join(typologies_directory, typology_file))
    # typology_files = sorted(typology_files)
    # print(typology_files)
    # k = 0
    # for surroundings, zone in zip(surroundings_files, zone_files):
    #     for index, typology in enumerate(typology_files):
    #         if index == 0:
    #         else:
    #         k = k + 1


