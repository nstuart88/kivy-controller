/*
 WiFiEsp example: WebServer

 A simple web server that shows the value of the analog input 
 pins via a web page using an ESP8266 module.
 This sketch will print the IP address of your ESP8266 module (once connected)
 to the Serial monitor. From there, you can open that address in a web browser
 to display the web page.
 The web page will be automatically refreshed each 20 seconds.

 For more details see: http://yaab-arduino.blogspot.com/p/wifiesp.html
*/

#include "WiFiEsp.h"

// Emulate Serial1 on pins 6/7 if not present
#ifndef HAVE_HWSERIAL1
#include "SoftwareSerial.h"
SoftwareSerial Serial1(2, 3); // RX, TX
//SoftwareSerial Serial2(4, 5);
#endif
bool started;
//char ssid[] = "DP_Dredge";            // your network SSID (name)
//char pass[] = "6173061032";        // your network password
char ssid[] = "Verizon-M2100-9D38";            // your network SSID (name)
char pass[] = "2d55aaf9";        // your network password
int status = WL_IDLE_STATUS;     // the Wifi radio's status
int reqCount = 0;                // number of requests received
int i = 0;
char receive;
char endRX = "\r\n\r\n";
char processRcv [30];
float RxString[5];
char *end;
char dataArray[] = {"0.000,0.000,0.000,0,0"};

const char* data[5]; 

int startB = 0;

WiFiEspServer server(6543);
long myRssi;

void setup()
{
  // initialize serial for debugging
  Serial.begin(9600);
  // initialize serial for ESP module
  
  Serial1.begin(9600);
  pinMode(4,OUTPUT); 
  pinMode(5,OUTPUT);
  pinMode(6,OUTPUT);
  pinMode(7,OUTPUT);
  pinMode(8,OUTPUT);
  pinMode(9,OUTPUT);
  pinMode(10,OUTPUT);
  pinMode(11,OUTPUT);
  digitalWrite(4,LOW);
  digitalWrite(5,LOW);
  digitalWrite(6,LOW);
  digitalWrite(7,LOW);
  digitalWrite(8,LOW);
  digitalWrite(9,LOW);
  digitalWrite(10,LOW);
  digitalWrite(11,LOW);
  //Serial2.begin(115200);
  // initialize ESP module
  IPAddress ip(192,168,1,140);
  
  WiFi.init(&Serial1);
  //WiFi.config(ip);
  
//  WiFi.setDNS(IPAddress(192,168,2,139));
  //WiFi.gatewayIP();
  //long myRssi = WiFi.RSSI;
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // don't continue
    while (true);
  }

  // attempt to connect to WiFi network
  while ( status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network
    status = WiFi.begin(ssid, pass);
    WiFi.config(ip);
  }

  Serial.println("You're connected to the network");
  printWifiStatus();
  
  // start the web server on port 80
  server.begin();
  if (server.available()){
    bool started = true;
    }
}


void loop()
{
//  myRssi = WiFi.RSSI();
  // listen for incoming clients
  WiFiEspClient client = server.available();
  
  while (client) {
    //Serial.println("New client");
    // an http request ends with a blank line
    boolean currentLineIsBlank = true;
    while (client.connected()) {
      
      if (client.available()) {
        
        receive = client.read();
        dataArray[i] =  receive;

        i++;

        // if you've gotten to the end of the line (received a newline
        // character) and the line is blank, the http request has ended,
        // so you can send a reply
        
        if (receive == '\n' && currentLineIsBlank) {
          i=0;
//          dataArray[18]='\0';
//          dataArray[19]='\0';
          char* token = strtok(dataArray,",\n");
          int x = 0;
          while (token != NULL){
            data[x]= token;
            x++;
            token = strtok(NULL,",\n");

            }

//          client.write(data[0]);
//          client.write(',');
//          client.write(data[1]);
//          client.write(',');
//          client.write(data[2]);
//          client.write(',');
//          client.write(data[3]);
          //client.write('\n');
          char buffer[50];
          char* ok[] = {"ok"};
          sprintf(buffer,"%s,%s,%s,%s,%s,%s\n",ok[0],data[0],data[1],data[2],data[3],data[4]);
          client.print(buffer);

          break;
          }
        if (receive == '\n') {
                                      
          currentLineIsBlank = true;
           
        }
        else if (receive != '\r') {
          
          currentLineIsBlank = false;
        }
        
      }
      
    }
    

    
    RxString[0] = atof(data[0]);
    RxString[1] = atof(data[1]);
    RxString[2] = atof(data[2]);
    RxString[3] = atof(data[3]);
    RxString[4] = atof(data[4]);
//    for (int i = 0 ; i<2 ; i++){
//      switch(i){
//        case 0:
//          
//        
//        }
//      
//      }
    if (RxString[0] > 0){
      digitalWrite(4,HIGH);
      digitalWrite(5,LOW);
      }
    if (RxString[0] == 0){
      digitalWrite(4,LOW);
      digitalWrite(5,LOW);
      }

    if (RxString[0] < 0){
      digitalWrite(5,HIGH);
      digitalWrite(4,LOW);
      }
/////////
    if (RxString[1] > 0){
      digitalWrite(6,HIGH);
      digitalWrite(7,LOW);
      }
    if (RxString[1] <= 0){
      digitalWrite(6,LOW);
      digitalWrite(7,LOW);
      }

    if (RxString[1] < 0){
      digitalWrite(7,HIGH);
      digitalWrite(6,LOW);
      }  
///////
    if (RxString[2] > 0){
      digitalWrite(8,HIGH);
     
      }
    if (RxString[2] <= 0){
      digitalWrite(8,LOW);
      digitalWrite(9,LOW);
     
      }

    if (RxString[2] < 0){
      digitalWrite(9,HIGH);
      digitalWrite(8,LOW);
     
      }
    if (RxString[3] > 0){
      digitalWrite(10,HIGH); 
      
      }
    if (RxString[3] == 0){
      digitalWrite(10,LOW);
      }

    if (RxString[4] > 0){
      digitalWrite(11,HIGH); 
      
      }
    if (RxString[4] == 0){
      digitalWrite(11,LOW);
      }
//    
//    Serial.print(RxString[0]);
//    Serial.print(",");
//    Serial.print(RxString[1]);
//    Serial.print(",");
//    Serial.print(RxString[2]);
//    Serial.print(",");
//    Serial.print(RxString[3]);
//    Serial.print(",");
//    Serial.print(RxString[4]);
////    Serial.print(",");
//   // Serial.print(myRssi);
//    Serial.print('\n');
    delay(10);
    Serial.flush();
    i=0;
    // close the connection:
    
    //Serial.println("Client disconnected");
    
    }
    client.stop();
    client.flush(); 
    client = server.available();
  //WiFi.reset();
   
}


void printWifiStatus()
{
  // print the SSID of the network you're attached to
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
  IPAddress gateway = WiFi.gatewayIP();
  Serial.print("Gateway Address: ");
  Serial.println(gateway);
  //gateway = WiFi.gatewayIP();
  //Serial.println(gateway);
  // print where to go in the browser
  Serial.println();
  Serial.print("To see this page in action, open a browser to http://");
  Serial.println(ip);
  Serial.println();
}
