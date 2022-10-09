#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include "DHT.h"

#define SERVER_IP "https://restful-api-morgan.herokuapp.com/post/env"
#define STASSID "morgan"
#define STAPSK "testpassword"

DHT dht(4, DHT11);

void setup() {
	Serial.begin(115200);
	WiFi.begin(STASSID, STAPSK);
	while(WiFi.status() != WL_CONNECTED) {
		delay(500);
	}
	Serial.println(WiFi.localIP());
}

void loop() {
	WiFiClient client;
	HTTPClient http;
	float humidity = dht.readHumidity();
	float temp = dht.readTemperature(true);
	if(isnan(humidity) || isnan(temp)) {
		Serial.println(F("Failed to read from DHT sensor!"));
	}
	if ((WiFi.status() == WL_CONNECTED)) {
		http.begin(client, SERVER_IP);
		http.addHeader("Content-Type", "application/json");
		int r = http.POST("{\"temp\": " + temp + ", \"humidity\": " + humidity + "}");
		Serial.println(r);
		http.end();
	}
	delay(10000);
}
