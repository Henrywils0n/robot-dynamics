#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ArduinoJson.h>

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
    serializeJson(doc, Serial);
  }
  else
  {
    return;
  }
}
void PUT(String address, String payload)
{
  WiFiClient client;
  HTTPClient http;
  http.begin(client, address);
  int httpCode = http.PUT(payload);
  http.end();
  return;
}
void setup()
{
  Serial.begin(115200);
  connectWiFi();
}

void loop()
{
  if (Serial.available())
  {
    StaticJsonDocument<200> req;
    DeserializationError error = deserializeJson(req, Serial);
    if (error == DeserializationError::Ok)
    {
      if (req["type"].as<String>() == "GET")
      {
        GET(req["address"].as<String>());
      }
      if (req["type"].as<String>() == "PUT")
      {
        StaticJsonDocument<200> doc;
        doc["id"] = req["id"].as<int>();
        doc["x"] = position[0].as<float>();
        doc["y"] = position[1].as<float>();
        doc["theta"] = position[2].as<float>();
        String payload;
        serializeJson(doc, payload);
        PUT(req["address"].as<String>(), payload);
        doc.clear();
      }
    }
    req.clear();
  }
}
