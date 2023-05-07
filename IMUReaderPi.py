
from ModuleBase import Module
from pubsub import pub

class IMUReaderPi(Module):
    def __init__ (self, args): # args optional
        super().__init__()
        # self.args = args

        # init variables

        pub.subscribe(self.message_listener, "")
    
    def message_listener(self, message):
        msg = message
    
    def run(self):
        # runs in a loop

        # reads data

        pub.sendMessage("ethernet.send", message = {"data": [1,2,3,4,5,6]}) # data to be sent

class Test_IMU(Module):
    def __init__(self):
        super().__init__()

        pub.subscribe(self.message_listener, "ethernet.send")

    def message_listener(self, message):
        print(message)


if __name__ == "__main__":
    freq = 1
    IMUReaderPi = IMUReaderPi()
    Test_IMU = Test_IMU()
    IMUReaderPi.start(freq) # frequency change
    Test_IMU.start(freq)
