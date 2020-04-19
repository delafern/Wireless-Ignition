#!/usr/bin/env python
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from datetime import datetime
import serial.tools.list_ports
from digi.xbee.devices import DigiMeshDevice
from digi.xbee.devices import XBeeDevice
import time

def Arm(instance):
    now=datetime.now()
    string = now.strftime("%H:%M:%S")+ "    DELIVERED:      Arm"
    string = {string:'out'}
    add_messages(string)
    device.send_data_broadcast('arm')

def Disarm(instance):
    now=datetime.now()
    string = now.strftime("%H:%M:%S")+ "    DELIVERED:      Disarm"
    string = {string:'out'}
    add_messages(string)
    device.send_data_broadcast('disarm')

def Launch(instance):
    now=datetime.now()
    string = now.strftime("%H:%M:%S")+ "    DELIVERED:      Launch"
    string = {string:'out'}
    add_messages(string)
    device.send_data_broadcast('relay_on')

def Ping(instance):  
    now=datetime.now()
    string = now.strftime("%H:%M:%S")+ "    DELIVERED       Ping"
    string = {string:'out'}
    add_messages(string)
    device.send_data_broadcast('ping')

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
btn_layout = BoxLayout(orientation='vertical')
for button in buttons: 
    btn_layout.add_widget(button)

#for formatting reasons - populating the labels so they look consistent even if empty
msg_layout = BoxLayout(orientation='vertical')

#todo: color implementation
#turn messages into dictionary
#add a color for whether it was a sent message or a received message
global msgs
msgs={'':'',' ':'','   ':'','    ':'','     ':'','      ':'','       ':'','        ':'','        ':'','         ':'','          ':'','           ':'','           ':'','            ':'','             ':'','              ':'','              ':'','               ':'','                ':'','                ':'','                 ':''}
for m in msgs:
    foo = Label(text=msgs[m])
    foo.bind(size=foo.setter('text_size'))
    msg_layout.add_widget(foo)

def add_messages(message):
    global msgs
    msgs = {**msgs,**message}
    msg_layout.clear_widgets()
    n = 0
    for m in reversed(sorted(msgs.keys())):
        if n>=19:
            break
        elif msgs[m]=='out':
            foo = Label(text='[color=0060DB]'+m+'[/color]',markup=True)
        else: #if== 'in'
            foo = Label(text='[color=24BD00]'+m+'[/color]',markup=True)
        n+=1
        foo.bind(size=foo.setter('text_size'))
        msg_layout.add_widget(foo)  

comport_list=[]
comport_list.append([comport.device for comport in serial.tools.list_ports.comports()])
print(comport_list)
com = input("Input available COM port (ex. COM8).\n COM Port: ")

class MyApp(App):
    def build(self):
        total_layout = BoxLayout(orientation='horizontal')
        total_layout.add_widget(msg_layout)
        total_layout.add_widget(btn_layout)
        return total_layout

#create a callback
def data_receive_callback(xbee_message):
    now=datetime.now()
    string = now.strftime("%H:%M:%S")+ "    RECEIVED:       " +xbee_message.data.decode()
    string = {string:'in'}
    add_messages(string)

#assign comport to device

device = XBeeDevice(com,9600)
device.open()
device.add_data_received_callback(data_receive_callback)

if __name__ == '__main__':
    MyApp().run()
