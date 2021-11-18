#include "UbidotsESPMQTT.h" 
#include "PubSubClient.h" 
#include <NTPClient.h> 
#include "Time.h"
#include <WiFiUdp.h>

#define TOKEN "UBIDOTS_TOKEN_HERE" // Ubidots TOKEN 
#define WIFINAME "SSID_HERE" // SSID
#define WIFIPASS "WIFI_PASSWORD_HERE" // Wifi Password

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP,10800);

int Status = 15; 
int sensor = 13; 
int motion=0;
Ubidots client(TOKEN);

void callback(char* topic, byte* payload, unsigned int length) {
	
	Serial.print("Message arrived ["); 
	Serial.print(topic); 
	Serial.print("] ");

	for (int i = 0; i < length; i++) {

	Serial.print((char)payload[i]);
	}

	Serial.println();
}


void setup() {
	Serial.begin(9600);
	pinMode(sensor, INPUT); // declare sensor as input 
	pinMode(Status, OUTPUT);  // declare Status as output
	client.setDebug(true);    // Pass a true or false bool value to activate debug messages
	client.wifiConnection(WIFINAME, WIFIPASS); 
	client.begin(callback); 
	timeClient.begin();
}

Time t1,t2,t3; 
int hareket=0;

void loop(){
	
	if (!client.connected()) {
		client.reconnect();
	}
		
	timeClient.update();
	long state = digitalRead(sensor);

	delay(1000);
		if(state == HIGH){
			motion=1;

			if (hareket==0){ 
				hareket=1;
				t1.setTime(timeClient);
			}
			
			digitalWrite (Status, HIGH); 
			Serial.println("Motion detected!");
		}

		else {
			motion=0;
			if (hareket==1){
				
				hareket=0; 
				t2.setTime(timeClient); 
				t3 = t2-t1;
				
			   Serial.println("saat"); 
			   Serial.println(t3.seconds());
			}
			digitalWrite (Status, LOW); 
			Serial.println("Motion absent!");
			}
			client.add("motion-detection2", motion);     // Variable for the water heater sensor assigned the ADC value. This will show up in Ubidots within the water-sensor device
		client.ubidotsPublish("motion-sensor");          // Device name for Ubidots.

	if (motion==1) {
		delay(60000);
	}
	
	client.loop();
	}