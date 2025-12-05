#!/usr/bin/env python
# -*- coding: utf-8 -
# Imports:
import numpy as np
import pandas as pd


def fetch_stable_timestamp(dt: float, numsteps: int) -> int:
    """
    Calculates and returns the first stable timestamp, assuming the simulation has stabilized after
    approx. 50 seconds (per conversation with S. Fatemi)

    :return:
    """
    real_time = dt*numsteps

    stable_timestamp = 50*(numsteps/real_time)

    return int(stable_timestamp)



