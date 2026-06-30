# Bridge-local-tuya-do-mqtt-AC-Rotenso-Roni-TCL
Bridge local tuya to mqtt AC Rotenso Roni / TCL

Najprawdopodobniej klimatyzator Rotenso Roni to bezpośredni klon TCL Elite.

    Pamiętaj, że eksperymentujesz na własną odpowiedzialność!
    

Uzyskanie local_key i device_ID urządzenie tuya:

- Skonfigurować apke tuya i zintegrować klimatyzator, zamknąć apkę
WAŻNE!
Otwarta aplikacja tuya przechwytuje ruch i local tuya wtedy nie działa, nie należy jej używać!

- Zarejestrować się na https://tuya.com
i włączyć/przedłużyć suybskrypcje w Developer Platform / Cloud /Cloud Services /IoT Core

- W zakładce Cloud / API Explorer poszykać w drzewku Device Management / Query Device Details, wkleić ID badanego urządzenia w device_id i nacisnąć Submit Request

local_key pojawi się w onie Debugging Results jako Response


Zapisać device_ID (uuid w Responce) i local_key (tez w Response) do pliku ac_pokoj_settings.json
Template pliku jest do pobrania z tego repozytorium.

Skopiowanie skryptu mostkujący klimatyzator tuya Rotenso Roni o nazwie ac_pokoj.py oraz ac_pokoj_settings.json
do przykładowo foldera:
    /home/pwoloszyn/domoticz/scripts/tuya/AC/

Instalacja python venv i tinytuya:

    sudo apt update
    sudo apt install python3-venv -y
    cd /home/pwoloszyn
    python3 -m venv tinytuya_env
    source /home/pwoloszyn/tinytuya_env/bin/activate
    pip install --upgrade pip
    pip install tinytuya paho-mqtt

Autostart tinytuya przez systemd:

    sudo nano /etc/systemd/system/ac_pokoj.service
    
i wkleić treść zmodyfikowaną pod siebie.

testowo możesz już teraz uruchomić skrypt przez:

    /home/pwoloszyn/tinytuya/bin/python /home/pwoloszyn/domoticz/scripts/tuya/AC/ac_pokoj.py

Podobnie z ac_sniffer.py, Skrypt snifuje komunikację klimatyzatora z tuya gdy naciskamy przyciski pilota.

    /home/pwoloszyn/tinytuya/bin/python /home/pwoloszyn/domoticz/scripts/tuya/AC/ac_snifer.py

Po uruchomieniu skryptu ac_pokoj_py w python venv od razu można obserwować status klimatyzatora:

    mosquitto_sub -v -t 'tuya/ac_pokoj/status'

i sterować nim:

🟩 1. POWER (DPS 1)
on /off

    mosquitto_pub -t tuya/ac_pokoj/set -m '{"power":"on"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"power":"off"}'

🟩 2. TEMPERATURA (DPS 2)
16–31

    mosquitto_pub -t tuya/ac_pokoj/set -m '{"temp":24}'

🟩 3. TRYB PRACY (DPS 4)
cold / hot / wet / wind / auto

    mosquitto_pub -t tuya/ac_pokoj/set -m '{"mode":"cold"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"mode":"hot"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"mode":"wet"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"mode":"wind"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"mode":"auto"}'

🟩 4. FAN SPEED (DPS 5)
low / mid / high / mute / auto

    mosquitto_pub -t tuya/ac_pokoj/set -m '{"fan":"low"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"fan":"mid"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"fan":"high"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"fan":"mute"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"fan":"auto"}'

🟩 5. SLEEP (DPS 105)
normal / off

    mosquitto_pub -t tuya/ac_pokoj/set -m '{"sleep":"normal"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"sleep":"off"}'

🟩 6. BITMASKA (DPS 123)
DISPLAY
display, eco, health, anti_mildew, beeper
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"display":true}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"display":false}'

ECO
true / false

    mosquitto_pub -t tuya/ac_pokoj/set -m '{"eco":true}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"eco":false}'

HEALTH
true / false

    mosquitto_pub -t tuya/ac_pokoj/set -m '{"health":true}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"health":false}'

ANTI‑MILDEW
true / false

    mosquitto_pub -t tuya/ac_pokoj/set -m '{"anti_mildew":true}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"anti_mildew":false}'

BEEPER
true / false

    mosquitto_pub -t tuya/ac_pokoj/set -m '{"beeper":"on"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"beeper":"off"}'

🟩 7. SWING PION (VERTICAL) — DPS 113 / 126 / 133
    0 = OFF
    1 = pełny swing 1–5
    2 = swing 1–3
    3 = swing 3–5

    mosquitto_pub -t tuya/ac_pokoj/set -m '{"vswing":"0"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"vswing":"1"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"vswing":"2"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"vswing":"3"}'

Pozycje pionowe (DPS 126):

    mosquitto_pub -t tuya/ac_pokoj/set -m '{"vpos":"1"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"vpos":"2"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"vpos":"3"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"vpos":"4"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"vpos":"5"}'

🟩 8. SWING POZIOM (HORIZONTAL) — DPS 114 / 127
    0 = OFF
    1 = swing 1–5
    2 = swing 1–3
    3 = swing 2–4
    4 = swing 3–5

    mosquitto_pub -t tuya/ac_pokoj/set -m '{"hswing":"0"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"hswing":"1"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"hswing":"2"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"hswing":"3"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"hswing":"4"}'

Pozycje poziome (DPS 127):

    mosquitto_pub -t tuya/ac_pokoj/set -m '{"hpos":"1"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"hpos":"2"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"hpos":"3"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"hpos":"4"}'
    mosquitto_pub -t tuya/ac_pokoj/set -m '{"hpos":"5"}'


Utworzyć w Domoticz wirtualne switche/ selectory/setpointy itd. według schematu:

    "Power"-Switch (On/Off)
    "Ustawiana temperatura": Setpoint (Thermostat/Setpoint)
    "Odczytana temperatura": Temperature
    "Tryb pracy": Selector Switch (Auto, Cold, Wet, Wind, Hot) (level 10/20/30/40/50)
    "Siła nawiewu": Selector Switch (Auto, Mute, Low, Mid, Mid-High, High) (level 10/20/30/40/50/60)
    "Pionowy swing": Selector Switch (Off, 1, 2, 3) (level 0/10/20/30)
    "Pionowa pozycja": Selector Switch (1, 2, 3, 4, 5) (level 10/20/30/40/50)
    "Poziomy swing": Selector Switch (Off, 1, 2, 3, 4) (level 0/10/20/30)
    "Pozioma pozycja": Selector Switch (1, 2, 3, 4, 5) (level 10/20/30/40/50)
    "Display": Switch (On/Off) (true, false)
    "Anti-mildew": Switch (On/Off) (true, false)
    "Health": Switch (On/Off) (true, false)
    "Tryb Eco": Switch (On/Off) (true, false)
    "Beeper": Switch (On/Off) (on, off)
    "Tryb do spania": Switch (On/Off) (normal, off)


IDX utworzonych przełaczników przenieść do pliku ac_pokoj_settings.json
Przykład:

    "power": 735,       // Switch (On/Off)
    "temp": 736,        // Setpoint (Thermostat/Setpoint)
    "temp_current": 764,// Temperature
    "mode": 737,        // Selector Switch (Auto, Cold, Wet, Wind, Hot) (level 10/20/30/40/50)
    "fan": 738,         // Selector Switch (Auto, Mute, Low, Mid, Mid-High, High) (level 10/20/30/40/50/60)
    "vswing": 744,      // Selector Switch (Off, 1, 2, 3) (level 0/10/20/30)
    "vpos": 745,        // Selector Switch (1, 2, 3, 4, 5) (level 10/20/30/40/50)
    "hswing": 746,      // Selector Switch (Off, 1, 2, 3, 4) (level 0/10/20/30)
    "hpos": 747,        // Selector Switch (1, 2, 3, 4, 5) (level 10/20/30/40/50)
    "display": 739,     // Switch (On/Off) (true, false)
    "anti_mildew": 740, // Switch (On/Off) (true, false)
    "health": 741,      // Switch (On/Off) (true, false)
    "eco": 742,         // Switch (On/Off) (true, false)
    "beeper": 743,      // Switch (On/Off) (on, off)
    "sleep": 761        // Switch (On/Off) (normal, off)

Skopiowanie skryptu mostkujący klimatyzator tuya Rotenso Roni o nazwie ac_pokoj.py oraz ac_pokoj_settings.json
do przykładowo foldera:

 /home/pwoloszyn/domoticz/scripts/tuya/AC/

Instalacja python venv i tinytuya:

sudo apt update
sudo apt install python3-venv -y
cd /home/pwoloszyn
python3 -m venv tinytuya_env
source /home/pwoloszyn/tinytuya_env/bin/activate
pip install --upgrade pip
pip install tinytuya paho-mqtt


Autostart tinytuya przez systemd:

    sudo nano /etc/systemd/system/ac_pokoj.service
    
i wkleić treść zmodyfikowaną pod siebie.

Przykład pliku systemd:

    [Unit]
    Description=Klimatyzacja w pokoju (Tuya MQTT)
    After=network.target

    [Service]
    Type=simple
    User=pwoloszyn
    WorkingDirectory=/home/pwoloszyn/domoticz/scripts/tuya/AC
    ExecStart=/home/pwoloszyn/tinytuya_env/bin/python /home/pwoloszyn/domoticz/scripts/tuya/AC/ac_pokoj.py
    Restart=always
    RestartSec=5
    #StandardOutput=append:/tmp/ac_pokoj.log
    #StandardError=append:/tmp/ac_pokoj.log
    StandardOutput=null
    StandardError=null

    [Install]
    WantedBy=multi-user.target

Zapewnienie autostartu tinytuya jako systemd:

    sudo systemctl daemon-reload
    sudo systemctl enable ac_pokoj.service
    sudo systemctl start ac_pokoj.service
    sudo systemctl status ac_pokoj.service

Pamiętaj, że każda modyfikacja skryptu lub jego konfiguracji musi zakończyć się restartem systemd:

    sudo systemctl restart ac_pokoj
