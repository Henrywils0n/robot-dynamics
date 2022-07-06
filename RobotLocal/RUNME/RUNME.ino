#include "RobotControl.h"
#define id 1
String server = "http://192.168.0.181:3000";
void setup(void)
{
    Serial.begin(115200);
}

Robot robotA(0, 0, pi / 2, id, server);
// CW
/*
float positions[16][2] = {{0.0f, 0.25f}, {0.0f, 0.5f}, {0.0f, 0.75f}, {0.0f, 1.0f}, {0.25f, 1.0f}, {0.5f, 1.0f}, {0.75f, 1.0f}, {1.0f, 1.0f}, {1.0f, 0.75f}, {1.0f, 0.5f}, {1.0f, 0.25f}, {1.0f, 0.0f}, {0.75f, 0.0f}, {0.5f, 0.0f}, {0.25f, 0.0f}, {0.0f, 0.0f}};
*/
// CCW
/*
float positions[16][2] = {{0.0f, 0.0f}, {0.25f, 0.0f}, {0.5f, 0.0f}, {0.75f, 0.0f}, {1.0f, 0.0f}, {1.0f, 0.25f}, {1.0f, 0.5f}, {1.0f, 0.75f}, {1.0f, 1.0f}, {0.75f, 1.0f}, {0.5f, 1.0f}, {0.25f, 1.0f}, {0.0f, 1.0f}, {0.0f, 0.75f}, {0.0f, 0.5f}, {0.0f, 0.25f}};
*/
float positions[16][2] = {{0.0f, 0.0f}, {0.25f, 0.25f}, {0.5f, 0.5f}, {0.25f, 0.75f}, {0.0f, 1.0f}, {-0.25f, 0.75f}, {-0.5f, 0.5f}, {-0.25f, 0.25f}, {0.0f, 0.0f}, {0.25f, -0.25f}, {0.5f, -0.5f}, {0.25f, -0.75f}, {0.0f, -1.0f}, {-0.25f, -0.75f}, {-0.5f, -0.5f}, {-0.25f, -0.25f}};
void loop(void)
{

    for (int i = 0; i < 16; i++)
    {
        robotA.localize();
        robotA.moveTo(positions[i][0], positions[i][1]);
    }
    robotA.localize();
    robotA.moveTo(0.0f, 0.0f);
    delay(5000);
}
