#!/usr/bin/python
"""
@Author  :  Lijiawei
@Date    :  2023/12/6 7:54 PM
@Desc    :  qa run line.
"""
import os
import pickle

pkl = os.path.join(os.path.dirname(os.path.realpath(__file__)), "qatools.qa")

with open(pkl, "rb") as f:
    mode = pickle.load(f)

if __name__ == "__main__":
    mode()
