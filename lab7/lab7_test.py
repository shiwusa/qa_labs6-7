import pytest
from pytest_check import check
from parser import parse_iperf_output
from conftest import client


class TestSuite:

    @pytest.mark.parametrize("expected_output", [
        [15, 100],
        [30, 200]
    ])
    def test_iperf_transfer_bandwidth(self, client, expected_output):
        stdout, stderr, server_stderr = client
        check.is_false(stderr, f"Client has error: {stderr}")
        result = parse_iperf_output(stdout)

        for value in result:
            check.greater(float(value['Transfer']), expected_output[0],
                          f"Transfer: {float(value['Transfer'])} should be greater than {expected_output[0]}")
            check.greater(float(value['Bandwidth']), expected_output[1],
                          f"Bandwidth: {float(value['Bandwidth'])} should be greater than {expected_output[1]}")

    def test_iperf_server(self, client):
        stdout, stderr, server_stderr = client
        check.is_false(server_stderr, f"Server has error: {server_stderr}")
