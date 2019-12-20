#include <Arm7Bot.h>
Arm7Bot arm;

double pullup1[7] =  {20, 150,40, 90, 90, 180, 30};
double pullup2[7] =  {160, 150, 40, 90, 90, 180, 30};
double pullside1[7] =  {20, 150,40, 90, 90, 180, 30};
double pullside2[7] =  {160, 150, 40, 90, 90, 180, 30};
double drop1[7] =  {10, 150, 40, 90, 90, 180, 70};
double drop2[7] =  {160, 150, 40, 90, 90, 180, 70};
double test1[7] =  {90, 115, 60, 90, 180, 90, 30};
double test2[7] =  {90, 115, 60, 90, 160, 90, 70};
bool choice = 0;
double xyzc[4] = {.32 ,0,-.0254,0};
double xyzc2[4] = {.32 ,.1 ,-.0254,1};
const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data
boolean newData = false;

void moveRobot(char* my_str){
  //String stringOne =  String(input[1], 3);
  //char* my_str = strdup(myAngle.data);
    // Declaration of delimiter 
  const char s[4] = ","; 
  char* tok; 
    // Use of strtok 
    // get first token
  tok = strtok(my_str, s); 
    // Checks for delimeter 
  int count = 0;
  double* input = new double[3];
  while (tok != 0) { 
    input[count] = strtod(tok, NULL);
        // Use of strtok 
        // go through other tokens 
    tok = strtok(0, s); 
    count++;
  }
  test(input);
}

void recvWithEndMarker() {
    static byte ndx = 0;
    char endMarker = 'a';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (rc != endMarker) {
             receivedChars[ndx] = rc;
            ndx++;
            if (ndx >= numChars) {
                ndx = numChars - 1;
            }
        }
        else {
            receivedChars[ndx] = '\0'; // terminate the string
            ndx = 0;
            newData = true;
        }
    }
}

void showNewData() {
    if (newData == true) {
        Serial.println("This just in ... ");
        Serial.println(receivedChars);
        Serial.println(receivedChars);
        delay(1000);
        moveRobot(receivedChars);
        newData = false;
    }
}
    
void test(double* var) {
  double theta = atan2(var[1],var[0])*4068/71;
  double a1 = theta + 90 + 60;
  double newx = var[0] * sin(71.0/4068.0*abs(90 - theta));
  double a2 = 32 + 10.0/.06 * (.37 - newx);
  double a3 = 78 + 10.0/.06 * (.37 - newx);
  double a4 = 90; //don't change
  double a5 = 180 + (60 - a3); 
  //double a6 = 90 - theta;
  double a6 = 90;
  double a7 = 70; //gripper
  double test[7] =  {a1, a2, a3, a4, a5, a6, a7};
  arm.move(test);
  test[2] = a3 + 5;
  test[0] = a1 - 50;
  delay(3000);
  arm.move(test);
  delay(3000);
  test[6] = 30;
  arm.move(test);
  delay(3000);
  if (var[3] == 0) {
    arm.move(pullup1);
    delay(3000);
    arm.move(pullside1);
    delay(3000);
    arm.move(drop1);
  } else {
    arm.move(pullup2);
    delay(3000);
    arm.move(pullside2);
    delay(3000);
    arm.move(drop2);
  }
  delay(1000);
  
}

void setup()
{
  Serial.begin(9600);
  // initial 7Bot Arm
  arm.initialMove();
  // change speed to 30
  //arm.maxSpeed[0] = 30;

}

void loop() {
  delay(10);// must be added.
  recvWithEndMarker();
  showNewData();
}
