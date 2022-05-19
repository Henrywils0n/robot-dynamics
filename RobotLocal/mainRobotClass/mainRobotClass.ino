#define DIRB 7  // Direction control for motor B
#define DIRA 8  // Direction control for motor A
#define PWMA 9  // PWM control (speed) for motor A
#define PWMB 10 // PWM control (speed) for motor B
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
private:
    // radius of the wheels
    float r = 0.034;
    // radius from the centre to the wheel
    float R = 0.08;
    // position of the robot on the grid
    float x, y, theta;
    // sets up each board and should initialize communication with the xbee's

public:
    void Robot(void)
    {
        setupArdumoto();
    }
    // moves the robot at velocity v and angular velocity w
    void Move(float v, float w)
    {
        float wR = (v + R * w) / r;
        float wL = (v - R * w) / r;
        // set Directions according to the speed
        byte DirWL = 1;
        byte DirWR = 1;
        // using the calibrated values convert the speed to the correct PWM values
        int WR = 255;
        int WL = 255;
        // sending signal to the motors
        digitalWrite(DIRB, DirWR);
        digitalWrite(DIRA, DirWL);
        analogWrite(PWMB, WR);
        analogWrite(PWMA, WL);
    }
    // function that moves the robot to a certain position
};
Robot robotA();
void setup(void)
{
    Serial.begin(9600);
}

void loop(void)
{
    robotA.Move(10, 10);
}
