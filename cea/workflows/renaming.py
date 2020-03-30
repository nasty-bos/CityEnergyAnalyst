from __future__ import division
from __future__ import print_function

import os
import sys

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR))

def get_input_dir():
    return os.path.join(THIS_DIR, "input")


def get_output_dir():
    output_dir = os.path.join(THIS_DIR, "output")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    return output_dir


if __name__ == '__main__':

    directory = os.path.join(get_input_dir(), "renaming", "zones")
    files = os.listdir(directory)
    for file in files:
        os.rename(os.path.join(directory, file), os.path.join(directory, file.replace("_s_", "_c_")))
    print("Done!")
