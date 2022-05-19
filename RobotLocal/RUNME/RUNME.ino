
#include <math.h>
#include "mainRobotClass.h"

Robot robotA(0, 0, 0);
void setup(void)
{
    Serial.begin(9600);
}

void loop(void)
{
    robotA.sendMessage('Z');
    delay(5000);
}
