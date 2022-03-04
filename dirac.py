# dirac.py
# This script takes a .targetcurve file and
# transforms the y values by a constant dB
# and outputs to a new file

import sys
from TargetCurve import TargetCurve, Operation
import numpy as np
import matplotlib.pyplot as plt

try:
    original_file = sys.argv[1]
except Exception:
    print("Error: no filename passed as first argument when running script.")

target_curve = TargetCurve(original_file)
target_curve.transform_breakpoints(Operation.Attenuate, 3, 50, 270)

# Graphing
fig, ax = plt.subplots()
x = [point[0] for point in target_curve.breakpoints_original]
y_original = [point[1] for point in target_curve.breakpoints_original]
y_transformed = [point[1] for point in target_curve.breakpoints_transformed]
plt.plot(x, y_original, marker='o')
plt.plot(x, y_transformed, color='r', marker='*', ms=10, mec='r', mfc='r', alpha=0.2)
plt.xlabel("Frequency")
plt.ylabel("dB")
plt.title("Target Curve modification")
plt.grid(axis='x', which="both", ls="-")
plt.xscale("log")
plt.show()
