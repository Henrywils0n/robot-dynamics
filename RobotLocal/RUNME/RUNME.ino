#include "RobotControl.h"
#include "WirelessCommunication.h"
String positionAddress = "http://192.168.0.181:3000/agents/1";
void setup(void)
{
    Serial.begin(115200);
}

Robot robotA(0, 0, pi / 2);
float positions[] = {{0, 0}, {0, 1}, {0.5, 0.5}, {0, 1}};
void loop(void)
{
    for (int i = 0; i < 4; i++)
    {
        localize(positionAddress, robotA);
        Serial1.print("(");
        Serial1.print(robotA.x);
        Serial1.print(", ");
        Serial1.print(robotA.y);
        Serial1.print(", ");
        Serial1.print(robotA.theta);
        Serial1.print(")\n")
        // robotA.moveTo(positions[i][0], positions[i][1]);
    }
}
