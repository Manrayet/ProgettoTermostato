#include <DHT.h>
#include <ArduinoJson.h>

#define DHTPIN 2
#define DHTTYPE DHT11

int rele = 11;
int ledRosso = 10;
int ledVerde = 9;
int ledBlu = 8;

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  pinMode(rele, OUTPUT);
  pinMode(ledRosso, OUTPUT);
  pinMode(ledVerde, OUTPUT);
  pinMode(ledBlu, OUTPUT);

  digitalWrite(rele, LOW);
  digitalWrite(ledRosso, LOW);
  digitalWrite(ledVerde, LOW);
  digitalWrite(ledBlu, LOW);

  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float temperatura = dht.readTemperature();
  float umidita = dht.readHumidity();

 JsonDocument doc;
  doc["temperatura"] = temperatura;
  doc["umidita"] = umidita;
  doc["time"] = millis() /1000

  String jsonString;
  serializeJson(doc, jsonString);
  Serial.println(jsonString);

  if (temperatura >= 27.0) {  
    digitalWrite(ledRosso, HIGH);
    digitalWrite(ledVerde, LOW);
    digitalWrite(ledBlu, LOW);
  }  
  else if (temperatura >= 17.0) {  
    digitalWrite(ledRosso, LOW);
    digitalWrite(ledVerde, HIGH);
    digitalWrite(ledBlu, LOW);
  }  
  else {  
    digitalWrite(ledRosso, LOW);
    digitalWrite(ledVerde, LOW);
    digitalWrite(ledBlu, HIGH);
  }

  if (temperatura >= 17.0) {
    digitalWrite(rele, LOW);
  } else {
    digitalWrite(rele, HIGH);
  }

  delay(1500);
}
