import collections
from pathlib import Path
from typing import List


def parse_symbol_definition(line: str, reference_designator: str):
    stripped_line = line.strip()
    if not stripped_line.startswith(f"{reference_designator}("):
        raise ValueError(f"line doesn't start with '{reference_designator}('")
    if not stripped_line.endswith(")"):
        raise ValueError("line doesn't end with ')'")

    # make a line with ',' separated pin definitions
    trimmed_line = stripped_line[len(reference_designator) + 1 : -1]

    pin_definiton_dict = {}

    # (2:JTAG_TDI),(8:ARRAY_CONTROL_DATA),...
    for definiton in trimmed_line.split(","):
        # (2:JTAG_TDI)
        definition_without_parentheses = definiton.replace("(", "").replace(")", "")

        # 2,JTAG_TDI tuple no longer with parentheses
        (pin_number, pin_name) = definition_without_parentheses.split(":")

        # add to defintion dictionary
        pin_definiton_dict[pin_number] = pin_name

    # sort dictionary by keys (as integer so 1, 2, 3, .. not 1, 10, 100, 101, 2, 21, 22, 3)
    key_list = sorted([int(x) for x in pin_definiton_dict.keys()])
    sorted_pin_definiton_dict = collections.OrderedDict(
        [(x, pin_definiton_dict[str(x)]) for x in key_list]
    )
    print(key_list)
    print(sorted_pin_definiton_dict)
    return sorted_pin_definiton_dict


def to_record_list(path: Path, symbols: List[str]):
    symbol_of_interest_line_dict = {}
    symbol_of_interest_definition_dict = {}
    for symbol in symbols:
        symbol_of_interest_line_dict[symbol] = []

    # separate into lists of lines by symbol
    with open(file=path) as sct_netlist:
        for line in sct_netlist:
            for symbol_of_interest in symbols:
                if symbol_of_interest in line:
                    symbol_of_interest_line_dict[symbol_of_interest].append(line)

    # make definitions of symbols
    for key, value in symbol_of_interest_line_dict.items():
        print("\n\n\n")
        print(key)
        for line in value:
            if key in symbols:
                if line.startswith(f"{key}("):
                    print("\n\ndefinition\n\n")
                    print(line, end="")

                    print("\n\ntrimmed_line\n\n")

                    pin_definitions = parse_symbol_definition(
                        line, reference_designator=key
                    )
                    symbol_of_interest_definition_dict[key] = pin_definitions

    print(symbol_of_interest_definition_dict.keys())
    for ref_des, pin_definitions in symbol_of_interest_definition_dict.items():
        print("")
        print(f"{ref_des} symbol definition")
        for pin_number, pin_name in pin_definitions.items():
            print(f"{pin_number}: {pin_name}")

    # symbol = "CF1"

    symbol_net_dict = {}
    for symbol in symbols:
        symbol_net_dict[symbol] = {}
        for line in symbol_of_interest_line_dict[symbol]:
            print(line, end="")

            # split only on fist occurence
            net, connections_string = line.split(":", 1)
            print(net)
            print(connections_string)

            connections_list = connections_string.split(",")

            for connection in connections_list:
                if connection.startswith(f"{symbol}("):
                    connection_without_net = connection[len(symbol) + 1 : -1]
                    symbol_pin_number, symbol_pin_name = connection_without_net.split(
                        ":"
                    )
                    symbol_net_dict[symbol][int(symbol_pin_number)] = net

    for symbol, connection_dict in symbol_net_dict.items():
        for pin_number_string, net in connection_dict.items():
            print(
                f"{symbol}, {pin_number_string}, {symbol_of_interest_definition_dict[symbol][int(pin_number_string)]}, {net}"
            )

    df_record_list = []
    for symbol in symbols:
        for pin_number in symbol_of_interest_definition_dict[symbol].keys():
            # handle no connects
            if pin_number not in symbol_net_dict[symbol].keys():
                net = "No Connect"
            else:
                net = symbol_net_dict[symbol][pin_number]
            record = {
                "symbol": symbol,
                "pin_number": pin_number,
                "pin_name": symbol_of_interest_definition_dict[symbol][pin_number],
                "net": net,
            }
            df_record_list.append(record)
            print(record)

    return df_record_list
