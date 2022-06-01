#include "RobotControl.h"
void setup(void)
{
    Serial.begin(9600);
}

Robot robotA(0, 0, pi / 2);

void loop(void)
{

    robotA.moveTo(0, 1);
    robotA.moveTo(0.5, 0.5);
    robotA.moveTo(0, 0);
}
