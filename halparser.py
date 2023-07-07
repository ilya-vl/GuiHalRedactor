import os

def load_components(folder_path):
    comps = {
        "last": [],
        "system": [],
        "logic": [],
        "arithm": [],
        "types": [],
        "drivers": [],
        "other": [],
    }
    # Пройдемся по содержимому папки
    str = ""
    noparsed = []
    if (os.path.exists(folder_path) and os.path.isdir(folder_path)):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                if (item == "Submakefile" or item == ""): continue
                item_s = item.split(".")[0]
                item_r = item.split(".")[1]
                
                if (item_r == "c" or item_r == "h"):
                    noparsed.append(item_s)
                    continue

                if (item_s in ["axis", "joint", "halui", "io", "iocontrol", "iov2", "milltask"]):
                    str = "system"
                elif (item_s in 
                        ["and2", "bitwise", "dbounce", "debounce", "demux", "edge", "estop_latch", "flipflop", "logic", "lut5", "match8", "multiclick", "multiswitch", "not", "oneshot", "or2", "select8", "tof", "toggle", "toggle2nist", "ton", "timedelay", "tp", "tristate_bit", "tristate_float", "xor2"]):
                    str = "logic"
                elif (item_s in ["abs_s32", "abs", "biquad", "blend", "comp", "constant", "counter", "ddt", "deadzone", "hypot", "ilowpass", "integ", "invert", "filter_kalman", "knob2float", "lowpass", "limit1", "limit2", "limit3", "lincurve", "maj3", "minmax", "mult2", "mux16", "mux2", "mux4", "mux8", "mux_generic", "near", "offset", "sample_hold", "scale", "sum2", "timedelta", "updown", "wcomp", "weighted_sum", "xhc_hb04_util"]):
                    str = "arithm"
                elif (item_s in ["bin2gray", "bitslice", "conv_bit_float", "conv_bit_s32", "conv_bit_u32", "conv_float_s32", "conf_float_u32", "conv_s32_bit", "conf_s32_float", "conv_s32_u32", "conv_u32_bit", "conv_u32_float", "conv_u32_s32", "gray2bin"]):
                    str = "types"
                else:
                    str = "other"
                
                comps[str].append(item)
    return comps, noparsed

def isHasCountPins(pins):
    for pin in pins:
        if (pin["maxcount"] != "" and pin["varname"] != ""):
            return True
        
    return False

def component_parse(component_file):
    # Чтение файла описания компонента
    if (not os.path.exists(component_file)): return False
    with open(component_file, "r") as file:
        lines = file.readlines()

    # Переменные для хранения информации о входах и выходах
    pins = []
    
    # Обработка строк файла описания компонента
    for line in lines:
        line = line.strip()
        if line.startswith("pin "):
            parts = line.split()
            pin_direction = parts[1]
            pin_type = parts[2]
            pin_name = parts[3].rstrip(";")
            pin_description = " ".join(parts[4:])

            pin_maxcount = ""
            pin_varname = ""
            pin_ccc = ""

            if pin_direction not in ["in", "out", "io"]: continue

            if (len(pin_name.split("-##[")) > 1):
                other_text = "".join(parts[3:]).rstrip(";")
                pin_namesplt = other_text.split("-##[")
                if ( len(pin_namesplt) > 1 ):
                    pin_ccc = pin_namesplt[1].split(":")
                    pin_maxcount = pin_ccc[0]
                    pin_name = pin_namesplt[0] + "#"
                else: pin_maxcount = ""

                if (pin_maxcount != ""):
                    pin_varname = pin_ccc[1].split("]")[0].split("&")[0] #parts[4:][1]
                else : pin_varname = ""
                pin_description = pin_name, "maximum <"+pin_maxcount+"> pins"
                
            pins.append({
                    "dir": pin_direction,
                    "name": pin_name,
                    "type": pin_type,
                    "description": pin_description,
                    "maxcount": pin_maxcount,
                    "varname": pin_varname
                })
    return pins
    # Вывод списка входов
    # print("Inputs:")
    # for input_pin in inputs:
    #     print("Pin Name:", input_pin["name"])
    #     print("Pin Type:", input_pin["type"])
    #     print("Pin Description:", input_pin["description"])
    #     print("-----------------------------")

    # # Вывод списка выходов
    # print("Outputs:")
    # for output_pin in outputs:
    #     print("Pin Name:", output_pin["name"])
    #     print("Pin Type:", output_pin["type"])
    #     print("Pin Description:", output_pin["description"])
    #     print("-----------------------------")

# test, tests, testsss = component_parse("/home/pi/dev/linuxcnc/src/hal/components/logic.comp")
# i = 0
# print()
# for t in test:
#     print(t["dir"], t["name"], t["maxcount"], t["varname"])