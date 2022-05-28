
#include <math.h>
#include <Adafruit_LSM9DS0.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <SPI.h>
#include "mainRobotClass.h"

void setup(void)
{
    Serial.begin(9600);
}

Robot robotA(0, 0, 0);

void loop(void)
{
    robotA.moveTo(0, 1);
    digitalWrite(INDICATORLED, HIGH);
    delay(1000);
    digitalWrite(INDICATORLED, LOW);
    robotA.moveTo(0, 0);
}
