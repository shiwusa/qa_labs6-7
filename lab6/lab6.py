from subprocess import Popen, PIPE
import re

server_ip = '192.168.1.110'


def client(ip):
    process = Popen(['iperf', '-c', ip, '-i', '1', '-t', '10', '-b', '3G', '-l', '1000', '-u'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode(), stderr.decode()


def parse(output):
    lines = output.split('\n')
    data_list = []

    for line in lines:
        match = re.search(
            r'([0-9]*\.[0-9]+-[0-9]*\.[0-9]+)\s+sec\s+([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[Ee]([+-]?\d+))?\s+([A-Za-z][A-Za-z]ytes)\s\s([0-9]*\.[0-9]+)\s+([A-Za-z]+bits/sec)', line)
        if match:
            interval = match.group(1) + "sec"
            transfer = match.group(2)
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


result, error = client(server_ip)

if error:
    print("Error:", error)
else:
    result_list = parse(result)
    for value in result_list:
        if float(value['Transfer']) > 200 and float(value['Bandwidth']) > 2:
            print(value)
