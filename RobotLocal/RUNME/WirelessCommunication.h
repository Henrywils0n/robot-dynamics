#include <ArduinoJson.h>
// updates the robots position with data from the json document position
void localize(String address, Robot &robot)
{
    // sends the address of the get request to the ESP8266
    StaticJsonDocument<200> req;
    req["type"] = "GET";
    req["address"] = address;
    serializeJson(req, Serial);
    req.clear();
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
                robot.x = doc["position"][0].as<float>();
                robot.y = doc["position"][1].as<float>();
                robot.theta = doc["position"][2].as<float>();
                doc.clear();
                clearLeftEncoder();
                clearRightEncoder();
                return;
            }
        }
    }
}
void putPosition(String address, Robot &robot)
{
    // sends the address of the get request to the ESP8266
    StaticJsonDocument<200> req;

    req["type"] = "PUT";
    req["address"] = address;
    req["id"] = robot.id;
    JsonArray position = req.createNestedArray("position");
    position.add(robot.x);
    position.add(robot.y);
    position.add(robot.theta);
    serializeJson(req, Serial);
    req.clear();
}
