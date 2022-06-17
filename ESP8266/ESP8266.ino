#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <SoftwareSerial.h>

const char *ssid = "Kelly 2.4";
const char *password = "6134848186";

SoftwareSerial ARD(2, 5);
void connectWiFi()
{
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
}
void setup()
{
  Serial.begin(9600);
  ARD.begin(2400);
}
void loop()
{
  if (ARD.available())
    {
        String test = ARD.readStringUntil('\n');
        ARD.println(test);
        Serial.println(test);
    }
}
