#include "UbidotsESPMQTT.h" 
#include "PubSubClient.h"


#define TOKEN "UBIDOTS_TOKEN_HERE" // Ubidots TOKEN 

#define WIFINAME "YOUR_SSID_HERE" // SSID
#define WIFIPASS "WIFI_PASSWORD_HERE" // Wifi Password
#define sensor    A0       // Water sensor connected to A0 pin of NODEMCU module

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
	
	Serial.begin(115200);
	pinMode(sensor, INPUT);   // Analog pin setup for read 
	client.setDebug(true);    // Pass a true or false bool value to activate debug messages 
	client.wifiConnection(WIFINAME, WIFIPASS); 
	client.begin(callback);
}
void loop() {

	if (!client.connected()) {

		client.reconnect();
	}
//  Water will cause the voltage to rise and the ADC will read this as a higher value.
// Once the value is read the NODEMCU will publish it to UBIDOTS. The Node MCU does not care what the reading is. It only reports it.
// If below trigger value the text message will NOT be delivered. Above trigger it's sent.

	float adcValue = analogRead(sensor);    // Read the ADC channel 
	client.add("h2o_heater1", adcValue);     // Variable for the water heatersensor assigned the ADC value. This will show up in Ubidots within the water-sensor device
	client.ubidotsPublish("water-sensor");  // Device name for Ubidots.

	if (adcValue>=80.0){
		delay(1800000);
	}
	client.loop(); 
	Serial.println("\n"); 
	Serial.print(adcValue); 
	delay(1000);
}
