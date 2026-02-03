#include <Servo.h>
#include <SoftwareSerial.h>

#define  trigPin   5         
#define  echoPin   4         
#define  ServoPin  3

String localaddr="3";
String targetaddr="10";
char receive[50]={0};
int distance[100]={0};
unsigned long previousMillis = 0;
const unsigned long interval = 1000;
unsigned char function=0;//接收：0，发送：1
unsigned int speed=0;

SoftwareSerial mySerial(11, 10);  // RX = 11, TX = 10
Servo baseServo;

String setlocal="AT+CADDRSET="+localaddr+"\r\n";
String settarget="AT+CTXADDRSET="+targetaddr+"\r\n";

void setup() {
  Serial.begin(9600);    // 初始化主串口
  mySerial.begin(9600);  // 初始化虚拟串

  randomSeed(analogRead(0));  // 用模拟引脚生成随机种子

  pinMode(trigPin, OUTPUT);       
  pinMode(echoPin, INPUT);        
  baseServo.attach(ServoPin);

  baseServo.write(0);
  clear();
  sendATCommand(setlocal);//设置本机地址：13
  sendATCommand("AT+CRXS=470500000,5,0,1,1\r\n");
}

void loop() {
  int angle=0;
  if(function==0)
  {
    memset(receive,0,sizeof(receive));
    memset(distance,0,sizeof(distance));
    clear();//接收模式初始化
    
    //mySerial.println("1");
    delay(100); 
    if (mySerial.available())//检测到虚拟串口有数据开始分析数据 
    {
      delay(100);
      int i=0;
      while (mySerial.available())
      {
        receive[i]=mySerial.read();
        i++;
      }// 将虚拟串口数据输出到主串口

      //receive[17]='1';receive[18]='1';//测试

      Serial.print("on/off:");
      Serial.println(receive[17]);

      Serial.print("speed:");
      Serial.println(receive[18]);
      clear();
      if(receive[17]!=0)
      {
        speed=20;
        angle=servo(speed,distance);
        baseServo.write(0);
        function=1;
      }else
      {
        baseServo.write(0);
        function=0;
      }
      memset(receive,0,sizeof(receive));
      clear();
    }
    clear();
  }
  if(function==1)
  {
    delay(3000);
    sendATCommand(settarget);//设置发送目标：12
    sendATCommand("AT+CTX=470500000,5,0,1,21,1\r\n");
    clear();
    delay(100);
    while (mySerial.available()) {
      Serial.write(mySerial.read());  // 将虚拟串口数据输出到主串口
    }

    while (Serial.available()) {
      mySerial.write(Serial.read());  // 将主串口数据发送到虚拟串口
    }

    //generateRandomDistances(distance);  // 替换掉真实测距

    String distanceData = "";
    distanceData = String(angle) + "," + String(distance[ angle / 2 ]) + "," + String(localaddr);  // 角度,距离
    mySerial.println(distanceData);
    Serial.println(distanceData);
      
    /*while (mySerial.available()) {
      Serial.write(mySerial.read());  // 将虚拟串口数据输出到主串口
    }
    while (Serial.available()) {
      mySerial.write(Serial.read());  // 将主串口数据发送到虚拟串口
    }*/

    clear();

    delay(100);
    sendATCommand("+++\r\n");//退出发送模式
    delay(100);
    function=0;
    clear();
    sendATCommand("AT+CRXS=470500000,5,0,1,1\r\n");
  }
}

void sendATCommand(String command) {
  Serial.print(command);
  mySerial.print(command); 
  clear();
}

void clear()
{
  delay(100);
   while (Serial.available()) {
    Serial.read(); // 读取并丢弃缓存区中的数据
  }
  while (mySerial.available()) {
    mySerial.read(); // 读取并丢弃缓存区中的数据
  }
}

int servo(int speed, int* distance) {
  int flag=0;
  for (int x = 0; x < 180; x += 2) {
    int i=x/2;
    baseServo.write(x);
    distance[i] = calculateDistance();
    if(flag == 1 && distance[i] == 99 )
    {
      Serial.print('\n');
      Serial.print(distance[i - 1]);
      Serial.println("\nServo scan complete.");
      return x - 2;
    }
    if( distance[i] < 50 && flag == 0 ) 
      flag=1;
    Serial.print(distance[i]);
    Serial.print(" ");
    delay(speed);
    
  }
  Serial.println("\nServo scan complete.");
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

void generateRandomDistances(int* distanceArray) {
  for (int i = 0; i < 90; i++) {
    distanceArray[i] = random(0, 201);  // 生成 0 到 200 之间的随机数
  }
}