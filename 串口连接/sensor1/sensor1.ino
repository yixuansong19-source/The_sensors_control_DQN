#include <Servo.h>
#include <SoftwareSerial.h>

#define trigPin   5
#define  echoPin   4         
#define  ServoPin  3

char receive[50]={0};
int distance[100]={0};
int speed=0;
int angle=0;

Servo baseServo;

void setup() {
  Serial.begin(9600);    // 初始化主串口

  pinMode(trigPin, OUTPUT);       
  pinMode(echoPin, INPUT);        
  baseServo.attach(ServoPin);

  baseServo.write(0);
  
  memset(receive,0,sizeof(receive));
  memset(distance,0,sizeof(distance));
  
  clear();
}

void loop() { 
  if (Serial.available())//检测到虚拟串口有数据开始分析数据 
  {
    delay(100);
    int i=0;
    while (Serial.available())
    {
      receive[i]=Serial.read();
      i++;
    }

    //receive[0]='1'//测试

    Serial.print("on/off:");
    if(receive[0]=='0')
    {
      Serial.println("off");
      clear();
    }
    if(receive[0]>'0')
    {
      Serial.println("on");
      speed=20;
      angle=servo(speed,distance);
      baseServo.write(0);
    }else
    {
      baseServo.write(0);
    }
    memset(receive,0,sizeof(receive));
    clear();
    String distanceData = "";
    distanceData = "\n" + String(angle) + "," + String(distance[ angle / 2 ])  ;  // 角度,距离
    Serial.println(distanceData);
    Serial.println("END");
    clear();
  }
}

int servo(int speed, int* distance) {
  int flag=0;
  for (int x = 0; x < 180; x += 2) {
    int i=x/2;  //舵机步长为2，相应角度的编号=角度/2
    baseServo.write(x);
    distance[i] = calculateDistance();
    if(flag == 1 && distance[i] == 99 )
    {
      Serial.print('\n');
      Serial.print(distance[i - 1]);
      //Serial.println("\nServo scan complete.");
      return x - 2;
    }
    if( distance[i] < 50 && flag == 0 ) 
      flag=1;
    Serial.print(distance[i]);
    Serial.print(" ");
    delay(speed);
    
  }
  //Serial.println("\nServo scan complete.");
  return 178;
}

int calculateDistance()
{
  int distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  distance = pulseIn(echoPin, HIGH) * 0.034 / 2;
  
  if(distance<15)
    return distance;
  else
    return 99;
}
void clear()
{
  delay(100);
   while (Serial.available()) {
    Serial.read(); // 读取并丢弃缓存区中的数据
  }
}