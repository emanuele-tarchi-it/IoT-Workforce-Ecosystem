#include <M5Stack.h>
#include <SD.h>
#include <WiFi.h>
#include "time.h"

// --- CONFIGURAZIONE ---
const char* ssid     = "IL_TUO_WIFI";
const char* password = "LA_TUA_PASSWORD";
const char* ntpServer = "pool.ntp.org";
const char* mesi[] = {"Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"};

// --- FUNZIONE BATTERIA ---
float getBatteryVoltage() {
    pinMode(35, INPUT);
    uint16_t raw = analogRead(35);
    if (raw == 0) {
        pinMode(34, INPUT);
        raw = analogRead(34);
    }
    return ((float)raw / 4095.0) * 2.0 * 3.3 * 1.1;
}

// ... (resto delle tue funzioni: updateBatteryIcon, timbra, etc.)

void setup() {
    M5.begin();
    M5.Power.begin();
    WiFi.begin(ssid, password);
    configTime(3600, 0, ntpServer); // GMT+1
    mostraInterfacciaBase();
}

void loop() {
    M5.update();
    if (M5.BtnA.wasPressed() || M5.BtnB.wasPressed() || M5.BtnC.wasPressed()) {
        timbra();
    }
    // Aggiornamento orario e icone...
    delay(500);
}