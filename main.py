import math
import tabulate
from typing import Literal

OUTPUT_VOLTAGE_DECIMAL_PLACES = 3
GAIN_DECIMAL_PLACES = 5

def find_gain(filter_type, frequency, resistance, C_or_L):
    omega = 2 * math.pi * frequency
    if filter_type == "RC_low":
        return 1 / math.sqrt(1 + (omega * resistance * C_or_L) ** 2)
    elif filter_type == "RC_high":
        return (omega * resistance * C_or_L) / math.sqrt(1 + (omega * resistance * C_or_L) ** 2)
    elif filter_type == "RL_low":
        return resistance / math.sqrt(resistance ** 2 + (omega * C_or_L) ** 2)
    elif filter_type == "RL_high":
        return (omega * C_or_L) / math.sqrt(resistance ** 2 + (omega * C_or_L) ** 2)
    else:
        raise TypeError("Invalid filter type")

# ========== RC ==========
def RC_low_pass_output(input_voltage, frequency, resistance, capacitance, decimal_places=OUTPUT_VOLTAGE_DECIMAL_PLACES):
    Av = find_gain("RC_low", frequency, resistance, capacitance)
    output_voltage = Av * input_voltage
    return round(output_voltage, decimal_places)


def RC_high_pass_output(input_voltage, frequency, resistance, capacitance, decimal_places=OUTPUT_VOLTAGE_DECIMAL_PLACES):   
    Av = find_gain("RC_high", frequency, resistance, capacitance)
    output_voltage = Av * input_voltage
    return round(output_voltage, decimal_places)


# ========== RL ==========
def RL_low_pass_output(input_voltage, frequency, resistance, inductance, decimal_places=OUTPUT_VOLTAGE_DECIMAL_PLACES):
    Av = find_gain("RL_low", frequency, resistance, inductance)
    output_voltage = Av * input_voltage
    return round(output_voltage, decimal_places)
     
def RL_high_pass_output(input_voltage, frequency, resistance, inductance, decimal_places=OUTPUT_VOLTAGE_DECIMAL_PLACES):
    Av = find_gain("RL_high", frequency, resistance, inductance)
    output_voltage = Av * input_voltage
    return round(output_voltage, decimal_places)


def take_inputs(filter_type: Literal["RC_low", "RC_high", "RL_low", "RL_high"]):
    voltage = float(input("Enter input voltage (V): "))
    frequencies = input("Enter input frequency(s) (Hz): ").replace(" ", "").split(",")
    frequencies = sorted([float(f) for f in frequencies])
    resistance = float(input("Enter resistance (Ohm): "))
    capacitance = 0

    if filter_type in ("RC_low", "RC_high"):
        capacitance = float(input("Enter capacitance (F): "))
    elif filter_type in ("RL_low", "RL_high"):
        inductance = float(input("Enter inductance (H): "))
    else:
        raise TypeError("Invalid filter type")

    return voltage, frequencies, resistance, capacitance or inductance


def find_output_volt(filter_type: Literal["RC_low", "RC_high", "RL_low", "RL_high"], input_voltage, frequency, resistance, C_or_L):
    if filter_type ==  "RC_low":
        return RC_low_pass_output(input_voltage, frequency, resistance, C_or_L)
    elif filter_type ==  "RC_high":
        return RC_high_pass_output(input_voltage, frequency, resistance, C_or_L)
    elif filter_type ==  "RL_low":
        return RL_low_pass_output(input_voltage, frequency, resistance, C_or_L)
    elif filter_type ==  "RL_high":
        return RL_high_pass_output(input_voltage, frequency, resistance, C_or_L)
    else:
        raise TypeError("Invalid filter type")


def print_table(data: list[dict]):
    if not data:
        return

    # Get headers from keys of the first dict
    headers = list(data[0].keys())

    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in data:
        for i, h in enumerate(headers):
            col_widths[i] = max(col_widths[i], len(str(row[h])))

    # Build separator line
    sep_line = "+".join("-" * (w + 2) for w in col_widths)
    sep_line = "+" + sep_line + "+"

    # Print header
    header_row = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"
    print(sep_line)
    print(header_row)
    print(sep_line)

    # Print rows
    for row in data:
        row_str = "| " + " | ".join(str(row[h]).ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"
        print(row_str)
    print(sep_line)



def main():
    print("Filters: ")
    for i, f in enumerate(("RC_low", "RC_high", "RL_low", "RL_high"), start=1):
        print(i, f)
    filter_type = int(input("enter filter type (1/2/3/4): "))
    filter_type = {1 :"RC_low",2 :"RC_high",3 :"RL_low",4 :"RL_high"}[filter_type]

    in_voltage, frequencies, resistance, C_or_L = take_inputs(filter_type)

    data = []

    for frq in frequencies:
        data.append({
            "Frequency (Hz)": frq,
            "Input voltage (V)": in_voltage,
            "Output voltage (V)": find_output_volt(filter_type, in_voltage, frq, resistance, C_or_L),
            "Gain": round(find_gain(filter_type, frq, resistance, C_or_L), GAIN_DECIMAL_PLACES)
        })

    print_table(data)




if __name__ == "__main__":
    main()



