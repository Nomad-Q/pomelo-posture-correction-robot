// 接收 "o;" 打开开关、
// 接收 "c;" 关闭开关、
#define comSerial         Serial    // 通信串口
#define ledPin 13                   // led指示灯
#define relayPin 8                  // 控制引脚
#define relayOn    LOW              // 开启电平
#define relayOff  !relayOn          // 关闭电平
String comdata = "";                // 接收字符串
char receiveChar;                   // 接收字符
bool receiveFlag = false;           // 接收标志位
void setup() {
  Serial.begin(9600);               // 串口波特率
  pinMode(ledPin, OUTPUT);          // IO设置输出
  pinMode(relayPin, OUTPUT);        // IO设置输出
  digitalWrite(ledPin, LOW);        // IO低电平
  digitalWrite(relayPin, relayOff); // IO低电平
}

void loop() {
  if (comSerial.available()) {         // 如果串口有数据
    delay(10);
    comdata = "";
    while (comSerial.available()) {    // 读取串口数据
      char receiveChar = char(comSerial.read());// 字符接收
      comdata += receiveChar;          // 字符串接收
      delay(2);
      if (receiveChar == ';')break;    // 直到';'退出接收
    }
    receiveFlag = true;
  }
  if (receiveFlag == true) {           // 第一个字符处理
    receiveFlag = false;               // 清空标志位
    runMotion(comdata);                // 接收处理
  }
}

void runMotion(String com) {           // 接收指令处理
  com.toLowerCase();                   // 小写处理
  Serial.println(com);
  Serial.println(com[0]);
  switch (com[0]) {
    case 'o': {
        Serial.println("open");
        digitalWrite(ledPin, HIGH);        // 亮板载灯
        digitalWrite(relayPin, relayOn);   // 开启电路
      } break;
    case 'c': {
        Serial.println("close");
        digitalWrite(relayPin, relayOff);  // 关闭电路
        digitalWrite(ledPin, LOW);         // 灭板载灯
      } break;
    default: break;
  }
}
