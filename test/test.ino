#include <ArduinoJson.h>

void setup()
{
    Serial.begin(115200);
    int BUFFER_SIZE = JSON_OBJECT_SIZE(5) + JSON_ARRAY_SIZE(40);
    Serial.println(BUFFER_SIZE);
}

void loop()
{
}
