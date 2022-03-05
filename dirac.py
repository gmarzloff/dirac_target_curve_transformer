# dirac.py
# This script takes a .targetcurve file and
# transforms the y values by a constant dB
# and outputs to a new file

import sys
from TargetCurve import TargetCurve, Operation
import matplotlib.pyplot as plt

target_curve = None

def main():
    try:
        original_file = sys.argv[1]
        
    except Exception:
        print("Error: no filename passed as first argument when running script.")
    
    global target_curve
    target_curve = TargetCurve(original_file)
    
    
    while True:
        choice = pick_menu_options()
        if choice <= 5:
            low = float(input("Low Frequency cutoff for transformation (Hz) [0 Hz]:") or 0)
            high = float(input("High Frequency cutoff for transformation (Hz) [20 kHz]:") or 20000)
        
        if choice == Operation.Gain.value:
            value = float(input("Gain by __ dB [0]:"))
            target_curve.transform_breakpoints(Operation.Gain, value, low, high)
        elif choice == Operation.Attenuate.value:
            value = float(input("Attenuate by __ dB [0]:"))
            target_curve.transform_breakpoints(Operation.Attenuate, value, low, high)
        elif choice == Operation.Compress.value:
            value = float(input("Compression by __ % [0] (e.g. '10' = 90% output:"))
            target_curve.transform_breakpoints(Operation.Compress, value, low, high)
        elif choice == Operation.Expand.value:
            value = float(input("Expansion by __ % [0] (e.g. '10' = 110% output:"))
            target_curve.transform_breakpoints(Operation.Expand, value, low, high)
        elif choice == Operation.Limit.value:
            value = float(input("Limit using ceiling  __ dB:"))
            target_curve.transform_breakpoints(Operation.Limit, value, low, high)
        elif choice == 6:
            print("Close graph window to continue.")
            graph()
        elif choice == 7:
            if len(target_curve.breakpoints_transformed) == 0:
                print("No transformation done yet! Nothing to write.")
            else:
                default_filename = original_file[0:-12] + "_transformed.targetcurve"
                output_file = str(input("Target filename: [%s]" % default_filename)) or default_filename
                target_curve.write_transformed(output_file)
        elif choice == 8:
            sys.exit()
    
def pick_menu_options():
    options_str = "\nChoose Target curve Modification:\n" \
                  "1. Gain\n" \
                  "2. Attenuate\n" \
                  "3. Compress\n" \
                  "4. Expand\n" \
                  "5. Limit\n" \
                  "6. Graph\n" \
                  "7. Write to new .targetcurve file\n" \
                  "8. Quit\n\n"
    return int(input(options_str))

    
def graph():
    global target_curve
    
    fig, ax = plt.subplots()
    x = [point[0] for point in target_curve.breakpoints_original]
    y_original = [point[1] for point in target_curve.breakpoints_original]
    y_transformed = [point[1] for point in target_curve.breakpoints_transformed]
    plt.plot(x, y_original, marker='o', alpha=0.2, label="Original")
    plt.plot(x, y_transformed, color='r', marker='*', ms=10, mec='r', mfc='r', label="Transformed")
    plt.xlabel("Frequency")
    plt.ylabel("dB")
    plt.title("Target Curve")
    plt.grid(axis='x', which="both", ls="-")
    plt.xscale("log")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
