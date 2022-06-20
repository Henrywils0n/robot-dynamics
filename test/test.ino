#include <ArduinoJson.h>
String address = "http://192.168.0.181:3000/agents/1";
String addresses[] = {"http://192.168.0.181:3000/agents/1", "http://192.168.0.181:3000/agents/2", "http://192.168.0.181:3000/agents/3"};
StaticJsonDocument<200> GET(String Address)
{

    Serial.println(Address);
    while (1)
    {
        if (Serial.available())
        {
            StaticJsonDocument<200> doc;
            DeserializationError error = deserializeJson(doc, Serial);
            if (error != DeserializationError::Ok)
            {
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
    Serial.begin(115200);
}

void loop()
{
    for (int i = 0; i < 3; i++)
    {
        int start = millis();
        StaticJsonDocument<200> payload = GET(addresses[i]);
        float position[] = {payload["position"][0], payload["position"][1], payload["position"][2]};
        delay(2000);
    }
}
