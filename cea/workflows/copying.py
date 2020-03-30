"""
This script fills up the scenario parameter matrix with demand values, renewable energy potential and CO2 emissions
"""
from __future__ import division
from __future__ import print_function

import os
import sys

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR))

import tempfile
import xlrd
import shutil

from itertools import compress

def get_input_dir():
    return os.path.join(THIS_DIR, "input")


def get_output_dir():
    output_dir = os.path.join(THIS_DIR, "output")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    return output_dir


def get_filenames(filename, worksheet_num, col_num):
    workbook_path = os.path.join(get_input_dir(), filename)
    excel_workbook = xlrd.open_workbook(workbook_path)
    sheet_with_file_names = excel_workbook.sheet_by_index(worksheet_num)
    file_names = list()
    for cell in sheet_with_file_names.col(col_num):
        val = cell.value
        if val:
            file_names.append(val)

    print("\n found these file-names in excel \n", file_names)
    return file_names


def cleanup(dir):
    shutil.rmtree(dir)


if __name__ == '__main__':
    cleanup(get_output_dir())

    control = [
        ("zone_cr45_15", "zone1", "zones", 0),
        ("zone_cr45_31", "zone2", "zones", 0),
        ("zone_cr45_45", "zone3", "zones", 0),
        ("surroundings_cr45_15", "zone1", "surroundings", 1),
        ("surroundings_cr45_31", "zone2", "surroundings", 1),
        ("surroundings_cr45_45", "zone3", "surroundings", 1),
    ]

    for ctl_params in control:

        str_startswith, zone_folder_id, zone_subfolder, col = ctl_params
        filenames = get_filenames("file_names.xlsx", 2, col)
        mask = [x.startswith(str_startswith) for x in filenames]
        filenames = list(compress(filenames, mask))
        print("copying these files", filenames)
        extenstions = ["shp", "shx", "qpj", "prj", "cpg"]

        tmp = tempfile.mkdtemp()
        for name in filenames:
            for ext in extenstions:
                shutil.copy(os.path.join(get_input_dir(), zone_folder_id, "%s.%s" % (str_startswith, ext)), os.path.join(tmp, "%s.%s" % (name, ext)))

        if os.listdir(tmp).__len__() == len(filenames) * len(extenstions):
            print("files copied correctly, sending to output dir")
            print("copying [%d] files" % os.listdir(tmp).__len__())
            shutil.copytree(tmp, os.path.join(get_output_dir(), zone_folder_id, zone_subfolder))

        cleanup(tmp)
        print("Done!")

