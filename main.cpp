//the receiving end which ignites the motor
#include <Arduino.h>
#include <XBee.h>
#define PROCESSING 16 //processing led (for testing)
#define RELAY 13 //pin to arm relay
unsigned long time_now; //current time
unsigned long time_armed; //time when we get the "arm" command
const unsigned long arm_window = 60000; //60 second window for igniting the rocket after sending an "arm" commmand for safety
boolean process = false; //boolean variable for processing received strings
boolean armed = false; //boolean variable for adding safety to ignite rocket motor

//xbee stuff and objects
XBeeAddress64 base_addr64 =  XBeeAddress64(0x0013a200, 0x41912af0); //address of base Xbee
XBee xbee = XBee();
XBeeResponse response = XBeeResponse();
ZBRxResponse rx = ZBRxResponse();

//build some functions
//transmit function, courtesy of richard smith
void xbee_transmit(String msg) {
  char msg_c[100];
  strcpy(msg_c, msg.c_str());
  ZBTxRequest tx_request = ZBTxRequest(base_addr64, (uint8_t*)msg_c, strlen(msg_c) + 1);
  xbee.send(tx_request);
}

void arm() //function to arm the igniter, mark the time the igniter was armed for timeout
  {
    time_armed = millis();
    armed = true;
    xbee_transmit("Igniter is armed");
  }
  
void relayOFF() //turn the relay off
  {
    digitalWrite(RELAY,LOW);
    digitalWrite(PROCESSING,LOW);
    xbee_transmit("Relay off");
  }

void disarm() //turn armed to false
  {
    armed = false;
    relayOFF();
    xbee_transmit("Igniter Disarmed");
  }

void relayON() //check if armed is set to true and ignite motor if so, else reply to user saying did not digitally arm
  {
    if (armed) {
      digitalWrite(RELAY,HIGH);
      digitalWrite(PROCESSING,HIGH);
      xbee_transmit("Relay on");
    } else {
      xbee_transmit("Igniter not digitally armed");
   }
  }


//setup time
//declare our pin outputs, open serial, send a welcome message (if anyones listening)
void setup()
{
    pinMode(RELAY,OUTPUT);
    pinMode(PROCESSING,OUTPUT);
    Serial1.begin(9600);
    xbee.begin(Serial1);
    delay(2000);
    xbee_transmit("Waiting for command");
}

//main loop
void loop()
{
  String cmd = ""; //empty string for commands from controller
  xbee.readPacket(); //look for packets
  
  if (xbee.getResponse().isAvailable())
  {
    if (xbee.getResponse().getApiId() == ZB_RX_RESPONSE) // MUST HAVE THIS OR YOU GET STUCK IN LOOP
    {
      cmd = ""; //clear our cmd string
      xbee.getResponse().getZBRxResponse(rx) ; //POPULATE THE xbee RESPONSE
      for (int i = 0; i < rx.getDataLength(); i++) //loop through the length of the response to build a command string
      {
        cmd += ((char)rx.getData(i)); 
      }
      process = true; //enter processing state
    }
  }

  else
  { 
    process = false; //we got no command so don't enter a processing state
  }  


  if (process)
  {
//    digitalWrite(16,HIGH);
    delay(100);
    if (cmd=="relay_on")  {
        relayON();
      } else if (cmd=="relay_off")  {
        relayOFF();
      } else if (cmd=="ping") {
        xbee_transmit("ping received");
      } else if (cmd=="arm") {
        arm();
      } else if (cmd=="disarm") {
        disarm();
      }
   process = false; // turn off the process since we ran the code
  }

//check to see if time is up and need to auto disarm igniter
  time_now = millis();  
  if (time_now-time_armed >= arm_window)
  {
    armed=false;
  }
} //end main loop
