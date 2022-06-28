#include "RobotControl.h"
int id = 1;
String server = "http://192.168.0.181:3000";
void setup(void)
{
    Serial.begin(115200);
}

Robot robotA(0, 0, pi / 2, id, server);
float positions[3][2] = {{0, 1}, {0.5, 0.5}, {0, 0}};
float localizedPos[3][3] = {{0, 0.95, pi / 2 + 0.2}, {0.45, 0.52, 11.0 / 16.0 * pi}, {-0.02, 0.05, pi / 2}};
void loop(void)
{
    for (int i = 0; i < 3; i++)
    {
        robotA.localize();
        robotA.putPosition();
        robotA.moveTo(positions[i][0], positions[i][1]);
        delay(3000);
    }
}
