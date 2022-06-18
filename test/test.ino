#include <SoftwareSerial.h>
#include <ArduinoJson.h>
SoftwareSerial ESPserial(12, 13); // RX | TX
String address = "http://192.168.0.181:3000/agents/1";
StaticJsonDocument<200> GET(String Address)
{

    ESPserial.println(Address);
    while (1)
    {
        if (ESPserial.available())
        {
            StaticJsonDocument<200> doc;
            DeserializationError error = deserializeJson(doc, ESPserial);
            if (error != DeserializationError::Ok)
            {
                Serial.println("Deserialization failed");
            }
            else
            {
                return doc;
            }
        }
    }
}
void setup()
{
    Serial.begin(19200);
    ESPserial.begin(9600);
}

void loop()
{
    String payload = GET(address);
    parseJsonPosition(payload);
}
