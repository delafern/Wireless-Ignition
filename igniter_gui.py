##just a quick demo to show how to enable a xbee device, create a callback, and send commands through the command window
import serial.tools.list_ports
from digi.xbee.devices import XBeeDevice
from time import gmtime, strftime

global text
messages = []

comport_list=[] #list of available ports for the user to choose from
comport_list.append([comport.device for comport in serial.tools.list_ports.comports()])
#menu to select comport, in case it isnt com8...
device = XBeeDevice("COM8",9600)

device.open()

def data_receive_callback(xbee_message):
    text = "From %s %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),strftime("%H:%M:%S"),xbee_message.data.decode())
    messages.append(text)
    print(text)

device.add_data_received_callback(data_receive_callback)
#device.send_data_broadcast('ping')

device.send_data_broadcast('ping')

print('hi')
