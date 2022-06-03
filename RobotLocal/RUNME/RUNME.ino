#include "RobotControl.h"
#define LEDPIN 13
void setup(void)
{
    Serial.begin(9600);
    pinMode(LEDPIN, OUTPUT);
    digitalWrite(LEDPIN, HIGH);
}

Robot robotA(0, 0, pi / 2);

void loop(void)
{
    robotA.moveTo(0, 1);
    robotA.moveTo(0, 0);
}
