#include "RobotControl.h"
#include "WirelessCommunication.h"
String positionAddress = "http://192.168.0.181:3000/agents/1";
void setup(void)
{
    Serial.begin(115200);
}

Robot robotA(0, 0, pi / 2);

void loop(void)
{
    StaticJsonDocument<200> position = GET(positionAddress);
    localizePosition(robotA, position);
    position.clear();
    robotA.moveTo(0, 0);
    position = GET(positionAddress);
    localizePosition(robotA, position);
    position.clear();
    robotA.moveTo(0, 0.5);
}
