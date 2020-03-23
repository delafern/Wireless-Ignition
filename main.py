import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from datetime import datetime
import serial.tools.list_ports
from digi.xbee.devices import DigiMeshDevice
from digi.xbee.devices import XBeeDevice


def Arm(instance):
    device.send_data_broadcast('arm')
    now=datetime.now()
    string = now.strftime("%H:%M:%S")+ "    SENT:           Arm"
    add_messages(string)

def Disarm(instance):
    device.send_data_broadcast('disarm')
    now=datetime.now()
    string = now.strftime("%H:%M:%S")+ "    SENT:           Disarm"
    add_messages(string)

def Launch(instance):
    device.send_data_broadcast('relay_on')
    now=datetime.now()
    string = now.strftime("%H:%M:%S")+ "    SENT:           Launch"
    add_messages(string)

def Ping(instance):  
    device.send_data_broadcast('ping')
    now=datetime.now()
    string = now.strftime("%H:%M:%S")+ "    SENT:           Ping"
    add_messages(string)

buttons=[]
def make_button(command,func):
    btn = Button(text=command)
    btn.bind(on_press = func)
    buttons.append(btn)
    return buttons

btn1 = make_button('Arm',Arm)
btn2 = make_button('Disarm',Disarm)
btn3 = make_button('Launch',Launch)
btn4 = make_button('Ping',Ping)
#buttons = [btn1,btn2,btn3,btn4]
btn_layout = BoxLayout(orientation='vertical')
for button in buttons: 
    btn_layout.add_widget(button)

#for formatting reasons - populating the labels so they look consistent even if empty
msg_layout = BoxLayout(orientation='vertical')
msgs=['','','','','','','','','','','','','','','','','','','','']
for m in msgs:
    foo = Label(text=m)
    foo.bind(size=foo.setter('text_size'))
    msg_layout.add_widget(foo)

def add_messages(message):
    global msgs
    msgs.insert(0,message)
    msgs = msgs[0:19]
    msg_layout.clear_widgets()
    for m in msgs:
        foo = Label(text=m)
        foo.bind(size=foo.setter('text_size'))
        msg_layout.add_widget(foo)

class MyApp(App):
    def build(self):
        total_layout = BoxLayout(orientation='horizontal')
        total_layout.add_widget(msg_layout)
        total_layout.add_widget(btn_layout)
        return total_layout

#get comports and list them
comport_list=[]
comport_list.append([comport.device for comport in serial.tools.list_ports.comports()])
print(comport_list)
com = input("Input available COM port (ex. COM8): ")

#create a callback
def data_receive_callback(xbee_message):
    #text = "\nFrom  %s %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),strftime("%H:%M:%S"),xbee_message.data.decode())
    now=datetime.now()
    string = now.strftime("%H:%M:%S")+ "    RECEIVED:   " +xbee_message.data.decode()
    add_messages(string)

#assign comport to device
device = XBeeDevice(com,9600)
device.open()
device.add_data_received_callback(data_receive_callback)

if __name__ == '__main__':
    MyApp().run()