from os.path import exists
from enum import Enum


class Operation(Enum):
    Gain = 1
    Attenuate = 2
    Compress = 3
    Expand = 4
    Limit = 5


class TargetCurve:
    def __init__(self, filename):
        self.breakpoints_original = []
        self.breakpoints_transformed = []
        self.name = ""
        self.device_name = ""
        self.low_limit_Hz = 0
        self.high_limit_Hz = 40000
        
        self.parse_file(filename)
    
    def parse_file(self, filename):
        try:
            exists(filename)
            print("Loading file:", filename)
        except Exception:
            print("Error: file not found")
        
        with open(filename) as f:
            lines = f.read().splitlines()
            self.name = lines[1]
            self.device_name = lines[3]
            breakpoints_first = 5
            breakpoints_last = lines.index("LOWLIMITHZ", breakpoints_first)
            for coord in lines[breakpoints_first:breakpoints_last]:
                self.breakpoints_original.append([float(x) for x in coord.split()])
            
            self.low_limit_Hz = lines[breakpoints_last + 1]
            self.high_limit_Hz = lines[breakpoints_last + 3]
    
    def description(self):
        print(
            "------------------------\nName: %s\nDevice Name: %s\nLow Limit: %s Hz\nHigh Limit: %s Hz\nBreakpoints (%i): %s\n------------------------" % (
            self.name, self.device_name, self.low_limit_Hz, self.high_limit_Hz, len(self.breakpoints_original),
            self.breakpoints_original))
    
    def transform_breakpoints(self, operation: Operation, dB_change, bandpass_low_freq=None, bandpass_high_freq=None):
        if bandpass_low_freq is None:
            bandpass_low_freq = self.low_limit_Hz
        if bandpass_high_freq is None:
            bandpass_high_freq = self.high_limit_Hz
        
        if operation == Operation.Gain:
            transform = lambda p: [p[0], p[1] + abs(dB_change)] if (
                        p[0] >= float(bandpass_low_freq) and p[0] <= float(bandpass_high_freq)) else p
        elif operation == Operation.Attenuate:
            transform = lambda p: [p[0], p[1] - abs(dB_change)] if (
                        p[0] >= float(bandpass_low_freq) and p[0] <= float(bandpass_high_freq)) else p
        elif operation == Operation.Compress:
            transform = lambda p: [p[0], p[1] * (100 - dB_change)/100] if (
                        p[0] >= float(bandpass_low_freq) and p[0] <= float(bandpass_high_freq)) else p
        elif operation == Operation.Expand:
            transform = lambda p: [p[0], p[1] * (100 + dB_change)/100] if (
                        p[0] >= float(bandpass_low_freq) and p[0] <= float(bandpass_high_freq)) else p
        elif operation == Operation.Limit:
            transform = lambda p: [p[0], dB_change if p[1] >= dB_change else p[1]] if (
                p[0] >= float(bandpass_low_freq) and p[0] <= float(bandpass_high_freq)) else p
        
        self.breakpoints_transformed = [transform(p) for p in self.breakpoints_original]

    def write_transformed(self, target_filename):
        text = "NAME\n%s\nDEVICENAME\n%s\nBREAKPOINTS\n" % (self.name, self.device_name)
        for point in self.breakpoints_transformed:
            text += "%s %s\n" % (str(point[0]), str(point[1]))
        text += "LOWLIMITHZ\n%s\nHIGHLIMITHZ\n%s\n" % (str(self.low_limit_Hz), str(self.high_limit_Hz))
        
        with open(target_filename, 'w') as f:
            f.write(text)
            f.close()
            print("File saved to %s" % target_filename)
