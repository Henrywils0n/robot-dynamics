#include <math.h>
#include <ArduinoJson.h>
// Pin definitions
#define DIRR 7  // Direction control for motor B
#define DIRL 8  // Direction control for motor A
#define PWML 9  // PWM control (speed) for motor A
#define PWMR 10 // PWM control (speed) for motor B
#define leftEncoder 2
#define rightEncoder 3
// Encoder ticks and interrupt functions are global because it wouldn't compile with them as members and methods
unsigned int leftEncoderTicks = 0;
unsigned int rightEncoderTicks = 0;
float pi = M_PI;
// Interrupts for encoders
void incrementLeftEncoder()
{
    leftEncoderTicks++;
}
void incrementRightEncoder()
{
    rightEncoderTicks++;
}
// Clears the encoder ticks to prevent overflow
void clearLeftEncoder()
{
    leftEncoderTicks = 0;
}
void clearRightEncoder()
{
    rightEncoderTicks = 0;
}
// same as fix theta but it changes a given angle instead of the robot heading
float fixAngle(float angle)
{
    while (angle > pi)
    {
        angle -= 2.0f * pi;
    }
    while (angle < -pi)
    {
        angle += 2.0f * pi;
    }
    return angle;
}
// Robot class for controlling the robot
class Robot
{
public:
    // position of the robot on the grid
    float x, y, theta;
    // robot id
    int id;
    // address of the server
    String serverAddress;
    // sets up required pin modes and objects
    Robot(float X, float Y, float THETA, int ID, String address)
    {
        // sets the position and heading to the specified values
        x = X;
        y = Y;
        theta = THETA;
        id = ID;
        serverAddress = address;
        // initializes the motor controller
        setupArdumoto();
        // initializes the encoders and interrupts
        pinMode(leftEncoder, INPUT_PULLUP);
        pinMode(rightEncoder, INPUT_PULLUP);
        attachInterrupt(digitalPinToInterrupt(leftEncoder), incrementLeftEncoder, CHANGE);
        attachInterrupt(digitalPinToInterrupt(rightEncoder), incrementRightEncoder, CHANGE);
    }
    // send x,y position and the robot will move to that position
    void moveTo(float X, float Y)
    {
        // variables for the PID controller
        float integral = 0;
        float derivative = 0;
        float integralTheta = 0;
        float derivativeTheta = 0;
        float prevDirectionalErr;
        float prevThetaErr;
        int prevTime = micros();
        int currentTime;
        float directionalErr;

        // absolute positional error
        float err = sqrt(pow(X - x, 2) + pow(Y - y, 2));
        // angle error
        float thetaErr = fixAngle(atan2(Y - y, X - x) - theta);
        // used for debugging
        putPosition();
        putData(err, thetaErr, 0.0f);
        //  continues to drive while the absolute positional Error on position is greater than the tolerance of Err
        while (err > Err)
        {
            // updates position, time, and error
            // putPosition();
            updatePosition();
            currentTime = micros();
            err = sqrt(pow(X - x, 2) + pow(Y - y, 2));
            thetaErr = atan2(Y - y, X - x) - theta;
            // multiplying by the cosine of the angle error to return directionality to the
            // absolute error (this will also cause the robot to drive in reverse and set the speed
            // according to how productive moving forward or backward is)
            directionalErr = err * cos(thetaErr);
            // flips the error by 180 degrees if the robot is driving backwards
            if (directionalErr < 0.0f)
            {
                thetaErr = fixAngle(thetaErr - pi);
            }
            // PID control for the linear and angular velocity
            derivative = (directionalErr - prevDirectionalErr) / (currentTime - prevTime) * 1000000;
            integral += directionalErr * (currentTime - prevTime) / 1000000;
            integralTheta += thetaErr * (currentTime - prevTime) / 1000000;
            derivativeTheta = (thetaErr - prevThetaErr) / (currentTime - prevTime) * 1000000;
            prevTime = currentTime;
            prevDirectionalErr = directionalErr;
            prevThetaErr = thetaErr;
            // sets the linear and angular velocity
            float v = Kp * directionalErr + Ki * integral + Kd * derivative;
            float w = KpTheta * thetaErr + KiTheta * integralTheta + KdTheta * derivativeTheta;
            // sets the speed of the robot
            drive(v, w);
            // debug print statements for absolute and angular errors
            /*
            Serial.print(err);
            Serial.print(thetaErr);
            Serial.print("\n");
            */
            // debug print statements for position and heading
            /*
            Serial.print("(");
            Serial.print(x);
            Serial.print(",");
            Serial.print(y);
            Serial.print(",");
            Serial.print(theta);
            Serial.print(")\n");
            */
        }
        // set the speed to zero once the new position is reached
        drive(0, 0);
    }

    // moves the robot at velocity v and angular velocity w
    void drive(float v, float w)
    {
        // angular velocities
        float wR = (v + R * w) / r;
        float wL = (v - R * w) / r;
        // set Directions according to the speed
        // 1 moves forward, 0 moves backward (if this isn't true on a robot flip the wires going to the motor)
        if (wR > 0)
        {
            DirWR = 1;
        }
        else
        {
            DirWR = 0;
        }
        if (wL > 0)
        {
            DirWL = 1;
        }
        else
        {
            DirWL = 0;
        }
        // using the calibrated values convert the speed to the correct PWM values
        // robot starts moving at 103 (on laplace)
        // at max reading W of each wheel is about 19.5 on the floor(precision does not really matter its just helpful)
        // set the max left wheel speed a little higher to account for differences in the motors to make it drive straighter
        int WR = map(abs(wR), 0, 19.5, 76, 255);
        int WL = map(abs(wL), 0, 19.5, 76, 255);
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
    void localize()
    {
        String address = serverAddress + "/agents/" + id;
        // sends the address of the get request to the ESP8266
        StaticJsonDocument<200> req;
        req["type"] = "GET";
        req["address"] = address;
        serializeJson(req, Serial);
        req.clear();
        // waits for the ESP8266 to send the data
        while (1)
        {
            if (Serial.available())
            {
                // loads the data into the json document
                StaticJsonDocument<200> doc;
                DeserializationError error = deserializeJson(doc, Serial);
                // if the data is not valid try again until it is
                if (error != DeserializationError::Ok)
                {
                    localize();
                    return;
                }
                else
                {
                    x = doc["position"][0];
                    y = doc["position"][1];
                    theta = doc["position"][2];
                    doc.clear();
                    clearLeftEncoder();
                    clearRightEncoder();
                    return;
                }
            }
        }
    }
    void putPosition()
    {
        String address = serverAddress + "/agentsLocal/" + id;
        // sends the address of the get request to the ESP8266
        StaticJsonDocument<200> req;

        req["type"] = "PUT";
        req["address"] = address;
        req["id"] = id;
        JsonArray position = req.createNestedArray("position");
        position.add(x);
        position.add(y);
        position.add(theta);
        serializeJson(req, Serial);
        req.clear();
    }
    void putData(float d1, float d2, float d3)
    {
        String address = serverAddress + "/agentsLocal/" + id;
        // sends the address of the get request to the ESP8266
        StaticJsonDocument<200> req;

        req["type"] = "PUT";
        req["address"] = address;
        req["id"] = id + 1;
        JsonArray position = req.createNestedArray("position");
        position.add(d1);
        position.add(d2);
        position.add(d3);
        serializeJson(req, Serial);
        req.clear();
    }

private:
    // radius of the wheels
    float r = 0.034;
    // radius from the centre to the wheel
    float R = 0.082;
    // direction of each wheel, 1 is forward, 0 is backward
    uint8_t DirWL = 1;
    uint8_t DirWR = 1;
    // Linear velocity gains
    float Kp = 1.5;
    float Ki = 0.005;
    float Kd = 0.5;
    // Angular velocity gains
    float KpTheta = 11;
    float KiTheta = 1;
    float KdTheta = 1.5;
    // Acceptable position error
    float Err = 0.03;

    // updates the position estimate of the robot based on the encoders
    void updatePosition()
    {
        // encoder ticks since last update
        int diffLeft = leftEncoderTicks;
        clearLeftEncoder();
        int diffRight = rightEncoderTicks;
        clearRightEncoder();
        // angle change since last update
        float dTheta = 0;
        float dL = 0;
        if (DirWL)
        {
            dTheta -= diffLeft;
            dL += diffLeft;
        }
        else
        {
            dTheta += diffLeft;
            dL -= diffLeft;
        }
        if (DirWR)
        {
            dTheta += diffRight;
            dL += diffRight;
        }
        else
        {
            dTheta -= diffRight;
            dL -= diffRight;
        }
        dL *= pi / 384.0f * r;
        dTheta *= pi / 384.0f * r / R;

        // calculating the new position
        float EncoderdX = dL * cos(theta + 0.5f * dTheta);
        float EncoderdY = dL * sin(theta + 0.5f * dTheta);
        theta += (dTheta);
        fixTheta();
        x += EncoderdX;
        y += EncoderdY;
    }

    // returns theta to the bounds +/-pi
    void fixTheta()
    {
        while (theta > pi)
        {
            theta -= 2.0f * pi;
        }
        while (theta < -pi)
        {
            theta += 2.0f * pi;
        }
    }

    // sets up the motor controller
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
};
