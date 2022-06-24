#include "RobotControl.h"
#include "WirelessCommunication.h"
int id = 1;
String positionAddress = "http://192.168.0.181:3000/agents/" + String(id);
String sendPositionAddress = "http://192.168.0.181:3000/agentsLocal/" + String(id);
void setup(void)
{
    Serial.begin(115200);
}

Robot robotA(0, 0, pi / 2, id);
float positions[4][2] = {{0, 0}, {0, 1}, {0.5, 0.5}, {0, 1}};
void loop(void)
{
    for (int i = 0; i < 4; i++)
    {
        localize(positionAddress, robotA);
        // robotA.moveTo(positions[i][0], positions[i][1]);
        putPosition(sendPositionAddress, robotA);
    }
}
