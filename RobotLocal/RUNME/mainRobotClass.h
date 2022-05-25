// motor A is left, B is right
#define DIRR 7                       // Direction control for motor B
#define DIRL 8                       // Direction control for motor A
#define PWML 9                       // PWM control (speed) for motor A
#define PWMR 10                      // PWM control (speed) for motor B
#define hostAddress 0013A20041466E40 // MY address of the host XBee
#define leftEncoder 2
#define rightEncoder 3
unsigned int leftEncoderTicks = 0;
unsigned int rightEncoderTicks = 0;
float pi = 3.14159265358979323846;
float Err = 0.02;
void setupArdumoto()
{
    // All pins should be setup as outputs:
    pinMode(PWML, OUTPUT);
    pinMode(PWMR, OUTPUT);
    pinMode(DIRL, OUTPUT);
    pinMode(DIRR, OUTPUT);

    // Initialize all pins as low:
    digitalWrite(PWML, LOW);
    digitalWrite(PWMR, LOW);
    digitalWrite(DIRL, LOW);
    digitalWrite(DIRR, LOW);
}
void incrementLeftEncoder()
{
    leftEncoderTicks++;
}
void incrementRightEncoder()
{
    rightEncoderTicks++;
}
void clearLeftEncoder()
{
    leftEncoderTicks = 0;
}
void clearRightEncoder()
{
    rightEncoderTicks = 0;
}
class Robot
{
public:
    // radius of the wheels
    float r = 0.033;
    // radius from the centre to the wheel
    float R = 0.08;
    // position of the robot on the grid
    float x, y, theta;
    byte DirWL, DirWR;
    int prevLeftEncoderTicks = 0;
    int prevRightEncoderTicks = 0;
    // sets up each board and should initialize communication with the xbee's
    Robot(float X, float Y, float THETA)
    {
        x = X;
        y = Y;
        theta = THETA;
        setupArdumoto();
        pinMode(leftEncoder, INPUT_PULLUP);
        pinMode(rightEncoder, INPUT_PULLUP);
        attachInterrupt(digitalPinToInterrupt(leftEncoder), incrementLeftEncoder, CHANGE);
        attachInterrupt(digitalPinToInterrupt(rightEncoder), incrementRightEncoder, CHANGE);
    }

    // moves the robot at velocity v and angular velocity w
    void drive(float v, float w)
    {
        // angular velocities
        float wR = (v + R * w) / r;
        float wL = (v - R * w) / r;
        // set Directions according to the speed
        // 1 moves forward, -1 moves backward (if this isnt true on a robot flip the wires going to the motor)
        DirWL = -1 + 2 * (wL >= 0);
        DirWR = -1 + 2 * (wR >= 0);
        // using the calibrated values convert the speed to the correct PWM values
        // robot starts moving at 103 (on laplace)
        // at max reading W of each wheel is about 19.5 on the floor(precision does not really matter its just helpful)
        // testing without the floor shows the left motor on laplace being about a little faster (should test on each robot to have the robot drive straighter)
        // this map is linear but the velocity is not (doesent really matter because of pid control)
        int WR = map(abs(wR), 0, 19.2, 75, 255);
        int WL = map(abs(wL), 0, 20.5, 75, 255);
        // setting cutoffs for the motors
        if (WR > 255)
            WR = 255;
        else if (WR <= 75)
            WR = 0;
        if (WL > 255)
            WL = 255;
        else if (WL <= 75)
            WL = 0;
        // sending signal to the motors
        digitalWrite(DIRR, DirWR);
        digitalWrite(DIRL, DirWL);
        analogWrite(PWMR, WR);
        analogWrite(PWML, WL);
    }
    void moveTo(float X, float Y)
    {
        int prevLEncoder = leftEncoderTicks;
        int prevREncoder = rightEncoderTicks;
        float err = sqrt(pow(X - x, 2) + pow(Y - y, 2));
        while (err > Err)
        {
            int diffLeft = leftEncoderTicks;
            clearLeftEncoder();
            int diffRight = rightEncoderTicks;
            clearRightEncoder();
            float dL = (diffLeft * DirWL + diffRight * DirWR) * pi / 192 * r * 0.5;
            float dTheta = (diffRight * DirWR - diffLeft * DirWL) * pi / 192 * r / R * 0.5;
            float dX = dL * cos(theta);
            float dY = dL * sin(theta);
            x += dX;
            y += dY;
            theta += dTheta;
            fixTheta();
            err = sqrt(pow(X - x, 2) + pow(Y - y, 2));
            float targetTheta = atan2(Y - y, X - x);
            drive(err * 0.5 * (targetTheta - theta < pi / 4), (targetTheta - theta) * 1);
            // delay(10)
            Serial.print("(");
            Serial.print(x);
            Serial.print(",");
            Serial.print(y);
            Serial.print(",");
            Serial.print(theta);
            Serial.print(")\n");
        }
        drive(0, 0);
    }
    void fixTheta()
    {
        while (theta > pi)
        {
            theta -= 2 * pi;
        }
        while (theta < -pi)
        {
            theta += 2 * pi;
        }
    }
    // function to just run the motor full out and calculate the angular velocity
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
    // function that moves the robot to a certain position
};
