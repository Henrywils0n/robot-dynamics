#include "RobotControl.h"
#define id 1
String server = "http://192.168.0.181:3000";
void setup(void)
{
  Serial.begin(115200);
}



void loop(void)
{
  Robot robotA(0, 0, pi / 2, id, server);
  robotA.getPath(1);
  int idx = robotA.pathDoc["id"].as<int>( );
  int total = robotA.pathDoc["total"].as<int>();
  while (idx <= total)
  {
    robotA.getPath(idx);
    int len = robotA.pathDoc["path"].size();
    Serial.println(len);
    for (int i = 0; i < len; i++)
    {
      int sucsess = 0;
      while (!sucsess) {
        sucsess = robotA.localize();
      }
      robotA.moveTo(robotA.pathDoc["path"][i][0].as<float>(), robotA.pathDoc["path"][i][1].as<float>());
    }
    idx++;

  }
  delay(5000);
}
