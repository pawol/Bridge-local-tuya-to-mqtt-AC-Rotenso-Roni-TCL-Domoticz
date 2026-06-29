# Mostek-local-tuya-do-mqtt-klimatyzatora-Rotenso-Roni-TCL
Mostek local tuya do mqtt klimatyzatora Rotenso Roni 

Najprawdopodobniej klimatyzator Rotenso Roni to bezpośredni klon TCL Elite.

Uzyskanie local_key i device_ID urządzenie tuya:

- Skonfigurować apke tuya i zintegrować klimatyzator, zamknąć apkę
WAŻNE!
Otwarta aplikacja tuya przechwytuje ruch i local tuya wtedy nie działa, nie należy jej używać!

- Zarejestrować się na https://tuya.com
i włączyć/przedłużyć suybskrypcje w Developer Platform / Cloud /Cloud Services /IoT Core

- W zakładce Cloud / API Explorer poszykać w drzewku Device Management / Query Device Details, wkleić ID badanego urządzenia w device_id i nacisnąć Submit Request

local_key pojawi się w onie Debugging Results jako Response

Zapisać device_ID (uuid w Responce) i local_key (tez w Response) do pliku ac_pokoj_settings.json
Template pliku do pobrania.
Utworzyć w Domoticz wirtualne switche/ selectory/setpointy itd. według schematu:
Power-Switch (On/Off)
Ustawiana temperatura-jako Setpoint (Thermostat/Setpoint)
Odczytana temperatura-jako Temperature
Tryb pracy-jako Selector Switch (Auto, Cold, Wet, Wind, Hot) (level 10/20/30/40/50)
Siła nawiewu-jako Selector Switch (Auto, Mute, Low, Mid, Mid-High, High) (level 10/20/30/40/50/60)
Pionowy swing-jako Selector Switch (Off, 1, 2, 3) (level 0/10/20/30)
Pionowa pozycja-jako Selector Switch (1, 2, 3, 4, 5) (level 10/20/30/40/50)
Poziomy swing-jako Selector Switch (Off, 1, 2, 3, 4) (level 0/10/20/30)
Pozioma pozycja-jako Selector Switch (1, 2, 3, 4, 5) (level 10/20/30/40/50)
Display-jako Switch (On/Off) (true, false)
Anti-mildew-jako Switch (On/Off) (true, false)
Health-jako Switch (On/Off) (true, false)
Tryb Eco-jako Switch (On/Off) (true, false)
Beeper-jako Switch (On/Off) (on, off)
Tryb do spania-jako Switch (On/Off) (normal, off)


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


#---------------------------
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
#--------------------------------

Zapewnienie autostartu tinytuya jako systemd:

sudo systemctl daemon-reload
sudo systemctl enable ac_pokoj.service
sudo systemctl start ac_pokoj.service
sudo systemctl status ac_pokoj.service
