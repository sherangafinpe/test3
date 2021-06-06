# -*- coding: utf-8 -*-
"""
Created on Sun May 23 11:21:21 2021

@author: Sheranga
"""

import pandas as pd


def million_or_billion(value,normal=False):

    if normal==True:
        million = 1000000
        billion = 1000000000
        if abs(value/million) <1:
            return 1, ''
        elif abs(value/billion) >=1:
            return billion, ' Billion'
        else:
            return million, " Million"

    else:
        return 1, ""