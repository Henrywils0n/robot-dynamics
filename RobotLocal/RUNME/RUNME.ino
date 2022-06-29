#include "RobotControl.h"
int id = 1;
String server = "http://192.168.0.181:3000";
void setup(void)
{
    Serial.begin(115200);
}

Robot robotA(0, 0, pi / 2, id, server);
float positions[2][2] = {{0.0f, 0.0f}, {0.0f, 1.0f}};
void loop(void)
{
    for (int i = 0; i < 2; i++)
    {
        robotA.localize();
        robotA.moveTo(positions[i][0], positions[i][1]);
        delay(3000);
    }
}
