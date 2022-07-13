#include <ArduinoJson.h>

void setup()
{
  Serial.begin(115200);

}

void loop()
{
    char serverAddress[] = "http://192.168.0.181:3000";
  int id = 1;
  int idx = 1;
char address[100];
        strcpy(address, serverAddress);
        strcat(address,"/goal");
        char tempchar[1] = {id + '0'};
        strcat(address,tempchar);
        strcat(address, "/");
        tempchar[0] = idx + '0';
        strcat(address, tempchar);
        Serial.println(address);
}
