#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

const char *ssid = "Kelly 2.4";
const char *password = "6134848186";

void connectWiFi()
{
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
  }
}
void GET(String address)
{
  WiFiClient client;
  HTTPClient http;
  http.begin(client, address);
  int httpCode = http.GET();
  if (httpCode > 0)
  {
    String payload = http.getString();
    char buff[payload.length()];
    payload.toCharArray(buff, payload.length());
    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, buff);
    SerializeJson(doc, Serial);
  }
  else
  {
    return;
  }
}
void setup()
{
  Serial.begin(9600);
  connectWiFi();
}
void loop()
{
  if (Serial.available())
  {
    String address = Serial.readStringUntil('\n');
    address.trim();
    GET(address);
  }
}
