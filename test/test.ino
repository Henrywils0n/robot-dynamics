#include <SoftwareSerial.h>

SoftwareSerial ESPserial(12, 13); // RX | TX
String address = "http://192.168.0.181:3000/agents/1";

void setup()
{
    Serial.begin(9600);
    ESPserial.begin(2400);
}

void loop()
{
    if (ESPserial.available())
    {
        String test = ESPserial.readStringUntil('\n');
        Serial.println(test);
    }
    // problem could be interference try adding a delay by checking difference in time between last and current time maybe 50ms or so???? or maybe lower the baud rate or raise the baud rate
    ESPserial.println(address);
}
