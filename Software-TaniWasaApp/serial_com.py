import serial
import serial.tools.list_ports

class SerialCom:

    def __init__(self):
        self.arduino_ser = serial.Serial()
        self.actual_baudrate = 38400
        self.actual_port = None
        self.actual_pressure_val = ""
        self.update_ports()

    def update_ports(self):
        self.ports = serial.tools.list_ports.comports()
        self.port_list = []
        for one_port in self.ports:
            self.port_list.append(str(one_port))
    
    def _update_serial_params(self):
        self.arduino_ser.baudrate = self.actual_baudrate
        self.arduino_ser.port = self.actual_port

    def open_and_write(self, command):
        self._update_serial_params()
        self.arduino_ser.open()
        self.arduino_ser.write(bytes(command, 'utf-8'))
    
    def receive_data(self, data_list=[], save_data=True):
        if self.arduino_ser.in_waiting:
            bytes_data = self.arduino_ser.readline()
            str_data = bytes_data.decode('utf').strip()
            
            if str_data.lower() == "done":
                return False
            else:
                if save_data:
                    data_list.append(str_data)
                self.actual_pressure_val = str_data
                return True

# Search available ports
# Initialize serial comm
# data lecture
    # Open comm
    # Send command character
    # Receive 100 analogReads and make an average
    # Close comm
# Activate air pumps
    # Open comm
    # Send command character 1
    # Send pressure string
    # Receive analogReads from sensor until adecuate pressure is reached
    # If neccesary send command for deactivating the pump
    # Receive confirmation
    # Close comm