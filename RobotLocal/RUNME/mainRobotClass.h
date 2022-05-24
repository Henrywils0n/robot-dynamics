#include <SoftwareSerial.h>
#include <XBee.h>
// motor A is left, B is right
#define DIRB 7             // Direction control for motor B
#define DIRA 8             // Direction control for motor A
#define PWMA 9             // PWM control (speed) for motor A
#define PWMB 10            // PWM control (speed) for motor B
#define hostAddress 0xBEEF // MY address of the host XBee
XBee xbee = XBee();
// union used to convert the float to binary data so it can be sent over the XBee
union payload
{
    float floatVal;
    uint8_t binary[sizeof(float)];
};
void setupArdumoto()
{
    // All pins should be setup as outputs:
    pinMode(PWMA, OUTPUT);
    pinMode(PWMB, OUTPUT);
    pinMode(DIRA, OUTPUT);
    pinMode(DIRB, OUTPUT);

    // Initialize all pins as low:
    digitalWrite(PWMA, LOW);
    digitalWrite(PWMB, LOW);
    digitalWrite(DIRA, LOW);
    digitalWrite(DIRB, LOW);
}

class Robot
{
public:
    // radius of the wheels
    float r = 0.034;
    // radius from the centre to the wheel
    float R = 0.08;
    // position of the robot on the grid
    float x, y, theta;

    // sets up each board and should initialize communication with the xbee's
    Robot(float X, float Y, float THETA)
    {
        x = X;
        y = Y;
        theta = THETA;
        setupArdumoto();
        xbee.setSerial(Serial);
    }

    // moves the robot at velocity v and angular velocity w
    void drive(float v, float w)
    {
        // angular velocities
        float wR = (v + R * w) / r;
        float wL = (v - R * w) / r;
        // set Directions according to the speed
        // 1 moves forward, -1 moves backward (if this isnt true on a robot flip the wires going to the motor)
        byte DirWL = -1 + 2 * (wL >= 0);
        byte DirWR = -1 + 2 * (wR >= 0);
        // using the calibrated values convert the speed to the correct PWM values
        // min apears to be about 100 to get it to move????
        int WR = 1 * v;
        int WL = 1 * v;
        // sending signal to the motors
        digitalWrite(DIRB, DirWR);
        digitalWrite(DIRA, DirWL);
        analogWrite(PWMB, WR);
        analogWrite(PWMA, WL);
    }
    // function sends a float to the host
    void sendTransmission(float message)
    {
        payload Payload;
        Payload.floatVal = message;
        Tx16Request tx = Tx16Request(hostAddress, Payload.binary, sizeof(Payload.binary));
        TxStatusResponse txStatus = TxStatusResponse();
        xbee.send(tx);
    }
    // function that moves the robot to a certain position
};
