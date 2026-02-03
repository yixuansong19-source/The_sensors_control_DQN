#include <SoftwareSerial.h>
//AT+CADDRSET=10 AT+CRXS=470500000,5,0,1,1

SoftwareSerial mySerial(5, 4);  // RX = 5, TX = 4



void setup() {
  Serial.begin(9600);    // 初始化主串口
  mySerial.begin(9600);  // 初始化虚拟串
}

void loop() {
  if (mySerial.available()) {
    Serial.write(mySerial.read());  // 将虚拟串口数据输出到主串口
  }

  if (Serial.available()) {
    mySerial.write(Serial.read());  // 将主串口数据发送到虚拟串口
  }
}