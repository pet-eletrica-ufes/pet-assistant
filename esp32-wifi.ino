
#include <WiFi.h>
 
const char* ssid = "***";
const char* password = "****";
int LED = 33;
int MED =14;
WiFiServer server(80);
 
void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
  pinMode(MED, OUTPUT);
 
  Serial.println();
  Serial.print("Conectando-se a ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
 
  Serial.println("");
  Serial.println("WiFi conectada.");
  Serial.println("Endereço de IP: ");
  Serial.println(WiFi.localIP());
 
  server.begin();
}
 
void loop() {
  WiFiClient client = server.available();
  if (client) {
    Serial.println("New Client.");
    String currentLine = "";
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        Serial.write(c);
        if (c == '\n') {
          if (currentLine.length() == 0) {
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println();
            client.print("Clique <a href=\"/H\">aqui</a> para acender.<br>");
            client.print("Clique <a href=\"/A\">aqui</a> para acender 2.<br>");
            client.print("Clique <a href=\"/L\">aqui</a> para desligar.<br>");
            client.println();
            break;
          } else {
            currentLine = "";
          }
        } else if (c != '\r') {
          currentLine += c;
        }
        int var=0;
        if (currentLine.endsWith("GET /H")) {
          while (var < 30){
            digitalWrite(LED, HIGH);
            delay(1000);
            digitalWrite(LED, LOW);
            digitalWrite(MED, HIGH);
            delay(1000);
            digitalWrite(MED, LOW);
            var++;
            Serial.println(var);
          }


        }
         if (currentLine.endsWith("GET /A")) {
          digitalWrite(MED, HIGH);
        }
        if (currentLine.endsWith("GET /L")) {
          digitalWrite(LED, LOW);
          digitalWrite(MED, LOW);
        }
      }
    }
    client.stop();
    Serial.println("Client Disconnected.");
  }
}
