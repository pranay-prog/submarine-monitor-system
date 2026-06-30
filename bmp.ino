#include <Wire.h>
#include <Adafruit_BMP085.h>

Adafruit_BMP085 bmp;

#define SEA_LEVEL_PRESSURE 101325  // Pa

void setup() {
  Serial.begin(9600);
  Wire.begin();   // Uno uses A4 (SDA), A5 (SCL)

  Serial.println("Initializing BMP180...");

  if (!bmp.begin()) {
    Serial.println("BMP180 not detected!");
    while (1);
  }

  Serial.println("BMP180 Ready!");
  Serial.println("----------------------------");
}

void loop() {

  float temperature = bmp.readTemperature();     // °C
  int32_t pressurePa = bmp.readPressure();       // Pa

  // Convert to bar
  float pressure_bar = pressurePa / 100000.0;

  float altitude = bmp.readAltitude();           // m

  // Depth calculation
  float depth = (pressurePa - SEA_LEVEL_PRESSURE) / 9810.0;
  if (depth < 0) depth = 0;

  Serial.println("\nBMP180 Readings:");

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");

  Serial.print("Pressure: ");
  Serial.print(pressure_bar, 3);
  Serial.println(" bar");

  Serial.print("Altitude: ");
  Serial.print(altitude);
  Serial.println(" m");

  Serial.print("Depth: ");
  Serial.print(depth);
  Serial.println(" m");

  Serial.println("----------------------------");

  delay(3000);
}