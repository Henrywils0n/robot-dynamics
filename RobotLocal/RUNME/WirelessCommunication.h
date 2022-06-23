#include <ArduinoJson.h>
StaticJsonDocument<200> GET(String Address)
{
    // sends the address of the get request to the ESP8266
    Serial.println(Address);
    // waits for the ESP8266 to send the data
    while (1)
    {
        if (Serial.available())
        {
            // loads the data into the json document
            StaticJsonDocument<200> doc;
            DeserializationError error = deserializeJson(doc, Serial);
            // if the data is not valid try again until it is
            if (error != DeserializationError::Ok)
            {
                doc = GET(Address);
                return doc;
            }
            else
            {
                return doc;
            }
        }
    }
}

// updates the robots position with data from the json document position
void localize(String address, Robot &robot)
{
    // sends the address of the get request to the ESP8266
    Serial.println(Address);
    // waits for the ESP8266 to send the data
    while (1)
    {
        if (Serial.available())
        {
            // loads the data into the json document
            StaticJsonDocument<200> doc;
            DeserializationError error = deserializeJson(doc, Serial);
            // if the data is not valid try again until it is
            if (error != DeserializationError::Ok)
            {
                localize(address, robot);
                return;
            }
            else
            {
                robot.x = doc["position"][0].as<String>().toFloat();
                robot.y = doc["position"][1].as<String>().toFloat();
                robot.theta = doc["position"][2].as<String>().toFloat();
                doc.clear();
                clearLeftEncoder();
                clearRightEncoder();
                return
            }
        }
    }
}