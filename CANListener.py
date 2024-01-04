import can

def listener(msg):
    print(msg)


if __name__ == "__main__":
    bus = can.interface.Bus(channel = "can0", bustype="socketcan")
    can.Notifier(bus, [listener])

    while 1:
        pass
