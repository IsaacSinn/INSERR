'''
Subscribe Topics:

thruster.power
    message: FL, FR, BL, BR, BL, UF, UB <-1, 1>

Publish Topics:

can.send
    address <hexadecimal>
    data <bytearray>

thurster.info
    "thrusters_output": FL, FR, BL, BR, BL, UF, UB <32767, -32768> Integer

'''


from ModuleBase import Module
from pubsub import pub
import yaml
import numpy as np

class Thrusters(Module):
    def __init__ (self):
        super().__init__()
        try:
            content = yaml.load(open('Thruster.yaml', 'r'), Loader = yaml.FullLoader)
            for key,value in content.items():
                exec(f"self.{key} = value")
        except FileNotFoundError:
            pass

        pub.subscribe(self.listener, "thruster.power")
        self.current_power = [0,0,0,0,0,0]
        self.output_power = [0,0,0,0,0,0]
        self.difference = [0,0,0,0,0,0]
        self.target_power = [[0,0,0,0,0,0]]
        self.Thrusters = [self.ThrusterFL, self.ThrusterFR, self.ThrusterBL, self.ThrusterBR, self.ThrusterUF, self.ThrusterUB]


    @staticmethod
    def valmap(value, istart, istop, ostart, ostop):
      return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

    def listener(self, message):
        self.power = message["thruster_power"]
        for list in self.power:
            for counter, power in enumerate(list):
                if power > 0:
                    self.target_power[0][counter] = self.valmap(power, 0, 1, self.Thrusters[counter]["Deadzone"], 1)
                elif power < 0:
                    self.target_power[0][counter] = self.valmap(power, 0, -1, -self.Thrusters[counter]["Deadzone"], -1)
                else:
                    self.target_power[0][counter] = 0

    def run(self):
        rate = self.rate * (1 / self.interval)
        for list in self.target_power:
            for counter, power in enumerate(list):
                self.difference[counter] = power - self.current_power[counter]
                if abs(self.difference[counter]) > rate:
                    self.current_power[counter] += self.difference[counter]/abs(self.difference[counter])*rate
                else:
                    self.current_power[counter] = power
                if abs(self.current_power[counter]) > 1:
                    self.output_power[counter] = self.current_power/abs(self.current_power[counter])
                else:
                    self.output_power[counter] = self.current_power[counter]

                if self.output_power[counter] >= 0:
                    self.output_power[counter] = int(self.output_power[counter]*32767)
                else:
                    self.output_power[counter] = int(self.output_power[counter]*32768)
                pub.sendMessage("can.send", message = {"address": self.Thrusters[counter]["Address"], "data": [32, self.output_power[counter] >> 8 & 0xff, self.output_power[counter] & 0xff]})
                pub.sendMessage("thrusters.info", message = {"thrusters_output": self.output_power})
            #print(self.output_power)


class __Test_Case_Send__(Module):
    def __init__(self):
        super().__init__()
        pub.subscribe(self.can_send_listener, "can.send")

    def can_send_listener(self, message):
        print('address:' ,message["address"], 'data(binary):', message["data"], 'data(int):', message["data"][1] << 8| message["data"][2])

    def run(self):
        pub.sendMessage("thruster.power", message = {"thruster_power": [[0.0001,0,0,0,0,0]]})
        self.stop_all()

if __name__ == "__main__":
    pass
