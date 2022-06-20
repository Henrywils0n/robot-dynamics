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
            }
            else
            {
                return doc;
            }
        }
    }
}

// updates the robots position with data from the json document position
void localizePosition(Robot &robot, StaticJsonDocument<200> position)
{
    robot.x = position["position"][0].as<String>().toFloat();
    robot.y = position["position"][1].as<String>().toFloat();
    robot.theta = position["position"][2].as<String>().toFloat();
}