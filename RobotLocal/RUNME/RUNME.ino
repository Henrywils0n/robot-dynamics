
#include <math.h>
#include "mainRobotClass.h"

void setup(void)
{
    Serial.begin(9600);
}

Robot robotA(0, 0, 0);

void loop(void)
{
    robotA.sendTransmission(3.14);
    delay(1000);
}
