# parser
import re


def parse_iperf_output(output):
    lines = output.split('\n')
    data_list = []

    for line in lines:
        match = re.search(
            r'([0-9]*\.[0-9]+)-([0-9]*\.[0-9]+)\ssec\s+([0-9]*\.[0-9]+)\s+([A-Za-z0-9]+)\s+([0-9]+)\s+([A-Za-z]+/[A-Za-z]+)',
            line)
        if match:
            interval = match.group(1) + "-" + match.group(2)
            transfer = match.group(3)
            transfer_unit = match.group(4)
            bandwidth = match.group(5)
            bandwidth_unit = match.group(6)
            data_list.append({
                'Interval': interval,
                'Transfer': transfer,
                'Transfer unit': transfer_unit,
                'Bandwidth': bandwidth,
                'Bandwidth unit': bandwidth_unit,
            })
    return data_list
