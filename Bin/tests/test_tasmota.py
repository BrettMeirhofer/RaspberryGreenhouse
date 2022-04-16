from Bin.helper import devices


def test_answer():
    my_device = devices.TasmotaDevice()
    my_device.ip_address = "192.168.1.179"
    my_device.relay_id = 0
    state = my_device.read_state()
    print(state)
    assert state == 1
