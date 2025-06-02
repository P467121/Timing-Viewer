import wmi
from read import read_timing
MCHBAR = 0xFEDC0000
MCHBAR2 = 0xFEDD0000
def get_command_rate():
    """Returns the Command Rate (1N, 2N, 3N, or N:X) based on CMD Stretch and N to 1 Ratio."""
    try:
        cmd_stretch = read_timing(
            MCHBAR + 0xE088,
            bit_start=3,
            bit_length=2,
            read_type="standard"
        )
        if cmd_stretch is None:
            return "Unknown"
        if cmd_stretch == 0:
            return "1N"
        elif cmd_stretch == 1:
            return "2N"
        elif cmd_stretch == 2:
            return "3N"
        elif cmd_stretch == 3:
            n_to_1_ratio = read_timing(
                MCHBAR + 0xE088,
                bit_start=5,
                bit_length=3,
                read_type="standard"
            )
            if n_to_1_ratio is None:
                return "N:Unknown"
            return f"N:{n_to_1_ratio}"
        else:
            return "Unknown"
    except Exception as e:
        return "Error"
def get_tWTRL():
    """Returns tWTR_S timing calculated as tWRRD_dg - tCWL - 10."""
    try:
        tWRRDSG = read_timing(
            MCHBAR + 0xE014,
            bit_start=0,
            bit_length=7,
            read_type="standard"
        )
        tCWL = read_timing(
            MCHBAR + 0xE070,
            bit_start=24,
            bit_length=7,
            read_type="standard"
        )
        tWTRL = tWRRDSG - tCWL - 6
        return tWTRL
    except Exception as e:
        return "Error"
def get_tWTRS():
    """Returns tWTR_S timing calculated as tWRRD_dg - tCWL - 10."""
    try:
        tWRRDDG = read_timing(
            MCHBAR + 0xE014,
            bit_start=9,
            bit_length=7,
            read_type="standard"
        )
        tCWL = read_timing(
            MCHBAR + 0xE070,
            bit_start=24,
            bit_length=7,
            read_type="standard"
        )
        tWTRS = tWRRDDG - tCWL - 6
        return tWTRS
    except Exception as e:
        return "Error"
def detect_dual_channel_memory():
    try:
        w = wmi.WMI()
        memory_arrays = w.Win32_PhysicalMemoryArray()
        if not memory_arrays:
            return "No memory array detected"
        num_slots = memory_arrays[0].MemoryDevices
        used_slots = set(memory.Tag for memory in w.Win32_PhysicalMemory())
        if num_slots == 2:
            if {"Physical Memory 0", "Physical Memory 1"}.issubset(used_slots):
                return "Dual Channel"
            else:
                return "Single Channel"
        elif num_slots == 4:
            a_slots = {"Physical Memory 3", "Physical Memory 2"}
            b_slots = {"Physical Memory 1", "Physical Memory 0"}
            a_used = a_slots & used_slots
            b_used = b_slots & used_slots
            if a_used and b_used:
                return "Dual Channel"
            else:
                return "Single Channel"
        else:
            return f"{num_slots} DIMM slots detected - Unknown Channel Layout"
    except Exception as e:
        return f"Error detecting memory layout: {e}"
def get_cpu_name():
    try:
        w = wmi.WMI()
        cpu = w.Win32_Processor()[0]
        cpu_name = cpu.Name.replace("Processor", "").strip()
        return cpu_name
    except Exception as e:
        print(f"Error retrieving CPU name: {e}")
        return "Error"
def get_total_physical_memory():
    try:
        w = wmi.WMI()
        computer_system = w.Win32_ComputerSystem()[0]
        memory_bytes = int(computer_system.TotalPhysicalMemory)
        memory_gb = round(memory_bytes / (1024 ** 3))
        return f"{memory_gb}GB"
    except Exception as e:
        print(f"Error retrieving physical memory size: {e}")
        return "Error"
def get_motherboard_name():
    try:
        w = wmi.WMI()
        motherboard = w.Win32_BaseBoard()[0]
        return motherboard.Product
    except Exception as e:
        print(f"Error retrieving motherboard name: {e}")
        return "Unknown"
MCHBAR = 0xFEDC0000
MCHBAR2 = 0xFEDD0000
MULTIPLIER_FORMULA = {
    0: "133.33",
    1: "100",
}

DFE_ENABLE_FORMULA = {
    0: "ON",
    1: "OFF",
}
DFE_TAP_ENABLE_FORMULA = {
    0: "OFF",
    1: "ON",
}
DFE_GAIN_FORMULA ={
    0: "0",
    1: "1",
    2: "2",
    3: "3",
    4: "RFU",
    5: "RFU",
    6: "RFU",
    7: "RFU",
    8: "-0",
    9: "-1",
    10: "-2",
    11: "-3",
    12: "RFU",
    13: "RFU",
    14: "RFU",
    15: "RFU"
}

DFE_TAP_FORMULA ={
    0: "RZQ/7 (34)",
    1: "RZQ/6 (40)",
    2: "RZQ/5 (48)",
    3: "RFU",
    4: "RZQ/7 (34)",
    5: "RZQ/6 (40)",
    6: "RZQ/5 (48)",
    7: "RFU",
    8: "RZQ/7 (34)",
    9: "RZQ/6 (40)",
    10: "RZQ/5 (48)",
    11: "RFU",
    12: "RZQ/7 (34)",
    13: "RZQ/6 (40)",
    14: "RZQ/5 (48)",
    15: "RFU"
}

RON_FORMULA ={
    0: "RZQ/7 (34)",
    1: "RZQ/6 (40)",
    2: "RZQ/5 (48)",
    3: "RFU"
}
GEAR_MODE_FORMULA = {
    0: "Gear Mode 1",
    1: "Gear Mode 2",
    2: "Gear Mode 4"
}
REFRESH_MODE_FORMULA = {
    0: "Normal Refresh (tRFC)",
    1: "FGR Mode (tRFC2)",
}
tCCD_L_FORMULA = {
    0: "8",
    1: "9",
    2: "10",
    3: "11",
    4: "12",
    5: "13",
    6: "14",
    7: "15",
    8: "16",
    9: "Reserved",
    10: "Reserved",
    11: "Reserved",
    12: "Reserved",
    13: "Reserved",
    14: "Reserved",
    15: "Reserved",
}
tCCD_L_WR_FORMULA = {
    0: "32",
    1: "36",
    2: "40",
    3: "44",
    4: "48",
    5: "52",
    6: "56",
    7: "60",
    8: "64",
    9: "Reserved",
    10: "Reserved",
    11: "Reserved",
    12: "Reserved",
    13: "Reserved",
    14: "Reserved",
    15: "Reserved",
}
DFE_TAP1_FORMULA = {
    0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 
    8: "8", 9: "9", 10: "10", 11: "11", 12: "12", 13: "13", 14: "14", 15: "15", 
    16: "16", 17: "17", 18: "18", 19: "19", 20: "20", 21: "21", 22: "22", 23: "23", 
    24: "24", 25: "25", 26: "26", 27: "27", 28: "28", 29: "29", 30: "30", 31: "31", 
    32: "32", 33: "33", 34: "34", 35: "35", 36: "36", 37: "37", 38: "38", 39: "39", 
    40: "40", 41: "RFU", 42: "RFU", 43: "RFU", 44: "RFU", 45: "RFU", 46: "RFU", 
    47: "RFU", 48: "RFU", 49: "RFU", 50: "RFU", 51: "RFU", 52: "RFU", 53: "RFU", 
    54: "RFU", 55: "RFU", 56: "RFU", 57: "RFU", 58: "RFU", 59: "RFU", 60: "RFU", 
    61: "RFU", 62: "RFU", 63: "RFU", 64: "0", 65: "-1", 66: "-2", 67: "-3", 68: "-4", 
    69: "-5", 70: "-6", 71: "-7", 72: "-8", 73: "-9", 74: "-10", 75: "-11", 76: "-12", 
    77: "-13", 78: "-14", 79: "-15", 80: "-16", 81: "-17", 82: "-18", 83: "-19", 
    84: "-20", 85: "-21", 86: "-22", 87: "-23", 88: "-24", 89: "-25", 90: "-26", 
    91: "-27", 92: "-28", 93: "-29", 94: "-30", 95: "-31", 96: "-32", 97: "-33", 
    98: "-34", 99: "-35", 100: "-36", 101: "-37", 102: "-38", 103: "-39", 
    104: "-40", 105: "RFU", 106: "RFU", 107: "RFU", 108: "RFU", 109: "RFU", 
    110: "RFU", 111: "RFU", 112: "RFU", 113: "RFU", 114: "RFU", 115: "RFU", 
    116: "RFU", 117: "RFU", 118: "RFU", 119: "RFU", 120: "RFU", 121: "RFU", 
    122: "RFU", 123: "RFU", 124: "RFU", 125: "RFU", 126: "RFU", 127: "RFU"
}

DFE_TAP2_FORMULA = {
    0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7",
    8: "8", 9: "9", 10: "10", 11: "11", 12: "12", 13: "13", 14: "14", 15: "15",
    16: "RFU", 17: "RFU", 18: "RFU", 19: "RFU", 20: "RFU", 21: "RFU", 22: "RFU", 23: "RFU",
    24: "RFU", 25: "RFU", 26: "RFU", 27: "RFU", 28: "RFU", 29: "RFU", 30: "RFU", 31: "RFU",
    32: "RFU", 33: "RFU", 34: "RFU", 35: "RFU", 36: "RFU", 37: "RFU", 38: "RFU", 39: "RFU",
    40: "RFU", 41: "RFU", 42: "RFU", 43: "RFU", 44: "RFU", 45: "RFU", 46: "RFU", 47: "RFU",
    48: "RFU", 49: "RFU", 50: "RFU", 51: "RFU", 52: "RFU", 53: "RFU", 54: "RFU", 55: "RFU",
    56: "RFU", 57: "RFU", 58: "RFU", 59: "RFU", 60: "RFU", 61: "RFU", 62: "RFU", 63: "RFU",
    64: "0", 65: "-1", 66: "-2", 67: "-3", 68: "-4", 69: "-5", 70: "-6", 71: "-7",
    72: "-8", 73: "-9", 74: "-10", 75: "-11", 76: "-12", 77: "-13", 78: "-14", 79: "-15",
    80: "RFU", 81: "RFU", 82: "RFU", 83: "RFU", 84: "RFU", 85: "RFU", 86: "RFU", 87: "RFU",
    88: "RFU", 89: "RFU", 90: "RFU", 91: "RFU", 92: "RFU", 93: "RFU", 94: "RFU", 95: "RFU",
    96: "RFU", 97: "RFU", 98: "RFU", 99: "RFU", 100: "RFU", 101: "RFU", 102: "RFU", 103: "RFU",
    104: "RFU", 105: "RFU", 106: "RFU", 107: "RFU", 108: "RFU", 109: "RFU", 110: "RFU", 111: "RFU",
    112: "RFU", 113: "RFU", 114: "RFU", 115: "RFU", 116: "RFU", 117: "RFU", 118: "RFU", 119: "RFU",
    120: "RFU", 121: "RFU", 122: "RFU", 123: "RFU", 124: "RFU", 125: "RFU", 126: "RFU", 127: "RFU",
}

DFE_TAP3_FORMULA = {
    0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9",
    10: "10", 11: "11", 12: "12",
    13: "RFU", 14: "RFU", 15: "RFU",
    16: "RFU", 17: "RFU", 18: "RFU", 19: "RFU", 20: "RFU", 21: "RFU", 22: "RFU", 23: "RFU",
    24: "RFU", 25: "RFU", 26: "RFU", 27: "RFU", 28: "RFU", 29: "RFU", 30: "RFU", 31: "RFU",
    32: "RFU", 33: "RFU", 34: "RFU", 35: "RFU", 36: "RFU", 37: "RFU", 38: "RFU", 39: "RFU",
    40: "RFU", 41: "RFU", 42: "RFU", 43: "RFU", 44: "RFU", 45: "RFU", 46: "RFU", 47: "RFU",
    48: "RFU", 49: "RFU", 50: "RFU", 51: "RFU", 52: "RFU", 53: "RFU", 54: "RFU", 55: "RFU",
    56: "RFU", 57: "RFU", 58: "RFU", 59: "RFU", 60: "RFU", 61: "RFU", 62: "RFU", 63: "RFU",
    64: "0", 65: "-1", 66: "-2", 67: "-3", 68: "-4", 69: "-5", 70: "-6", 71: "-7",
    72: "-8", 73: "-9", 74: "-10", 75: "-11", 76: "-12",
    77: "RFU", 78: "RFU", 79: "RFU",
    80: "RFU", 81: "RFU", 82: "RFU", 83: "RFU", 84: "RFU", 85: "RFU", 86: "RFU", 87: "RFU",
    88: "RFU", 89: "RFU", 90: "RFU", 91: "RFU", 92: "RFU", 93: "RFU", 94: "RFU", 95: "RFU",
    96: "RFU", 97: "RFU", 98: "RFU", 99: "RFU", 100: "RFU", 101: "RFU", 102: "RFU", 103: "RFU",
    104: "RFU", 105: "RFU", 106: "RFU", 107: "RFU", 108: "RFU", 109: "RFU", 110: "RFU", 111: "RFU",
    112: "RFU", 113: "RFU", 114: "RFU", 115: "RFU", 116: "RFU", 117: "RFU", 118: "RFU", 119: "RFU",
    120: "RFU", 121: "RFU", 122: "RFU", 123: "RFU", 124: "RFU", 125: "RFU", 126: "RFU", 127: "RFU",
}

DFE_TAP4_FORMULA = {
    0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9",
    10: "RFU", 11: "RFU", 12: "RFU", 13: "RFU", 14: "RFU", 15: "RFU",
    16: "RFU", 17: "RFU", 18: "RFU", 19: "RFU", 20: "RFU", 21: "RFU", 22: "RFU", 23: "RFU",
    24: "RFU", 25: "RFU", 26: "RFU", 27: "RFU", 28: "RFU", 29: "RFU", 30: "RFU", 31: "RFU",
    32: "RFU", 33: "RFU", 34: "RFU", 35: "RFU", 36: "RFU", 37: "RFU", 38: "RFU", 39: "RFU",
    40: "RFU", 41: "RFU", 42: "RFU", 43: "RFU", 44: "RFU", 45: "RFU", 46: "RFU", 47: "RFU",
    48: "RFU", 49: "RFU", 50: "RFU", 51: "RFU", 52: "RFU", 53: "RFU", 54: "RFU", 55: "RFU",
    56: "RFU", 57: "RFU", 58: "RFU", 59: "RFU", 60: "RFU", 61: "RFU", 62: "RFU", 63: "RFU",
    64: "0", 65: "-1", 66: "-2", 67: "-3", 68: "-4", 69: "-5", 70: "-6", 71: "-7", 72: "-8", 73: "-9",
    74: "RFU", 75: "RFU", 76: "RFU", 77: "RFU", 78: "RFU", 79: "RFU",
    80: "RFU", 81: "RFU", 82: "RFU", 83: "RFU", 84: "RFU", 85: "RFU", 86: "RFU", 87: "RFU",
    88: "RFU", 89: "RFU", 90: "RFU", 91: "RFU", 92: "RFU", 93: "RFU", 94: "RFU", 95: "RFU",
    96: "RFU", 97: "RFU", 98: "RFU", 99: "RFU", 100: "RFU", 101: "RFU", 102: "RFU", 103: "RFU",
    104: "RFU", 105: "RFU", 106: "RFU", 107: "RFU", 108: "RFU", 109: "RFU", 110: "RFU", 111: "RFU",
    112: "RFU", 113: "RFU", 114: "RFU", 115: "RFU", 116: "RFU", 117: "RFU", 118: "RFU", 119: "RFU",
    120: "RFU", 121: "RFU", 122: "RFU", 123: "RFU", 124: "RFU", 125: "RFU", 126: "RFU", 127: "RFU",
}

CA_ODT_FORMULA = {
    0: "RTT_OFF",
    1: "RZQ/0.5 (480)",
    2: "RZQ/1 (240)",
    3: "RZQ/2 (120)",
    4: "RZQ/3 (80)",
    5: "RZQ/4 (60)",
    6: "RFU",
    7: "RZQ/6 (40)"
}
CA_ODT_FORMULA = {
    0: "RTT_OFF",
    1: "RZQ/0.5 (480)",
    2: "RZQ/1 (240)",
    3: "RZQ/2 (120)",
    4: "RZQ/3 (80)",
    5: "RZQ/4 (60)",
    6: "RFU",
    7: "RZQ/6 (40)"
}
CS_ODT_FORMULA = {
    0: "RTT_OFF",
    1: "RZQ/0.5 (480)",
    2: "RZQ/1 (240)",
    3: "RZQ/2 (120)",
    4: "RZQ/3 (80)",
    5: "RZQ/4 (60)",
    6: "RFU",
    7: "RZQ/6 (40)"
}
CK_ODT_FORMULA = {
    0: "RTT_OFF",
    1: "RZQ/0.5 (480)",
    2: "RZQ/1 (240)",
    3: "RZQ/2 (120)",
    4: "RZQ/3 (80)",
    5: "RZQ/4 (60)",
    6: "RFU",
    7: "RZQ/6 (40)"
}
DQS_RTT_PARK_FORMULA = {
    0: "RTT_OFF",
    1: "RZQ (240)",
    2: "RZQ/2 (120)",
    3: "RZQ/3 (80)",
    4: "RZQ/4 (60)",
    5: "RZQ/5 (48)",
    6: "RZQ/6 (40)",
    7: "RZQ/7 (34)"
}
RTT_PARK_FORMULA = {
    0: "RTT_OFF",
    1: "RZQ (240)",
    2: "RZQ/2 (120)",
    3: "RZQ/3 (80)",
    4: "RZQ/4 (60)",
    5: "RZQ/5 (48)",
    6: "RZQ/6 (40)",
    7: "RZQ/7 (34)"
}
RTT_WR_FORMULA = {
    0: "RTT_OFF",
    1: "RZQ (240)",
    2: "RZQ/2 (120)",
    3: "RZQ/3 (80)",
    4: "RZQ/4 (60)",
    5: "RZQ/5 (48)",
    6: "RZQ/6 (40)",
    7: "RZQ/7 (34)"
}
RTT_NOM_WR_FORMULA = {
    0: "RTT_OFF",
    1: "RZQ (240)",
    2: "RZQ/2 (120)",
    3: "RZQ/3 (80)",
    4: "RZQ/4 (60)",
    5: "RZQ/5 (48)",
    6: "RZQ/6 (40)",
    7: "RZQ/7 (34)"
}
tWR_FORMULA = {
    0: 48,
    1: 54,
    2: 60,
    3: 66,
    4: 72,
    5: 78,
    6: 84,
    7: 90,
    8: 96
}
RTT_NOM_RD_FORMULA = {
    0: "RTT_OFF",
    1: "RZQ (240)",
    2: "RZQ/2 (120)",
    3: "RZQ/3 (80)",
    4: "RZQ/4 (60)",
    5: "RZQ/5 (48)",
    6: "RZQ/6 (40)",
    7: "RZQ/7 (34)"
}
RTT_Loopback_FORMULA = {
    0: "RTT_OFF",
    1: "RFU",
    2: "RFU",
    3: "RFU",
    4: "RFU",
    5: "RZQ/5 (48)",
    6: "RFU",
    7: "RFU"
}
ODTL_ON_WR = {
    0: "RFU",
    1: "-4 Clocks",
    2: "-3 Clocks",
    3: "-2 Clocks",
    4: "-1 Clock",
    5: "0 Clocks",
    6: "+1 Clock",
    7: "+2 Clocks"
}
ODTL_OFF_WR = {
    0: "RFU",
    1: "4 Clocks",
    2: "3 Clocks",
    3: "2 Clocks",
    4: "1 Clock",
    5: "0 Clocks",
    6: "-1 Clock",
    7: "-2 Clocks"
}
ODTL_ON_WR_NT = {
    0: "RFU",
    1: "-4 Clocks",
    2: "-3 Clocks",
    3: "-2 Clocks",
    4: "-1 Clock",
    5: "0 Clocks",
    6: "+1 Clock",
    7: "+2 Clocks"
}
ODTL_OFF_WR_NT = {
    0: "RFU",
    1: "4 Clocks",
    2: "3 Clocks",
    3: "2 Clocks",
    4: "1 Clock",
    5: "0 Clocks",
    6: "-1 Clock",
    7: "-2 Clocks"
}
ODTL_ON_RD_NT = {
    0: "RFU",
    1: "RFU",
    2: "-3 Clocks",
    3: "-2 Clocks",
    4: "-1 Clock",
    5: "0 Clocks",
    6: "+1 Clock",
    7: "RFU"
}
ODTL_OFF_RD_NT = {
    0: "RFU",
    1: "RFU",
    2: "+3 Clocks",
    3: "+2 Clocks",
    4: "+1 Clock",
    5: "0 Clocks",
    6: "-1 Clock",
    7: "RFU"
}
EN_DIS_FORMULA = {
    0: "Disabled",
    1: "Enabled"
}
VREF_FORMULA = {
    0: "97.5%", 1: "97.0%", 2: "96.5%", 3: "96.0%", 4: "95.5%", 5: "95.0%", 6: "94.5%", 7: "94.0%", 8: "93.5%", 9: "93.0%",
    10: "92.5%", 11: "92.0%", 12: "91.5%", 13: "91.0%", 14: "90.5%", 15: "90.0%", 16: "89.5%", 17: "89.0%", 18: "88.5%", 19: "88.0%",
    20: "87.5%", 21: "87.0%", 22: "86.5%", 23: "86.0%", 24: "85.5%", 25: "85.0%", 26: "84.5%", 27: "84.0%", 28: "83.5%", 29: "83.0%",
    30: "82.5%", 31: "82.0%", 32: "81.5%", 33: "81.0%", 34: "80.5%", 35: "80.0%", 36: "79.5%", 37: "79.0%", 38: "78.5%", 39: "78.0%",
    40: "77.5%", 41: "77.0%", 42: "76.5%", 43: "76.0%", 44: "75.5%", 45: "75.0%", 46: "74.5%", 47: "74.0%", 48: "73.5%", 49: "73.0%",
    50: "72.5%", 51: "72.0%", 52: "71.5%", 53: "71.0%", 54: "70.5%", 55: "70.0%", 56: "69.5%", 57: "69.0%", 58: "68.5%", 59: "68.0%",
    60: "67.5%", 61: "67.0%", 62: "66.5%", 63: "66.0%", 64: "65.5%", 65: "65.0%", 66: "64.5%", 67: "64.0%", 68: "63.5%", 69: "63.0%",
    70: "62.5%", 71: "62.0%", 72: "61.5%", 73: "61.0%", 74: "60.5%", 75: "60.0%", 76: "59.5%", 77: "59.0%", 78: "58.5%", 79: "58.0%",
    80: "57.5%", 81: "57.0%", 82: "56.5%", 83: "56.0%", 84: "55.5%", 85: "55.0%", 86: "54.5%", 87: "54.0%", 88: "53.5%", 89: "53.0%",
    90: "52.5%", 91: "52.0%", 92: "51.5%", 93: "51.0%", 94: "50.5%", 95: "50.0%", 96: "49.5%", 97: "49.0%", 98: "48.5%", 99: "48.0%",
    100: "47.5%", 101: "47.0%", 102: "46.5%", 103: "46.0%", 104: "45.5%", 105: "45.0%", 106: "44.5%", 107: "44.0%", 108: "43.5%", 109: "43.0%",
    110: "42.5%", 111: "42.0%", 112: "41.5%", 113: "41.0%", 114: "40.5%", 115: "40.0%", 116: "39.5%", 117: "39.0%", 118: "38.5%", 119: "38.0%",
    120: "37.5%", 121: "37.0%", 122: "36.5%", 123: "36.0%", 124: "35.5%", 125: "35.0%",
}
TIMINGS = [
    {"name": "CPU", "value": get_cpu_name(), "Category": "General", "Tab": "Timings", "Column": "Left", "read_type": "standard"},
    {"name": "Motherboard", "value": get_motherboard_name(), "Category": "General", "Tab": "Timings", "Column": "Left", "read_type": "standard"},
    {"name": "Capacity", "value": get_total_physical_memory(), "Category": "General", "Tab": "Timings", "Column": "Left", "read_type": "standard"},
    {"name": "Speed", "value": None, "Category": "General", "Tab": "Timings", "Column": "Left", "read_type": "standard"},
    {"name": "Dram Ratio", "address": MCHBAR + 0x5E04, "Category": "General", "Tab": "Timings", "parameters": {"bit_start": 0, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "Multiplier", "address": MCHBAR + 0x5E04, "Category": "General", "Tab": "Timings", "parameters": {"bit_start": 8, "bit_length": 4}, "Column": "Left", "Formula": MULTIPLIER_FORMULA, "read_type": "standard"},
    {"name": "Gear Mode", "address": MCHBAR + 0x5E04, "Category": "General", "Tab": "Timings", "parameters": {"bit_start": 12, "bit_length": 2}, "Column": "Left", "Formula": GEAR_MODE_FORMULA, "read_type": "standard"},
    {"name": "Channels", "value": detect_dual_channel_memory(), "Category": "General", "Tab": "Timings", "parameters": {}, "Column": "Left", "read_type": "standard"},
    {"name": "tCL", "address": MCHBAR + 0xE070, "Category": "Primary", "Tab": "Timings", "parameters": {"bit_start": 16, "bit_length": 7}, "Column": "Left", "read_type": "standard"},
    {"name": "tRCD", "address": MCHBAR + 0xE004, "Category": "Primary", "Tab": "Timings", "parameters": {"bit_start": 19, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "tRCDW", "address": MCHBAR + 0xE000, "Category": "Primary", "Tab": "Timings", "parameters": {"bit_start": 24, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "tRP", "address": MCHBAR + 0xE000, "Category": "Primary", "Tab": "Timings", "parameters": {"bit_start": 0, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "tRAS", "address": MCHBAR + 0xE004, "Category": "Primary", "Tab": "Timings", "parameters": {"bit_start": 10, "bit_length": 9}, "Column": "Left", "read_type": "standard"},
    {"name": "Command Rate", "value": get_command_rate(), "Category": "Primary", "Tab": "Timings", "parameters": {}, "Column": "Left", "read_type": "standard"},
    {"name": "tRRDS", "address": MCHBAR + 0xE008, "Category": "Secondary", "Tab": "Timings", "parameters": {"bit_start": 9, "bit_length": 6}, "Column": "Left", "read_type": "standard"},
    {"name": "tRRDL", "address": MCHBAR + 0xE008, "Category": "Secondary", "Tab": "Timings", "parameters": {"bit_start": 15, "bit_length": 7}, "Column": "Left", "read_type": "standard"},
    {"name": "tRFC", "address": MCHBAR + 0xE43C, "Category": "Secondary", "Tab": "Timings", "parameters": {"bit_start": 18, "bit_length": 13}, "Column": "Left", "read_type": "standard"},
    {"name": "tRFCpb", "address": MCHBAR + 0xE488, "Category": "Secondary", "Tab": "Timings", "parameters": {"bit_start": 10, "bit_length": 11}, "Column": "Left", "read_type": "standard"},
    {"name": "tREFI", "address": MCHBAR + 0xE43C, "Category": "Secondary", "Tab": "Timings", "parameters": {"bit_start": 0, "bit_length": 18}, "Column": "Left", "read_type": "standard"},
    {"name": "tWR", "Category": "Secondary", "Tab": "Timings", "Column": "Left", "read_type": "dynamic", "dynamic_params": {"offset_start": 0xE600, "value_to_find": 0x06, "offset_base": 0xE200, "bit_start_dynamic": 0, "bit_length_dynamic": 4, "mchbar": 0xFEDC0000, "command": 0, "offset2": 0,}, "Formula": tWR_FORMULA},
    {"name": "tRTP", "address": MCHBAR + 0xE000, "Category": "Secondary", "Tab": "Timings", "parameters": {"bit_start": 13, "bit_length": 7}, "Column": "Left", "read_type": "standard"},
    {"name": "tFAW", "address": MCHBAR + 0xE008, "Category": "Secondary", "Tab": "Timings", "parameters": {"bit_start": 0, "bit_length": 9}, "Column": "Left", "read_type": "standard"},
    {
        "name": "tWTRS",
        "value": get_tWTRS(),  
        "Category": "Secondary",
        "Tab": "Timings",
        "parameters": {},
        "Column": "Left",
        "read_type": "standard"
    },
    {
        "name": "tWTRL",
        "value": get_tWTRL(),  
        "Category": "Secondary",
        "Tab": "Timings",
        "parameters": {},
        "Column": "Left",
        "read_type": "standard"
    },
    {"name": "tCWL", "address": MCHBAR + 0xE070, "Category": "Secondary", "Tab": "Timings", "parameters": {"bit_start": 24, "bit_length": 7}, "Column": "Left", "read_type": "standard"},
    {"name": "tCCDL", "Category": "Secondary", "Tab": "Timings", "Column": "Left", "read_type": "dynamic", "dynamic_params": {"offset_start": 0xE600, "value_to_find": 0x00, "offset_base": 0xE200, "bit_start_dynamic": 0, "bit_length_dynamic": 4, "mchbar": 0xFEDC0000, "command": 0, "offset2": 0,}, "Formula": tCCD_L_FORMULA},
    {"name": "tCCDL WR", "Category": "Secondary", "Tab": "Timings", "Column": "Left", "read_type": "dynamic", "dynamic_params": {"offset_start": 0xE600, "value_to_find": 0x00, "offset_base": 0xE200, "bit_start_dynamic": 0, "bit_length_dynamic": 4, "mchbar": 0xFEDC0000, "command": 0, "offset2": 0,}, "Formula": tCCD_L_WR_FORMULA},
    {"name": "tRDRDsg", "address": MCHBAR + 0xE00C, "Category": "Tertiary", "Tab": "Timings", "parameters": {"bit_start": 0, "bit_length": 7}, "Column": "Right", "read_type": "standard"},
    {"name": "tRDRDdg", "address": MCHBAR + 0xE00C, "Category": "Tertiary", "Tab": "Timings", "parameters": {"bit_start": 8, "bit_length": 7}, "Column": "Right", "read_type": "standard"},
    {"name": "tRDRDdr", "address": MCHBAR + 0xE00C, "Category": "Tertiary", "Tab": "Timings", "parameters": {"bit_start": 16, "bit_length": 7}, "Column": "Right", "read_type": "standard"},
    {"name": "tRDRDdd", "address": MCHBAR + 0xE00C, "Category": "Tertiary", "Tab": "Timings", "parameters": {"bit_start": 24, "bit_length": 7}, "Column": "Right", "read_type": "standard"},
    {"name": "tRDWRsg", "address": MCHBAR + 0xE010, "Category": "Tertiary", "Tab": "Timings", "parameters": {"bit_start": 0, "bit_length": 7}, "Column": "Right", "read_type": "standard"},
    {"name": "tRDWRdg", "address": MCHBAR + 0xE010, "Category": "Tertiary", "Tab": "Timings", "parameters": {"bit_start": 8, "bit_length": 7}, "Column": "Right", "read_type": "standard"},
    {"name": "tRDWRdr", "address": MCHBAR + 0xE010, "Category": "Tertiary", "Tab": "Timings", "parameters": {"bit_start": 16, "bit_length": 7}, "Column": "Right", "read_type": "standard"},
    {"name": "tRDWRdd", "address": MCHBAR + 0xE010, "Category": "Tertiary", "Tab": "Timings", "parameters": {"bit_start": 24, "bit_length": 7}, "Column": "Right", "read_type": "standard"},
    {"name": "tWRRDsg", "address": MCHBAR + 0xE014, "Category": "Tertiary", "Tab": "Timings", "parameters": {"bit_start": 0, "bit_length": 7}, "Column": "Right", "read_type": "standard"},
    {"name": "tWRRDdg", "address": MCHBAR + 0xE014, "Category": "Tertiary", "Tab": "Timings", "parameters": {"bit_start": 9, "bit_length": 7}, "Column": "Right", "read_type": "standard"},
    {"name": "tWRRDdr", "address": MCHBAR + 0xE014, "Category": "Tertiary", "Tab": "Timings", "parameters": {"bit_start": 18, "bit_length": 7}, "Column": "Right", "read_type": "standard"},
    {"name": "tWRRDdd", "address": MCHBAR + 0xE014, "Category": "Tertiary", "Tab": "Timings", "parameters": {"bit_start": 25, "bit_length": 7}, "Column": "Right", "read_type": "standard"},
    {"name": "tWRWRsg", "address": MCHBAR + 0xE018, "Category": "Tertiary", "Tab": "Timings", "parameters": {"bit_start": 0, "bit_length": 7}, "Column": "Right", "read_type": "standard"},
    {"name": "tWRWRdg", "address": MCHBAR + 0xE018, "Category": "Tertiary", "Tab": "Timings", "parameters": {"bit_start": 8, "bit_length": 7}, "Column": "Right", "read_type": "standard"},
    {"name": "tWRWRdr", "address": MCHBAR + 0xE018, "Category": "Tertiary", "Tab": "Timings", "parameters": {"bit_start": 16, "bit_length": 7}, "Column": "Right", "read_type": "standard"},
    {"name": "tWRWRdd", "address": MCHBAR + 0xE018, "Category": "Tertiary", "Tab": "Timings", "parameters": {"bit_start": 24, "bit_length": 7}, "Column": "Right", "read_type": "standard"},
    {"name": "tREFIx9", "address": MCHBAR + 0xE438, "Category": "Refresh timings", "Tab": "Timings", "parameters": {"bit_start": 24, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "Refresh Interval", "address": MCHBAR + 0xE444, "Category": "Refresh timings", "Tab": "Timings", "parameters": {"bit_start": 0, "bit_length": 13}, "Column": "Right", "read_type": "standard"},
    {"name": "Refresh panic wm", "address": MCHBAR + 0xE438, "Category": "Refresh timings", "Tab": "Timings", "parameters": {"bit_start": 12, "bit_length": 4}, "Column": "Right", "read_type": "standard"},
    {"name": "Refresh HP WM", "address": MCHBAR + 0xE438, "Category": "Refresh timings", "Tab": "Timings", "parameters": {"bit_start": 8, "bit_length": 4}, "Column": "Right", "read_type": "standard"},
    {"name": "Refresh Stagger Enabled", "address": MCHBAR + 0xE444, "Category": "Refresh timings", "Tab": "Timings", "parameters": {"bit_start": 15, "bit_length": 1}, "Column": "Right", "read_type": "standard"},
    {"name": "Refresh Stagger Mode", "address": MCHBAR + 0xE444, "Category": "Refresh timings", "Tab": "Timings", "parameters": {"bit_start": 16, "bit_length": 1}, "Column": "Right", "read_type": "standard"},
    {"name": "Disable Stolen Refresh", "address": MCHBAR + 0xE444, "Category": "Refresh timings", "Tab": "Timings", "parameters": {"bit_start": 13, "bit_length": 1}, "Column": "Right", "read_type": "standard"},
    {"name": "EFIPULSE Stagger Disable", "address": MCHBAR + 0xE444, "Category": "Refresh timings", "Tab": "Timings", "parameters": {"bit_start": 17, "bit_length": 1}, "Column": "Right", "read_type": "standard"},
    {"name": "En Ref Type Display", "address": MCHBAR + 0xE444, "Category": "Refresh timings", "Tab": "Timings", "parameters": {"bit_start": 14, "bit_length": 1}, "Column": "Right", "read_type": "standard"},
    {"name": "WakeUpOnHPM", "address": MCHBAR + 0xE444, "Category": "Refresh timings", "Tab": "Timings", "parameters": {"bit_start": 18, "bit_length": 1}, "Column": "Right", "read_type": "standard"},
    {"name": "tZQCAL", "address": MCHBAR + 0xE44C, "Category": "Other Timings", "Tab": "Timings", "parameters": {"bit_start": 0, "bit_length": 13}, "Column": "Right", "read_type": "standard"},
    {"name": "tZQCS", "address": MCHBAR + 0xE448, "Category": "Other Timings", "Tab": "Timings", "parameters": {"bit_start": 10, "bit_length": 11}, "Column": "Right", "read_type": "standard"},
    {"name": "ZQCS period", "address": MCHBAR + 0xE448, "Category": "Other Timings", "Tab": "Timings", "parameters": {"bit_start": 0, "bit_length": 10}, "Column": "Right", "read_type": "standard"},
    {"name": "tZQoper", "address": MCHBAR + 0xE440, "Category": "Other Timings", "Tab": "Timings", "parameters": {"bit_start": 13, "bit_length": 11}, "Column": "Right", "read_type": "standard"},
    {"name": "RAISE BLK WAIT", "address": MCHBAR + 0xE438, "Category": "Other Timings", "Tab": "Timings", "parameters": {"bit_start": 20, "bit_length": 4}, "Column": "Right", "read_type": "standard"},
    {"name": "tRPAB_EXT", "address": MCHBAR + 0xE000, "Category": "Other Timings", "Tab": "Timings", "parameters": {"bit_start": 8, "bit_length": 5}, "Column": "Right", "read_type": "standard"},
    {"name": "tREFSBRD", "address": MCHBAR + 0xE00A, "Category": "Other Timings", "Tab": "Timings", "parameters": {"bit_start": 8, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "DERATING EXT", "address": MCHBAR + 0xE006, "Category": "Other Timings", "Tab": "Timings", "parameters": {"bit_start": 11, "bit_length": 4}, "Column": "Right", "read_type": "standard"},
    {"name": "MultiCycCmd", "address": MCHBAR + 0xE08C, "Category": "Other Timings", "Tab": "Timings", "parameters": {"bit_start": 19, "bit_length": 1}, "Column": "Right", "read_type": "standard"},
    {"name": "MultiCycCS", "address": MCHBAR + 0xE07C, "Category": "Other Timings", "Tab": "Timings", "parameters": {"bit_start": 10, "bit_length": 5}, "Column": "Right", "read_type": "standard"},
    {"name": "tMOD", "address": MCHBAR + 0xE440, "Category": "Other Timings", "Tab": "Timings", "parameters": {"bit_start": 24, "bit_length": 7}, "Column": "Right", "read_type": "standard"},
    {"name": "CounttREFI", "address": MCHBAR + 0xE438, "Category": "Other Timings", "Tab": "Timings", "parameters": {"bit_start": 16, "bit_length": 1}, "Column": "Right", "read_type": "standard"},
    {"name": "tCAL", "address": MCHBAR + 0xE08C, "Category": "Other Timings", "Tab": "Timings", "parameters": {"bit_start": 3, "bit_length": 3}, "Column": "Right", "read_type": "standard"},
    {"name": "SRX_Ref_Debits", "address": MCHBAR + 0xE438, "Category": "Other Timings", "Tab": "Timings", "parameters": {"bit_start": 18, "bit_length": 2}, "Column": "Right", "read_type": "standard"},
    {"name": "HPRefOnMRS", "address": MCHBAR + 0xE438, "Category": "Other Timings", "Tab": "Timings", "parameters": {"bit_start": 17, "bit_length": 1}, "Column": "Right", "read_type": "standard"},
    {"name": "PtrSep", "address": MCHBAR + 0xE074, "Category": "Other Timings", "Tab": "Timings", "parameters": {"bit_start": 7, "bit_length": 2}, "Column": "Left", "read_type": "standard"},
    {"name": "DEC tCWL", "address": MCHBAR + 0xE478, "Category": "Other Timings", "Tab": "Timings", "parameters": {"bit_start": 0, "bit_length": 6}, "Column": "Left", "read_type": "standard"},
    {"name": "ADD tCWL", "address": MCHBAR + 0xE478, "Category": "Other Timings", "Tab": "Timings", "parameters": {"bit_start": 6, "bit_length": 6}, "Column": "Left", "read_type": "standard"},
    {"name": "ADD 1QCLK Delay", "address": MCHBAR + 0xE478, "Category": "Other Timings", "Tab": "Timings", "parameters": {"bit_start": 12, "bit_length": 1}, "Column": "Left", "read_type": "standard"},
    {"name": "tWRPDEN", "address": MCHBAR + 0xE054, "Category": "Power down", "Tab": "Timings", "parameters": {"bit_start": 0, "bit_length": 10,}, "Column": "Left", "read_type": "standard"},
    {"name": "tRDPDEN", "address": MCHBAR + 0xE050, "Category": "Power down", "Tab": "Timings", "parameters": {"bit_start": 21, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "tPRPDEN", "address": MCHBAR + 0xE054, "Category": "Power down", "Tab": "Timings", "parameters": {"bit_start": 27, "bit_length": 5}, "Column": "Left", "read_type": "standard"},
    {"name": "tAONPD", "address": MCHBAR + 0xE074, "Category": "Power down", "Tab": "Timings", "parameters": {"bit_start": 0, "bit_length": 6}, "Column": "Left", "read_type": "standard"},
    {"name": "tCPDED", "address": MCHBAR + 0xE08C, "Category": "Power down", "Tab": "Timings", "parameters": {"bit_start": 24, "bit_length": 5}, "Column": "Left", "read_type": "standard"},
    {"name": "tWRPRE", "address": MCHBAR + 0xE004, "Category": "Power down", "Tab": "Timings", "parameters": {"bit_start": 0, "bit_length": 10}, "Column": "Left", "read_type": "standard"},
    {"name": "tXP", "address": MCHBAR + 0xE050, "Category": "Power down", "Tab": "Timings", "parameters": {"bit_start": 7, "bit_length": 7}, "Column": "Left", "read_type": "standard"},
    {"name": "tXPDLL", "address": MCHBAR + 0xE050, "Category": "Power down", "Tab": "Timings", "parameters": {"bit_start": 14, "bit_length": 7}, "Column": "Left", "read_type": "standard"},
    {"name": "tXSDLL", "address": MCHBAR + 0xE440, "Category": "Power down", "Tab": "Timings", "parameters": {"bit_start": 0, "bit_length": 13}, "Column": "Left", "read_type": "standard"},
    {"name": "tPPD", "address": MCHBAR + 0xE000, "Category": "Power down", "Tab": "Timings", "parameters": {"bit_start": 20, "bit_length": 4}, "Column": "Left", "read_type": "standard"},
    {"name": "tCSH", "address": MCHBAR + 0xE054, "Category": "Power down", "Tab": "Timings", "parameters": {"bit_start": 10, "bit_length": 6}, "Column": "Left", "read_type": "standard"},
    {"name": "tCSL", "address": MCHBAR + 0xE054, "Category": "Power down", "Tab": "Timings", "parameters": {"bit_start": 16, "bit_length": 6}, "Column": "Left", "read_type": "standard"},
    {"name": "tCA2CS", "address": MCHBAR + 0xE054, "Category": "Power down", "Tab": "Timings", "parameters": {"bit_start": 22, "bit_length": 5}, "Column": "Left", "read_type": "standard"},
    {"name": "tCKE", "address": MCHBAR + 0xE050, "Category": "Power down", "Tab": "Timings", "parameters": {"bit_start": 0, "bit_length": 7}, "Column": "Left", "read_type": "standard"},
    {"name": "OREF_RI", "address": MCHBAR + 0xE438, "Category": "Power down", "Tab": "Timings", "parameters": {"bit_start": 0, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "CPU", "value": get_cpu_name(), "Category": "General", "Tab": "Skew", "Column": "Left", "read_type": "standard"},
    {"name": "Motherboard", "value": get_motherboard_name(), "Category": "General", "Tab": "Skew", "Column": "Left", "read_type": "standard"},
    {"name": "Capacity", "value": get_total_physical_memory(), "Category": "General", "Tab": "Skew", "Column": "Left", "read_type": "standard"},
    {"name": "Speed", "value": None, "Category": "General", "Tab": "Skew", "Column": "Left", "read_type": "standard"},
    {"name": "Dram Ratio", "address": MCHBAR + 0x5E04, "Category": "General", "Tab": "Skew", "parameters": {"bit_start": 0, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "Multiplier", "address": MCHBAR + 0x5E04, "Category": "General", "Tab": "Skew", "parameters": {"bit_start": 8, "bit_length": 4}, "Column": "Left", "Formula": MULTIPLIER_FORMULA, "read_type": "standard"},
    {"name": "Gear Mode", "address": MCHBAR + 0x5E04, "Category": "General", "Tab": "Skew", "parameters": {"bit_start": 12, "bit_length": 2}, "Column": "Left", "Formula": GEAR_MODE_FORMULA, "read_type": "standard"},
    {"name": "Channels", "value": detect_dual_channel_memory(), "Category": "General", "Tab": "Skew", "parameters": {}, "Column": "Left", "read_type": "standard"},
    {
    "name": "RTT WR",
    "Category": "RTT",
    "Tab": "Skew",
    "Column": "Left",
    "parameter_name": "Name",
    "name_a": "CHA",
    "name_b": "CHB",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0x22,
        "offset_base": 0xE200,
        "bit_start_dynamic": 3,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDC0000,
        "command": 0,
        "offset2": 0,  
    },
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0x22,
        "offset_base": 0xE200,
        "bit_start_dynamic": 3,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDD0000,
        "command": 0,
        "offset2": 0,  
    },
    "Formula": RTT_WR_FORMULA
    },
    {
    "name": "RTT NOM RD",
    "Category": "RTT",
    "Tab": "Skew",
    "Column": "Left",
    "parameter_name": "Name",
    "name_a": "CHA",
    "name_b": "CHB",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0x23,
        "offset_base": 0xE200,
        "bit_start_dynamic": 3,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDC0000,
        "command": 0,
        "offset2": 0,
    },
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0x23,
        "offset_base": 0xE200,
        "bit_start_dynamic": 3,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDD0000,
        "command": 0,
        "offset2": 0,
    },
    "Formula": RTT_NOM_RD_FORMULA
    },
    {
    "name": "RTT NOM WR",
    "Category": "RTT",
    "Tab": "Skew",
    "Column": "Left",
    "parameter_name": "Name",
    "name_a": "CHA",
    "name_b": "CHB",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0x23,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDC0000,
        "command": 0,
        "offset2": 0,  
    },
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0x23,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDD0000,
        "command": 0,
        "offset2": 0,  
    },
    "Formula": RTT_NOM_WR_FORMULA
    },
    {
    "name": "RTT PARK",
    "Category": "RTT",
    "Tab": "Skew",
    "Column": "Left",
    "parameter_name": "Name",
    "name_a": "CHA",
    "name_b": "CHB",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0x08,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDC0000,
        "command": 1,
        "offset2": 0,  
    },
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0x08,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDD0000,
        "command": 1,
        "offset2": 0,  
    },
    "Formula": RTT_PARK_FORMULA
    },
    {
    "name": "RTT PARK DQS",
    "Category": "RTT",
    "Tab": "Skew",
    "Column": "Left",
    "parameter_name": "Name",
    "name_a": "CHA",
    "name_b": "CHB",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0x06,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDC0000,
        "command": 1,
        "offset2": 0,
    },
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0x06,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDD0000,
        "command": 1,
        "offset2": 0,  
    },
    "Formula": DQS_RTT_PARK_FORMULA
    },
    {
    "name": "RTT LOOPBACK",
    "Category": "RTT",
    "Tab": "Skew",
    "Column": "Left",
    "parameter_name": "Name",
    "name_a": "CHA",
    "name_b": "CHB",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0x24,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDC0000,
        "command": 0,
        "offset2": 0,  
    },
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0x24,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDD0000,
        "command": 0,
        "offset2": 0,  
    },
    "Formula": RTT_Loopback_FORMULA
    },
    {
    "name": "CA ODT GROUP A",
    "Category": "ODT",
    "Tab": "Skew",
    "Column": "Left",
    "parameter_name": "Name",
    "name_a": "CHA",
    "name_b": "CHB",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0x05,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDC0000,
        "command": 1,
        "offset2": 0,  
    },
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0x05,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDD0000,
        "command": 1,
        "offset2": 0,  
    },
    "Formula": CA_ODT_FORMULA
    },
    {
    "name": "CS ODT GROUP A",
    "Category": "ODT",
    "Tab": "Skew",
    "Column": "Left",
    "parameter_name": "Name",
    "name_a": "CHA",
    "name_b": "CHB",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0x02,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDC0000,
        "command": 1,
        "offset2": 0,  
    },
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0x02,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDD0000,
        "command": 1,
        "offset2": 0,  
    },
    "Formula": CS_ODT_FORMULA
    },
    {
    "name": "CK ODT GROUP A",
    "Category": "ODT",
    "Tab": "Skew",
    "Column": "Left",
    "parameter_name": "Name",
    "name_a": "CHA",
    "name_b": "CHB",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0x01,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDC0000,  
        "command": 1,
        "offset2": 0,
    },
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0x01,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDD0000,
        "command": 1,
        "offset2": 0,  
    },
    "Formula": CK_ODT_FORMULA
    },
    {
    "name": "CA ODT GROUP B",
    "Category": "ODT",
    "Tab": "Skew",
    "Column": "Left",
    "parameter_name": "Name",
    "name_a": "CHA",
    "name_b": "CHB",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0x07,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDC0000,
        "command": 1,
        "offset2": 0,
    },
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0x07,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDD0000,
        "command": 1,
        "offset2": 0,
    },
    "Formula": CA_ODT_FORMULA
    },
    {
    "name": "CS ODT GROUP B",
    "Category": "ODT",
    "Tab": "Skew",
    "Column": "Left",
    "parameter_name": "Name",
    "name_a": "CHA",
    "name_b": "CHB",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0x04,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDC0000,
        "command": 1,
        "offset2": 0,
    },
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0x04,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDD0000,
        "command": 1,
        "offset2": 0,
    },
    "Formula": CS_ODT_FORMULA
    },
    {
    "name": "CK ODT GROUP B",
    "Category": "ODT",
    "Tab": "Skew",
    "Column": "Left",
    "parameter_name": "Name",
    "name_a": "CHA",
    "name_b": "CHB",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0x03,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDC0000,  
        "command": 1,
        "offset2": 0,
    },
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0x03,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDD0000,
        "command": 1,
        "offset2": 0, 
    },
    "Formula": CK_ODT_FORMULA
    },
    {
    "name": "PULL UP",
    "Category": "RON",
    "Tab": "Skew",
    "Column": "Left",
    "parameter_name": "Name",
    "name_a": "CHA",
    "name_b": "CHB",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0x05,
        "offset_base": 0xE200,
        "bit_start_dynamic": 1,
        "bit_length_dynamic": 2,
        "mchbar": 0xFEDC0000,  
        "command": 0,
        "offset2": 0,
    },
    "Formula": RON_FORMULA,
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0x05,
        "offset_base": 0xE200,
        "bit_start_dynamic": 1,
        "bit_length_dynamic": 2,
        "mchbar": 0xFEDD0000,  
        "command": 0,
        "offset2": 0,
    },
    "Formula": RON_FORMULA,
    },
    {
    "name": "PULL DN",
    "Category": "RON",
    "Tab": "Skew",
    "Column": "Left",
    "parameter_name": "Name",
    "name_a": "CHA",
    "name_b": "CHB",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0x05,
        "offset_base": 0xE200,
        "bit_start_dynamic": 6,
        "bit_length_dynamic": 2,
        "mchbar": 0xFEDC0000,  
        "command": 0,
        "offset2": 0,
    },
    "Formula": RON_FORMULA,
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0x05,
        "offset_base": 0xE200,
        "bit_start_dynamic": 6,
        "bit_length_dynamic": 2,
        "mchbar": 0xFEDD0000,  
        "command": 0,
        "offset2": 0,
    },
    "Formula": RON_FORMULA,
    },
    {"name": "DQ VREFUP", "address": MCHBAR + 0x2CE8, "Category": "VREF", "Tab": "Skew", "parameters": {"bit_start": 0, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "DQ VREFDN", "address": MCHBAR + 0x2CE8, "Category": "VREF", "Tab": "Skew", "parameters": {"bit_start": 8, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "DQ ODT VREFUP", "address": MCHBAR + 0x2CE8, "Category": "VREF", "Tab": "Skew", "parameters": {"bit_start": 16, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "DQ ODT VREFDN", "address": MCHBAR + 0x2CE8, "Category": "VREF", "Tab": "Skew", "parameters": {"bit_start": 24, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "CMD VREFUP", "address": MCHBAR + 0x2CEC, "Category": "VREF", "Tab": "Skew", "parameters": {"bit_start": 0, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "CTL VREFUP", "address": MCHBAR + 0x2CEC, "Category": "VREF", "Tab": "Skew", "parameters": {"bit_start": 8, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "CLK VREFUP", "address": MCHBAR + 0x2CEC, "Category": "VREF", "Tab": "Skew", "parameters": {"bit_start": 16, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "CKE CS VREFUP", "address": MCHBAR + 0x2CEC, "Category": "VREF", "Tab": "Skew", "parameters": {"bit_start": 24, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "CMD VREFDN", "address": MCHBAR + 0x2CF0, "Category": "VREF", "Tab": "Skew", "parameters": {"bit_start": 0, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "CTL VREFDN", "address": MCHBAR + 0x2CF0, "Category": "VREF", "Tab": "Skew", "parameters": {"bit_start": 8, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "CLK VREFDN", "address": MCHBAR + 0x2CF0, "Category": "VREF", "Tab": "Skew", "parameters": {"bit_start": 16, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {
    "name": "DQ VREF",
    "Category": "VREF Additional",
    "Tab": "Skew",
    "Column": "Right",
    "read_type": "dynamic",  
    "dynamic_params": {
        "offset_start": 0xE600,
        "value_to_find": 0x0A,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 7,
        "mchbar": 0xFEDC0000,
        "command": 0,
        "offset2": 0,
    },
    "Formula": VREF_FORMULA,
    },
    {
    "name": "CA VREF",
    "Category": "VREF Additional",
    "Tab": "Skew",
    "Column": "Right",
    "read_type": "dynamic",  
    "dynamic_params": {
        "offset_start": 0xE600,
        "value_to_find": 0x0B,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 7,
        "mchbar": 0xFEDC0000,
        "command": 2,
        "offset2": 0,
    },
    "Formula": VREF_FORMULA,
    },
    {
    "name": "CS VREF",
    "Category": "VREF Additional",
    "Tab": "Skew",
    "Column": "Right",
    "read_type": "dynamic",  
    "dynamic_params": {
        "offset_start": 0xE600,
        "value_to_find": 0x0C,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 7,
        "mchbar": 0xFEDC0000,
        "command": 2,
        "offset2": 0,
    },
    "Formula": VREF_FORMULA,
    },
    {"name": "DLL BWSEL", "address": MCHBAR + 0x01BC, "Category": "MISC Additional", "Tab": "Skew", "parameters": {"bit_start": 12, "bit_length": 6}, "Column": "Right", "read_type": "standard"},
    {"name": "VTT ODT", "address": MCHBAR + 0x017C, "Category": "MISC Additional", "Tab": "Skew", "parameters": {"bit_start": 0, "bit_length": 1}, "Column": "Right", "read_type": "standard"},
    {"name": "VSS ODT", "address": MCHBAR + 0x017C, "Category": "MISC Additional", "Tab": "Skew", "parameters": {"bit_start": 1, "bit_length": 1}, "Column": "Right", "read_type": "standard"},
    {"name": "VDDQ ODT", "address": MCHBAR + 0x017C, "Category": "MISC Additional", "Tab": "Skew", "parameters": {"bit_start": 2, "bit_length": 1}, "Column": "Right", "read_type": "standard"},
    {"name": "Weaklocken DLY Q0", "address": MCHBAR + 0x01AC, "Category": "MISC Additional", "Tab": "Skew", "parameters": {"bit_start": 8, "bit_length": 5}, "Column": "Right", "read_type": "standard"},
    {"name": "Weaklocken DLY", "address": MCHBAR + 0x01AC, "Category": "MISC Additional", "Tab": "Skew", "parameters": {"bit_start": 5, "bit_length": 5}, "Column": "Right", "read_type": "standard"},
    {"name": "SCR DLL EN TIMER VAL", "address": MCHBAR + 0x2D1C, "Category": "MISC Additional", "Tab": "Skew", "parameters": {"bit_start": 13, "bit_length": 10}, "Column": "Right", "read_type": "standard"},
    {"name": "SCR PIEN TIMER VAL", "address": MCHBAR + 0x2D20, "Category": "MISC Additional", "Tab": "Skew", "parameters": {"bit_start": 18, "bit_length": 11}, "Column": "Right", "read_type": "standard"},
    {"name": "ODT Write Early ODT", "address_a": MCHBAR + 0xE074, "address_b": MCHBAR2 + 0xE074, "Category": "ODT DELAY", "Tab": "Skew", "parameters_a": {"bit_start": 6, "bit_length": 1}, "parameters_b": {"bit_start": 6, "bit_length": 1}, "Column": "Right", "parameter_name": "Name", "name_a": "RD", "name_b": "WR", "read_type_a": "standard", "read_type_b": "standard"},
    {"name": "ODT Write Delay", "address_a": MCHBAR + 0xE070, "address_b": MCHBAR2 + 0xE070, "Category": "ODT DELAY", "Tab": "Skew", "parameters_a": {"bit_start": 12, "bit_length": 4}, "parameters_b": {"bit_start": 12, "bit_length": 4}, "Column": "Right", "parameter_name": "Name", "name_a": "RD", "name_b": "WR", "read_type_a": "standard", "read_type_b": "standard"},
    {"name": "ODT Write Duration", "address_a": MCHBAR + 0xE070, "address_b": MCHBAR2 + 0xE070, "Category": "ODT DELAY", "Tab": "Skew", "parameters_a": {"bit_start": 8, "bit_length": 4}, "parameters_b": {"bit_start": 8, "bit_length": 4}, "Column": "Right", "parameter_name": "Name", "name_a": "RD", "name_b": "WR", "read_type_a": "standard", "read_type_b": "standard"},
    {
    "name": "REFRESH",
    "Category": "REFRESH MODE",
    "Tab": "Skew",
    "Column": "Left",
    "read_type": "dynamic",  
    "dynamic_params": {
        "offset_start": 0xE600,
        "value_to_find": 0x04,
        "offset_base": 0xE200,
        "bit_start_dynamic": 4,
        "bit_length_dynamic": 1,
        "mchbar": 0xFEDC0000,
        "command": 0,
        "offset2": 0,
    },
    "Formula": REFRESH_MODE_FORMULA,
    },
    {
    "name": "ODTL WR",
    "Category": "ODTL",
    "Tab": "Skew",
    "Column": "Right",
    "parameter_name": "Offset",
    "name_a": "ON",
    "name_b": "OFF",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0x25,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDC0000,  
        "command": 0,
        "offset2": 0,
    },
    "Formula": ODTL_ON_WR,
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0x25,
        "offset_base": 0xE200,
        "bit_start_dynamic": 3,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDD0000,  
        "command": 0,
        "offset2": 0,
    },
    "Formula": ODTL_ON_WR,
    },
    {
    "name": "ODTL WR NT",
    "Category": "ODTL",
    "Tab": "Skew",
    "Column": "Right",
    "parameter_name": "Offset",
    "name_a": "ON",
    "name_b": "OFF",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0x26,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDC0000,  
        "command": 0,
        "offset2": 0,
    },
    "Formula": ODTL_ON_WR_NT,
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0x26,
        "offset_base": 0xE200,
        "bit_start_dynamic": 3,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDD0000,  
        "command": 0,
        "offset2": 0,
    },
    "Formula": ODTL_ON_WR_NT,
    },
    {
    "name": "ODTL RD NT",
    "Category": "ODTL",
    "Tab": "Skew",
    "Column": "Right",
    "parameter_name": "Offset",
    "name_a": "ON",
    "name_b": "OFF",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0x27,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDC0000,
        "command": 0, 
        "offset2": 0, 
    },
    "Formula": ODTL_ON_RD_NT,
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0x27,
        "offset_base": 0xE200,
        "bit_start_dynamic": 3,
        "bit_length_dynamic": 3,
        "mchbar": 0xFEDD0000,  
        "command": 0,
        "offset2": 0,
    },
    "Formula": ODTL_OFF_RD_NT,
    },
    {"name": "RTL MC0 CHA R0", "address": MCHBAR + 0xE020, "Category": "Latency CHA", "Tab": "RTL", "parameters": {"bit_start": 0, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "RTL MC0 CHA R1", "address": MCHBAR + 0xE020, "Category": "Latency CHA", "Tab": "RTL", "parameters": {"bit_start": 8, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "RTL MC0 CHA R2", "address": MCHBAR + 0xE020, "Category": "Latency CHA", "Tab": "RTL", "parameters": {"bit_start": 16, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "RTL MC0 CHA R3", "address": MCHBAR + 0xE020, "Category": "Latency CHA", "Tab": "RTL", "parameters": {"bit_start": 24, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "RTL MC0 CHA R4", "address": MCHBAR + 0xE024, "Category": "Latency CHA", "Tab": "RTL", "parameters": {"bit_start": 0, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "RTL MC0 CHA R5", "address": MCHBAR + 0xE024, "Category": "Latency CHA", "Tab": "RTL", "parameters": {"bit_start": 8, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "RTL MC0 CHA R6", "address": MCHBAR + 0xE024, "Category": "Latency CHA", "Tab": "RTL", "parameters": {"bit_start": 16, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "RTL MC0 CHA R7", "address": MCHBAR + 0xE024, "Category": "Latency CHA", "Tab": "RTL", "parameters": {"bit_start": 24, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "", "value": "", "Category": "Latency CHA", "Tab": "RTL", "parameters": {"bit_start": 0, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "RTL MC1 CHA R0", "address": MCHBAR2 + 0xE020, "Category": "Latency CHA", "Tab": "RTL", "parameters": {"bit_start": 0, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "RTL MC1 CHA R1", "address": MCHBAR2 + 0xE020, "Category": "Latency CHA", "Tab": "RTL", "parameters": {"bit_start": 8, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "RTL MC1 CHA R2", "address": MCHBAR2 + 0xE020, "Category": "Latency CHA", "Tab": "RTL", "parameters": {"bit_start": 16, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "RTL MC1 CHA R3", "address": MCHBAR2 + 0xE020, "Category": "Latency CHA", "Tab": "RTL", "parameters": {"bit_start": 24, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "RTL MC1 CHA R4", "address": MCHBAR2 + 0xE024, "Category": "Latency CHA", "Tab": "RTL", "parameters": {"bit_start": 0, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "RTL MC1 CHA R5", "address": MCHBAR2 + 0xE024, "Category": "Latency CHA", "Tab": "RTL", "parameters": {"bit_start": 8, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "RTL MC1 CHA R6", "address": MCHBAR2 + 0xE024, "Category": "Latency CHA", "Tab": "RTL", "parameters": {"bit_start": 16, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "RTL MC1 CHA R7", "address": MCHBAR2 + 0xE024, "Category": "Latency CHA", "Tab": "RTL", "parameters": {"bit_start": 24, "bit_length": 8}, "Column": "Left", "read_type": "standard"},
    {"name": "RTL MC0 CHB R0", "address": MCHBAR + 0xE820, "Category": "Latency CHB", "Tab": "RTL", "parameters": {"bit_start": 0, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "RTL MC0 CHB R1", "address": MCHBAR + 0xE820, "Category": "Latency CHB", "Tab": "RTL", "parameters": {"bit_start": 8, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "RTL MC0 CHB R2", "address": MCHBAR + 0xE820, "Category": "Latency CHB", "Tab": "RTL", "parameters": {"bit_start": 16, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "RTL MC0 CHB R3", "address": MCHBAR + 0xE820, "Category": "Latency CHB", "Tab": "RTL", "parameters": {"bit_start": 24, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "RTL MC0 CHB R4", "address": MCHBAR + 0xE824, "Category": "Latency CHB", "Tab": "RTL", "parameters": {"bit_start": 0, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "RTL MC0 CHB R5", "address": MCHBAR + 0xE824, "Category": "Latency CHB", "Tab": "RTL", "parameters": {"bit_start": 8, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "RTL MC0 CHB R6", "address": MCHBAR + 0xE824, "Category": "Latency CHB", "Tab": "RTL", "parameters": {"bit_start": 16, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "RTL MC0 CHB R7", "address": MCHBAR + 0xE824, "Category": "Latency CHB", "Tab": "RTL", "parameters": {"bit_start": 24, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "", "value": "", "Category": "Latency CHB", "Tab": "RTL", "parameters": {"bit_start": 0, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "RTL MC1 CHB R0", "address": MCHBAR2 + 0xE820, "Category": "Latency CHB", "Tab": "RTL", "parameters": {"bit_start": 0, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "RTL MC1 CHB R1", "address": MCHBAR2 + 0xE820, "Category": "Latency CHB", "Tab": "RTL", "parameters": {"bit_start": 8, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "RTL MC1 CHB R2", "address": MCHBAR2 + 0xE820, "Category": "Latency CHB", "Tab": "RTL", "parameters": {"bit_start": 16, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "RTL MC1 CHB R3", "address": MCHBAR2 + 0xE820, "Category": "Latency CHB", "Tab": "RTL", "parameters": {"bit_start": 24, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "RTL MC1 CHB R4", "address": MCHBAR2 + 0xE824, "Category": "Latency CHB", "Tab": "RTL", "parameters": {"bit_start": 0, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "RTL MC1 CHB R5", "address": MCHBAR2 + 0xE824, "Category": "Latency CHB", "Tab": "RTL", "parameters": {"bit_start": 8, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "RTL MC1 CHB R6", "address": MCHBAR2 + 0xE824, "Category": "Latency CHB", "Tab": "RTL", "parameters": {"bit_start": 16, "bit_length": 8}, "Column": "Right", "read_type": "standard"},
    {"name": "RTL MC1 CHB R7", "address": MCHBAR2 + 0xE824, "Category": "Latency CHB", "Tab": "RTL", "parameters": {"bit_start": 24, "bit_length": 8}, "Column": "Right", "read_type": "standard"},

    {
    "name": "Global DFE Gain",
    "Category": "DFE",
    "Tab": "JEDEC",
    "Column": "Left",
    "parameter_name": "Channel",
    "name_a": "A",
    "name_b": "B",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0xF9,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 1,
        "mchbar": 0xFEDC0000,
        "command": 0,  
        "offset2": 2,
    },
    "Formula": DFE_ENABLE_FORMULA,
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0xF9,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 1,
        "mchbar": 0xFEDD0000,  
        "command": 0,
        "offset2": 2,
    },
    "Formula": DFE_ENABLE_FORMULA,
    },
    {
    "name": "Global DFE Tap-1",
    "Category": "DFE",
    "Tab": "JEDEC",
    "Column": "Left",
    "parameter_name": "Channel",
    "name_a": "A",
    "name_b": "B",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0xF9,
        "offset_base": 0xE200,
        "bit_start_dynamic": 1,
        "bit_length_dynamic": 1,
        "mchbar": 0xFEDC0000,
        "command": 0,  
        "offset2": 2,
    },
    "Formula": DFE_ENABLE_FORMULA,
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0xF9,
        "offset_base": 0xE200,
        "bit_start_dynamic": 1,
        "bit_length_dynamic": 1,
        "mchbar": 0xFEDD0000,  
        "command": 0,
        "offset2": 2,
    },
    "Formula": DFE_ENABLE_FORMULA,
    },
    {
    "name": "Global DFE Tap-3",
    "Category": "DFE",
    "Tab": "JEDEC",
    "Column": "Left",
    "parameter_name": "Channel",
    "name_a": "A",
    "name_b": "B",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0xF9,
        "offset_base": 0xE200,
        "bit_start_dynamic": 3,
        "bit_length_dynamic": 1,
        "mchbar": 0xFEDC0000,
        "command": 0,  
        "offset2": 2,
    },
    "Formula": DFE_ENABLE_FORMULA,
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0xF9,
        "offset_base": 0xE200,
        "bit_start_dynamic": 3,
        "bit_length_dynamic": 1,
        "mchbar": 0xFEDD0000,  
        "command": 0,
        "offset2": 2,
    },
    "Formula": DFE_ENABLE_FORMULA,
    },
    {
    "name": "DFE GAIN Value",
    "Category": "DFE2",
    "Tab": "JEDEC",
    "Column": "Right",
    "parameter_name": "Channel",
    "name_a": "A",
    "name_b": "B",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0xF9,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 4,
        "mchbar": 0xFEDC0000,
        "command": 0,  
        "offset2": 1,
    },
    "Formula": DFE_GAIN_FORMULA,
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0xF9,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 4,
        "mchbar": 0xFEDD0000,  
        "command": 0,
        "offset2": 1,
    },
    "Formula": DFE_GAIN_FORMULA,
    },
    {
    "name": "Global DFE Tap-2",
    "Category": "DFE2",
    "Tab": "JEDEC",
    "Column": "Right",
    "parameter_name": "Channel",
    "name_a": "A",
    "name_b": "B",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0xF9,
        "offset_base": 0xE200,
        "bit_start_dynamic": 2,
        "bit_length_dynamic": 1,
        "mchbar": 0xFEDC0000,
        "command": 0, 
        "offset2": 2,
    },
    "Formula": DFE_ENABLE_FORMULA,
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0xF9,
        "offset_base": 0xE200,
        "bit_start_dynamic": 2,
        "bit_length_dynamic": 1,
        "mchbar": 0xFEDD0000,  
        "command": 0,
        "offset2": 2,
    },
    "Formula": DFE_ENABLE_FORMULA,
    },
    {
    "name": "Global DFE Tap-4",
    "Category": "DFE2",
    "Tab": "JEDEC",
    "Column": "Right",
    "parameter_name": "Channel",
    "name_a": "A",
    "name_b": "B",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0xF9,
        "offset_base": 0xE200,
        "bit_start_dynamic": 4,
        "bit_length_dynamic": 1,
        "mchbar": 0xFEDC0000,
        "command": 0, 
        "offset2": 2, 
    },
    "Formula": DFE_ENABLE_FORMULA,
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0xF9,
        "offset_base": 0xE200,
        "bit_start_dynamic": 4,
        "bit_length_dynamic": 1,
        "mchbar": 0xFEDD0000,  
        "command": 0,
        "offset2": 2,
    },
    "Formula": DFE_ENABLE_FORMULA,
    },


    {
    "name": "DFE Tap-1",
    "Category": "Tap 1",
    "Tab": "JEDEC",
    "Column": "Left",
    "parameter_name": "Channel",
    "name_a": "A",
    "name_b": "B",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0xF9,
        "offset_base": 0xE200,
        "bit_start_dynamic": 7,
        "bit_length_dynamic": 1,
        "mchbar": 0xFEDC0000,
        "command": 0, 
        "offset2": 0, 
    },
    "Formula": DFE_TAP_ENABLE_FORMULA,
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0xF9,
        "offset_base": 0xE200,
        "bit_start_dynamic": 7,
        "bit_length_dynamic": 1,
        "mchbar": 0xFEDD0000,  
        "command": 0,
        "offset2": 0,
    },
    "Formula": DFE_TAP_ENABLE_FORMULA,
    },
    {
    "name": "DFE Tap-1 Value",
    "Category": "Tap 1",
    "Tab": "JEDEC",
    "Column": "Left",
    "parameter_name": "Channel",
    "name_a": "A",
    "name_b": "B",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0xF9,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 6,
        "mchbar": 0xFEDC0000,
        "command": 0, 
        "offset2": 0, 
    },
    "Formula": DFE_TAP1_FORMULA,
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0xF9,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 6,
        "mchbar": 0xFEDD0000,  
        "command": 0,
        "offset2": 0,
    },
    "Formula": DFE_TAP1_FORMULA,
    },


    {
    "name": "DFE Tap-3",
    "Category": "Tap 3",
    "Tab": "JEDEC",
    "Column": "Left",
    "parameter_name": "Channel",
    "name_a": "A",
    "name_b": "B",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0xFB,
        "offset_base": 0xE200,
        "bit_start_dynamic": 7,
        "bit_length_dynamic": 1,
        "mchbar": 0xFEDC0000,
        "command": 0, 
        "offset2": 0, 
    },
    "Formula": DFE_TAP_ENABLE_FORMULA,
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0xFB,
        "offset_base": 0xE200,
        "bit_start_dynamic": 7,
        "bit_length_dynamic": 1,
        "mchbar": 0xFEDD0000,  
        "command": 0,
        "offset2": 0,
    },
    "Formula": DFE_TAP_ENABLE_FORMULA,
    },
    {
    "name": "DFE Tap-3 Value",
    "Category": "Tap 3",
    "Tab": "JEDEC",
    "Column": "Left",
    "parameter_name": "Channel",
    "name_a": "A",
    "name_b": "B",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0xFB,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 6,
        "mchbar": 0xFEDC0000,
        "command": 0, 
        "offset2": 0, 
    },
    "Formula": DFE_TAP3_FORMULA,
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0xFB,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 6,
        "mchbar": 0xFEDD0000,  
        "command": 0,
        "offset2": 0,
    },
    "Formula": DFE_TAP3_FORMULA,
    },


    {
    "name": "DFE Tap-2",
    "Category": "Tap 2",
    "Tab": "JEDEC",
    "Column": "Right",
    "parameter_name": "Channel",
    "name_a": "A",
    "name_b": "B",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0xFA,
        "offset_base": 0xE200,
        "bit_start_dynamic": 7,
        "bit_length_dynamic": 1,
        "mchbar": 0xFEDC0000,
        "command": 0, 
        "offset2": 0, 
    },
    "Formula": DFE_TAP_ENABLE_FORMULA,
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0xFA,
        "offset_base": 0xE200,
        "bit_start_dynamic": 7,
        "bit_length_dynamic": 1,
        "mchbar": 0xFEDD0000,  
        "command": 0,
        "offset2": 0,
    },
    "Formula": DFE_TAP_ENABLE_FORMULA,
    },
    {
    "name": "DFE Tap-2 Value",
    "Category": "Tap 2",
    "Tab": "JEDEC",
    "Column": "Right",
    "parameter_name": "Channel",
    "name_a": "A",
    "name_b": "B",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0xFA,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 6,
        "mchbar": 0xFEDC0000,
        "command": 0, 
        "offset2": 0, 
    },
    "Formula": DFE_TAP2_FORMULA,
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0xFA,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 6,
        "mchbar": 0xFEDD0000,  
        "command": 0,
        "offset2": 0,
    },
    "Formula": DFE_TAP2_FORMULA,
    },

    
    {
    "name": "DFE Tap-4",
    "Category": "Tap 4",
    "Tab": "JEDEC",
    "Column": "Right",
    "parameter_name": "Channel",
    "name_a": "A",
    "name_b": "B",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0xFC,
        "offset_base": 0xE200,
        "bit_start_dynamic": 7,
        "bit_length_dynamic": 1,
        "mchbar": 0xFEDC0000,
        "command": 0, 
        "offset2": 0, 
    },
    "Formula": DFE_TAP_ENABLE_FORMULA,
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0xFC,
        "offset_base": 0xE200,
        "bit_start_dynamic": 7,
        "bit_length_dynamic": 1,
        "mchbar": 0xFEDD0000,  
        "command": 0,
        "offset2": 0,
    },
    "Formula": DFE_TAP_ENABLE_FORMULA,
    },
    {
    "name": "DFE Tap-4 Value",
    "Category": "Tap 4",
    "Tab": "JEDEC",
    "Column": "Right",
    "parameter_name": "Channel",
    "name_a": "A",
    "name_b": "B",
    "read_type_a": "dynamic",
    "read_type_b": "dynamic",
    "dynamic_params_a": {
        "offset_start": 0xE600,
        "value_to_find": 0xFC,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 6,
        "mchbar": 0xFEDC0000,
        "command": 0, 
        "offset2": 0, 
    },
    "Formula": DFE_TAP4_FORMULA,
    "dynamic_params_b": {
        "offset_start": 0xE600,
        "value_to_find": 0xFC,
        "offset_base": 0xE200,
        "bit_start_dynamic": 0,
        "bit_length_dynamic": 6,
        "mchbar": 0xFEDD0000,  
        "command": 0,
        "offset2": 0,
    },
    "Formula": DFE_TAP4_FORMULA,
    },
]
def apply_formula(value, formula):
    if value is None:
        return "N/A"
    try:
        if isinstance(formula, dict):
            return formula.get(int(value), "N/A")
        elif callable(formula):
            return formula(value)
        else:
            return str(value)
    except (ValueError, TypeError) as e:
        print(f"Error applying formula: {e}")
        return "N/A"
def get_speed():    
    try:
        gear_mode_entry = next(t for t in TIMINGS if t["name"] == "Gear Mode")
        gear_mode_raw = read_timing(
            gear_mode_entry["address"],
            gear_mode_entry["parameters"]["bit_start"],
            gear_mode_entry["parameters"]["bit_length"],
            read_type=gear_mode_entry.get("read_type", "standard")
        ) if gear_mode_entry["address"] is not None else 0
        gear_mode_str = apply_formula(gear_mode_raw, gear_mode_entry.get("Formula"))
        gear_mode = float(gear_mode_str.split()[-1]) if gear_mode_str != "N/A" else 1
        multiplier_entry = next(t for t in TIMINGS if t["name"] == "Multiplier")
        multiplier_raw = read_timing(
            multiplier_entry["address"],
            multiplier_entry["parameters"]["bit_start"],
            multiplier_entry["parameters"]["bit_length"],
            read_type=multiplier_entry.get("read_type", "standard")
        ) if multiplier_entry["address"] is not None else 0
        multiplier_str = apply_formula(multiplier_raw, multiplier_entry.get("Formula"))
        multiplier = float(multiplier_str) if multiplier_str != "N/A" else 100
        dram_ratio_entry = next(t for t in TIMINGS if t["name"] == "Dram Ratio")
        dram_ratio_raw = read_timing(
            dram_ratio_entry["address"],
            dram_ratio_entry["parameters"]["bit_start"],
            dram_ratio_entry["parameters"]["bit_length"],
            read_type=dram_ratio_entry.get("read_type", "standard")
        ) if dram_ratio_entry["address"] is not None else 0
        dram_ratio = float(dram_ratio_raw) if dram_ratio_raw is not None else 1
        speed = dram_ratio * multiplier * gear_mode
        return f"{round(speed)} MHz"
    except Exception as e:
        print(f"Error calculating speed: {e}")
        return "Unknown"
for timing in TIMINGS:
    if timing["name"] == "Speed":
        timing["value"] = get_speed()
        break