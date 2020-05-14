from __future__ import division
from __future__ import print_function
from xlsxwriter import Workbook

import os
import pandas
import numpy


if __name__ == '__main__':
    """simple script to split files output by CEA workflow into analysis matrix"""

    """setup the script parameters"""
    results_file = r'C:\Users\HHM\Desktop\Thesis\Results\results_podium_new_efficiency.xlsx'
    output_file = r'C:\Users\HHM\Desktop\Thesis\Results\output.xls'
    sheet = pandas.read_excel(results_file, "Sheet1")
    major = ["15", "31", "45"]
    minor = [str(i).zfill(2) for i in numpy.arange(4, 26, 2)]
    print("major split: ", major)
    print("minor split: ", minor)

    """create output file"""
    if os.path.exists(output_file):
        os.remove(output_file)

    """extract the different data-frames"""
    result = list()
    for m in major:
        for n in minor:
            mask = sheet.Scenario.str.contains("p_%s_%s_" %(m, n))
            if sum(mask) > 0:
                print("number of records for [p_%s_%s]" %(m, n), sum(mask))
                result.append(sheet[mask])
            else:
                pass

    """write to new workbook"""
    with Workbook(output_file) as excel_file:
        excel_file.add_worksheet('Demand')
        excel_file.add_worksheet('RES')
        excel_file.add_worksheet('CO2')
        excel_file.add_worksheet('PV_generation')
        excel_file.add_worksheet('Demand_A')
        excel_file.add_worksheet('CO2_A')
        sheet_with_demand = excel_file.get_worksheet_by_name('Demand')
        sheet_with_res = excel_file.get_worksheet_by_name('RES')
        sheet_with_co2 = excel_file.get_worksheet_by_name('CO2')
        sheet_with_pv = excel_file.get_worksheet_by_name('PV_generation')
        sheet_with_demand_a = excel_file.get_worksheet_by_name('Demand_A')
        sheet_with_co2_a = excel_file.get_worksheet_by_name('CO2_A')
        number = 0
        for frame in result:
            print("writing results [%i]" %number)
            demand = frame['Demand [kWh/m2]']
            res = frame['RES [%]']
            co2 = frame['CO2_intensity [kg/m2]']
            pv = frame['PV_generation [MWh]']
            demand_a = frame['Demand [MWh]']
            co2_a = frame['CO2 [t]']
            sheet_with_demand.write_column(0, number, demand)
            sheet_with_res.write_column(0, number, res)
            sheet_with_co2.write_column(0, number, co2)
            sheet_with_pv.write_column(0, number, pv)
            sheet_with_demand_a.write_column(0, number, demand_a)
            sheet_with_co2_a.write_column(0, number, co2_a)
            number = number + 1