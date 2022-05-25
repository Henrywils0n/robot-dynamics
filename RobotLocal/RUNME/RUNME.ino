
#include <math.h>
#include "mainRobotClass.h"

void setup(void)
{
    Serial.begin(9600);
}

Robot robotA(0, 0, pi / 2);

void loop(void)
{
    robotA.moveTo(-0.25, 0);
    robotA.moveTo(-0.5, 0);
    robotA.moveTo(-1, 0);
    delay(10000);
}
