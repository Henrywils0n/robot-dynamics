#include <math.h>
#include "RobotControl.h"

void setup(void)
{
    Serial.begin(9600);
}

Robot robotA(0, 0, 0);

void loop(void)
{

    robotA.moveTo(0, 1);
    robotA.moveTo(0, 0);
}
