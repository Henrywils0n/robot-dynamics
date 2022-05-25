
#include <math.h>
#include "mainRobotClass.h"

void setup(void)
{
    Serial.begin(9600);
}

Robot robotA(0, 0, pi / 2);

void loop(void)
{
    robotA.moveTo(0, 1);
    delay(10000);
}
