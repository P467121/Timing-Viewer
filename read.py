import ctypes
import sys
import os
from ctypes import wintypes
try:
    dll_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "inpoutx64.dll")
    if not os.path.exists(dll_path):
        sys.exit(f"Error: inpoutx64.dll not found at {dll_path}. Please ensure the DLL is present.")
    inpout = ctypes.WinDLL(dll_path)
except Exception as e:
    sys.exit(f"Error loading inpoutx64.dll: {str(e)}. Ensure the DLL is compatible and you have administrator privileges.")
inpout.MapPhysToLin.argtypes = [wintypes.LPVOID, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE)]
inpout.MapPhysToLin.restype = wintypes.LPVOID
inpout.UnmapPhysicalMemory.argtypes = [wintypes.HANDLE, wintypes.LPVOID]
inpout.UnmapPhysicalMemory.restype = wintypes.BOOL
def map_physical_address(phys_addr, size):
    handle = wintypes.HANDLE()
    virt_addr = inpout.MapPhysToLin(phys_addr, size, ctypes.byref(handle))
    if not virt_addr:
        raise Exception(f"Failed to map physical address 0x{phys_addr:016X}. Ensure the driver is running and you have administrator privileges.")
    return virt_addr, handle
def unmap_physical_memory(handle, virt_addr):
    if not inpout.UnmapPhysicalMemory(handle, virt_addr):
        print(f"Warning: Failed to unmap physical memory at 0x{virt_addr:016X}")
def read_physical_memory(phys_addr, size=4):
    try:
        virt_addr, handle = map_physical_address(phys_addr, size)
        try:
            buffer_type = ctypes.c_ubyte * size
            buffer = buffer_type.from_address(virt_addr)
            return bytes(buffer)
        finally:
            unmap_physical_memory(handle, virt_addr)
    except Exception as e:
        print(f"Error reading physical memory at 0x{phys_addr:016X}: {str(e)}")
        return None
def dynamic_read_physical_memory(offset_start, value_to_find, offset_base, bit_start_dynamic, bit_length_dynamic, mchbar, command, offset2):
    try:
        value_to_find = int(value_to_find) & 0xFF  
        read_size = 4  
        start_address = mchbar + offset_start
        end_address = mchbar + 0xE7FF
        step = 4  
        for current_address in range(start_address, end_address + 1, step):
            data = read_physical_memory(current_address, read_size)
            if data is None:
                continue
            data_value = int.from_bytes(data, byteorder='little')
            if (data_value & 0xFF) == value_to_find:
                command_bits = (data_value >> 22) & 0x3
                if command_bits == command:
                    offset = (data_value >> 8) & 0xFF
                    target_address = mchbar + offset_base + offset - offset2
                    target_data = read_physical_memory(target_address, read_size)
                    if target_data is None:
                        print(f"Warning: Failed to read target address 0x{target_address:016X} for value_to_find 0x{value_to_find:02X}")
                        continue
                    hex_str = target_data.hex()
                    value = extract_value_from_hex(hex_str, bit_start_dynamic, bit_length_dynamic)
                    return value
                else:
                    continue
        return None
    except Exception as e:
        print(f"Error in dynamic read at 0x{start_address:016X}: {str(e)}")
        return None
def extract_value_from_hex(hex_str: str, bit_start: int, bit_width: int) -> int:
    hex_str = hex_str.replace(" ", "")
    if len(hex_str) != 8:
        raise ValueError(f"Input must be 4 bytes (8 hex chars), got: {hex_str}")
    bytes_swapped = [hex_str[i:i+2] for i in range(0, 8, 2)][::-1]
    reversed_hex = ''.join(bytes_swapped)
    binary_str = bin(int(reversed_hex, 16))[2:].zfill(32)
    bit_pos = 31 - bit_start
    reverse_bits = bit_width < 0
    effective_width = abs(bit_width)
    extracted_bits = binary_str[bit_pos - effective_width + 1 : bit_pos + 1]
    if reverse_bits:
        extracted_bits = extracted_bits[::-1]
    return int(extracted_bits, 2)
def read_timing(address=None, bit_start=None, bit_length=None, read_type="standard", dynamic_params=None):
    try:
        if read_type == "dynamic" and dynamic_params:
            if not all(key in dynamic_params for key in ["offset_start", "value_to_find", "offset_base", "bit_start_dynamic", "bit_length_dynamic", "mchbar", "command", "offset2"]):
                raise ValueError("Dynamic read requires offset_start, value_to_find, offset_base, bit_start_dynamic, bit_length_dynamic, mchbar, and command")
            value = dynamic_read_physical_memory(
                dynamic_params["offset_start"],
                dynamic_params["value_to_find"],
                dynamic_params["offset_base"],
                dynamic_params["bit_start_dynamic"],
                dynamic_params["bit_length_dynamic"],
                dynamic_params["mchbar"],
                dynamic_params["command"],
                dynamic_params["offset2"]
            )
            return value
        elif read_type == "standard" and address is not None:
            data = read_physical_memory(address)
            if data is None:
                return None
            hex_str = data.hex()
            value = extract_value_from_hex(hex_str, bit_start, bit_length)
            return value
        else:
            print(f"Invalid read configuration: read_type={read_type}, address={address}, dynamic_params={dynamic_params}")
            return None
    except Exception as e:
        print(f"Error processing memory at 0x{address:016X}: {str(e)}")
        return None