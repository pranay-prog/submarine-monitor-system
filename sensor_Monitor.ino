#include <Wire.h>
#include "DFRobot_OxygenSensor.h"
#include "DHT.h"

#define COLLECT_NUMBER 10

// -------- DHT11 --------
#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// -------- O2 Sensor --------
DFRobot_OxygenSensor oxygen;

void setup() {
  Serial.begin(9600);
  Wire.begin();

  dht.begin();

  delay(2000);

  while (!oxygen.begin(0x73)) {
    Serial.println("ERROR,O2_SENSOR_NOT_DETECTED");
    delay(1000);
  }

  Serial.println("SYSTEM_READY");
  Serial.println("TEMPERATURE,HUMIDITY,OXYGEN");
}

void loop() {

  float oxygenData = oxygen.getOxygenData(COLLECT_NUMBER);
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("ERROR,DHT11_READ_FAILED");
  } else {

    Serial.print(temperature);
    Serial.print(",");

    Serial.print(humidity);
    Serial.print(",");

    Serial.println(oxygenData, 2);
  }

  delay(2000);
}