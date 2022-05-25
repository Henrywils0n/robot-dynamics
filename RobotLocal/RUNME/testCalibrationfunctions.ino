// to use paste the function into the robot class to run the test script// function to just run the motor full out and calculate the angular velocity
void calibrateAngularV()
{
    digitalWrite(DIRR, 1);
    digitalWrite(DIRL, 1);
    analogWrite(PWMR, 255);
    analogWrite(PWML, 255);
    prevLeftEncoderTicks = leftEncoderTicks;
    prevRightEncoderTicks = rightEncoderTicks;
    int start = millis();
    while (1)
    {
        int diffLeft = leftEncoderTicks - prevLeftEncoderTicks;
        int diffRight = rightEncoderTicks - prevRightEncoderTicks;
        float WR = (diffRight * pi / 192) / (millis() - start) * 1000;
        float WL = (diffLeft * pi / 192) / (millis() - start) * 1000;
        Serial.print("WR, ");
        Serial.print(WR);
        Serial.print("\n");
        Serial.print("WL, ");
        Serial.print(WL);
        Serial.print("\n");
        prevLeftEncoderTicks = leftEncoderTicks;
        prevRightEncoderTicks = rightEncoderTicks;
        start = millis();
        delay(250);
    }
}
// function slowly increments the speed to find the minimum input to get it to move
void calibrateMotorMin()
{
    digitalWrite(DIRR, 1);
    digitalWrite(DIRL, 1);
    analogWrite(PWMR, 0);
    analogWrite(PWML, 0);
    int speed = 0;
    while (true)
    {
        analogWrite(PWMR, speed);
        analogWrite(PWML, speed);
        Serial.println(speed);
        speed++;
        delay(5000);
    }
}
// blank function used for test purposes
void test(void)
{
    digitalWrite(DIRR, 1);
    digitalWrite(DIRL, 1);
    analogWrite(PWMR, 255);
    analogWrite(PWML, 0);
    delay(5000);
    analogWrite(PWMR, 0);
}