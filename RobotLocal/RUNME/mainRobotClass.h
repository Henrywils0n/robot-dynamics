// motor A is left, B is right
#define DIRR 7                       // Direction control for motor B
#define DIRL 8                       // Direction control for motor A
#define PWML 9                       // PWM control (speed) for motor A
#define PWMR 10                      // PWM control (speed) for motor B
#define INDICATORLED 13              // LED to indicate when robot reaches position
#define hostAddress 0013A20041466E40 // MY address of the host XBee
#define leftEncoder 2
#define rightEncoder 3

unsigned int leftEncoderTicks = 0;
unsigned int rightEncoderTicks = 0;
float pi = 3.14159265358979323846;
float Err = 0.03;
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
    float r = 0.034;
    // radius from the centre to the wheel
    float R = 0.079;
    // position of the robot on the grid
    float x, y, theta;
    byte DirWL, DirWR;
    int prevLeftEncoderTicks = 0;
    int prevRightEncoderTicks = 0;
    // Linear velocity gains
    float Kp = 1.5;
    float Ki = 0.005;
    float Kd = 0.5;
    // Angular velocity gains
    float KpTheta = 11;
    float KiTheta = 1;
    float KdTheta = 1.5;
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
        pinMode(INDICATORLED, OUTPUT);
    }

    // moves the robot at velocity v and angular velocity w
    void drive(float v, float w)
    {
        // angular velocities
        float wR = (v + R * w) / r;
        float wL = (v - R * w) / r;
        // set Directions according to the speed
        // 1 moves forward, 0 moves backward (if this isn't true on a robot flip the wires going to the motor)
        DirWL = (wL >= 0);
        DirWR = (wR >= 0);
        // using the calibrated values convert the speed to the correct PWM values
        // robot starts moving at 103 (on laplace)
        // at max reading W of each wheel is about 19.5 on the floor(precision does not really matter its just helpful)
        int WR = map(abs(wR), 0, 19.5, 76, 255);
        int WL = map(abs(wL), 0, 19.8, 76, 255);
        // setting cutoffs for the motors
        if (WR > 255)
            WR = 255;
        else if (abs(wR) <= 0.25)
            WR = 0;
        if (WL > 255)
            WL = 255;
        else if (abs(wL) <= 0.25)
            WL = 0;
        // sending signal to the motors
        digitalWrite(DIRR, DirWR);
        digitalWrite(DIRL, DirWL);
        analogWrite(PWMR, WR);
        analogWrite(PWML, WL);
    }
    // updates the position estimate of the robot based on the encoders
    // TO DO add accelerometer, gyroscope, and magnetometer to the estimates
    void updatePosition()
    {

        int diffLeft = leftEncoderTicks;
        clearLeftEncoder();
        int diffRight = rightEncoderTicks;
        clearRightEncoder();
        float dL = (diffLeft * (-1 + 2 * DirWL) + diffRight * (-1 + 2 * DirWR)) * pi / 192 * r * 0.5;
        float EncoderdTheta = (diffRight * (-1 + 2 * DirWR) - diffLeft * (-1 + 2 * DirWL)) * pi / 192 * r / R * 0.5;
        float EncoderdX = dL * cos(theta);
        float EncoderdY = dL * sin(theta);
        x += EncoderdX;
        y += EncoderdY;
        theta += EncoderdTheta;
        fixTheta();
    }
    // send x,y position and the robot will move to that position
    void moveTo(float X, float Y)
    {
        float integral = 0;
        float derivative = 0;
        float integralTheta = 0;
        float derivativeTheta = 0;
        float prevErr;
        float prevThetaErr;

        int prevTime = micros();
        int currentTime;
        float directionalErr;
        float err = sqrt(pow(X - x, 2) + pow(Y - y, 2));
        float thetaErr = fixAngle(atan2(Y - y, X - x) - theta);
        // continues to drive while the positional Error on position is greater than the tolerance of Err
        while (err > Err)
        {
            // updates position, time, and error
            updatePosition();
            currentTime = micros();
            err = sqrt(pow(X - x, 2) + pow(Y - y, 2));
            thetaErr = atan2(Y - y, X - x) - theta;
            // multiplying by the cosine of the angle to return directionality to the absolute error (this will also cause the robot to drive in reverse and drive slower when forwards or reverse is not as productive a direction)
            directionalErr = err * cos(thetaErr);
            // flips the error by 180 degrees if the robot is driving backwards
            if (directionalErr < 0)
            {
                thetaErr = fixAngle(thetaErr - pi);
            }
            // PID control for the linear and angular velocity
            derivative = (directionalErr - prevErr) / (currentTime - prevTime) * 1000000;
            integral += directionalErr * (currentTime - prevTime) / 1000000;
            integralTheta += thetaErr * (currentTime - prevTime) / 1000000;
            derivativeTheta = (thetaErr - prevThetaErr) / (currentTime - prevTime) * 1000000;
            prevTime = currentTime;
            prevErr = directionalErr;
            prevThetaErr = thetaErr;
            float v = Kp * directionalErr + Ki * integral + Kd * derivative;
            float w = KpTheta * thetaErr + KiTheta * integralTheta + KdTheta * derivativeTheta;
            drive(v, w);
            // setting a slight delay to ensure that sufficient encoder ticks are captured
            delay(5);
            /*
            Serial.print(err);
            Serial.print(thetaErr);
            Serial.print("\n");
            */

            Serial.print("(");
            Serial.print(x);
            Serial.print(",");
            Serial.print(y);
            Serial.print(",");
            Serial.print(theta);
            Serial.print(")\n");
        }
        // stop the robot
        drive(0, 0);
    }
    // returns theta to the bounds +/-pi
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
    // same as fix theta but it changes a given angle instead of the robot heading
    float fixAngle(float angle)
    {
        while (angle > pi)
        {
            angle -= 2 * pi;
        }
        while (angle < -pi)
        {
            angle += 2 * pi;
        }
        return angle;
    }
};
