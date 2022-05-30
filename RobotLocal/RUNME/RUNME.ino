
#include <math.h>
#include <Adafruit_LSM9DS0.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <SPI.h>
#include "mainRobotClass.h"

void setup(void)
{
    Serial.begin(9600);
    if (!lsm.begin())
    {
        Serial.println("Oops ... unable to initialize the LSM9DS0. Check your wiring!");
        while (1)
            ;
    }
    setupSensor();
}

Robot robotA(0, 0, 0);

void loop(void)
{

    robotA.moveTo(0, 1);
    robotA.moveTo(0, 0);
}
