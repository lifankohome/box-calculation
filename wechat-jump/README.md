# 微信跳一跳自动测距

模板匹配并没有使用灰度图，而是用的蓝色通道，因为识别效果蓝色区分度最高

# 延时公式
Delay = Pixels Dis * 2.35 + 136

200个以内都符合，超过两百近距离-5，远距离+5

# Arduino 程序
```
int pin = 9;

void setup() {
  // put your setup code here, to run once:
  pinMode(pin, OUTPUT);
  digitalWrite(pin, HIGH);

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available() > 0) {
    int dis = Serial.parseInt();

    if (Serial.read() == '\n') {
      Serial.print(dis);
      Serial.print('\n');
      digitalWrite(pin, LOW);
      delay(dis);
    }
    digitalWrite(pin, HIGH);
  }
}

```

### 屏幕控制
pin9接继电器，继电器开关一端接GND，一端接屏幕，和屏幕的接触面积 >= 5mm * 5mm

原理请转至Youtube：How Capacitive Touch Screens Work
