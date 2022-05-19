Robot robotA();
void setup(void)
{
    Serial.begin(9600);
}

void loop(void)
{
    robotA.Move(10, 10);
}