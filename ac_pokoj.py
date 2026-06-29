#!/usr/bin/env python3
import time, json, tinytuya, paho.mqtt.client as mqtt

# Ładowanie konfiguracji
with open("ac_pokoj_settings.json", "r") as f: config = json.load(f)

DEVICE_ID = config["device_id"]; DEVICE_KEY = config["device_key"]; DEVICE_IP = config["device_ip"]
TOPIC_SET = config["topic_set"]; TOPIC_STATUS = config["topic_status"]

IDX_POWER = config["idx"]["power"]; IDX_TEMP = config["idx"]["temp"]; IDX_MODE = config["idx"]["mode"]
IDX_FAN = config["idx"]["fan"]; IDX_VSWING = config["idx"]["vswing"]; IDX_VPOS = config["idx"]["vpos"]
IDX_HSWING = config["idx"]["hswing"]; IDX_HPOS = config["idx"]["hpos"]; IDX_DISPLAY = config["idx"]["display"]
IDX_ANTIMILDEW = config["idx"]["anti_mildew"]; IDX_HEALTH = config["idx"]["health"]
IDX_ECO = config["idx"]["eco"]; IDX_BEEPER = config["idx"]["beeper"]; IDX_SLEEP = config["idx"]["sleep"]

def log(msg): print(time.strftime("%Y-%m-%d %H:%M:%S"), f"[POKÓJ] {msg}", flush=True)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2); d = tinytuya.Device(DEVICE_ID, DEVICE_IP, DEVICE_KEY); d.set_version(3.3)
last_dps = {}; pending_payload = {}

BIT_DISPLAY = 0x0008; BIT_ANTIMILDEW = 0x0100; BIT_HEALTH = 0x0020; BIT_ECO = 0x0001; BIT_BEEPER = 0x0010

def normalize_bm(bm): return format(bm, "04x") if isinstance(bm, int) else bm.zfill(4)
def update_bitmask_flag(val, bit, state): return (val | bit) if state else (val & ~bit)

def decode_dps(dps):
    pwr = dps.get("1")
    out = {"power": "on" if pwr is True or str(pwr) == "1" else "off"}
    if "2" in dps: out["temp"] = int(dps["2"]) // 10
    out["mode"] = dps.get("4"); out["fan"] = dps.get("5")
    out["vswing"] = str(dps.get("113", "0")); out["vpos"] = str(dps.get("126", "1"))
    out["hswing"] = str(dps.get("114", "0")); out["hpos"] = str(dps.get("127", "1"))
    out["sleep"] = dps.get("105", "off")
    val = int(normalize_bm(dps.get("123", "0000")), 16)
    out.update({"display": bool(val & BIT_DISPLAY), "anti_mildew": bool(val & BIT_ANTIMILDEW),
                "health": bool(val & BIT_HEALTH), "eco": bool(val & BIT_ECO), "beeper": bool(val & BIT_BEEPER)})
    return out

def process_command(payload):
    global pending_payload
    pending_payload.update(payload)

def execute_command(payload):
    global last_dps
    try:
        if "mode" in payload: d.set_value(4, payload["mode"])
        if "power" in payload: d.set_value(1, payload["power"] == "on")
        if "temp" in payload: d.set_value(2, int(payload["temp"]) * 10)
        if "fan" in payload: d.set_value(5, payload["fan"])
        if "vswing" in payload: d.set_value(113, payload["vswing"])
        if "vpos" in payload: d.set_value(126, payload["vpos"])
        if "hswing" in payload: d.set_value(114, payload["hswing"])
        if "hpos" in payload: d.set_value(127, payload["hpos"])
        if "sleep" in payload: d.set_value(105, payload["sleep"])
        if any(k in payload for k in ["display", "anti_mildew", "health", "eco", "beeper"]):
            bm = int(normalize_bm(last_dps.get("123", "0000")), 16)
            if "display" in payload: bm = update_bitmask_flag(bm, BIT_DISPLAY, payload["display"] in ["on", True, 1])
            if "anti_mildew" in payload: bm = update_bitmask_flag(bm, BIT_ANTIMILDEW, payload["anti_mildew"] in ["on", True, 1])
            if "health" in payload: bm = update_bitmask_flag(bm, BIT_HEALTH, payload["health"] in ["on", True, 1])
            if "eco" in payload: bm = update_bitmask_flag(bm, BIT_ECO, payload["eco"] in ["on", True, 1])
            if "beeper" in payload: bm = update_bitmask_flag(bm, BIT_BEEPER, payload["beeper"] in ["on", True, 1])
            d.set_value(123, format(bm, "04x"))
    except Exception as e: log(f"Błąd wysyłania: {e}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        if msg.topic == TOPIC_SET: process_command(payload)
        elif msg.topic == "domoticz/out":
            idx = payload.get("idx"); s = str(payload.get("svalue1", "0")); n = payload.get("nvalue", 0)
            if idx == IDX_POWER: process_command({"power": "on" if n == 1 else "off"})
            elif idx == IDX_SLEEP: process_command({"sleep": "normal" if n == 1 else "off"})
            elif idx == IDX_MODE:
                m = {"10":"auto","20":"cold","30":"wet","40":"wind","50":"hot"}
                if s in m: process_command({"mode": m[s]})
            elif idx == IDX_FAN:
                f = {"10":"auto","20":"mute","30":"low","40":"mid","50":"mid-high","60":"high"}
                if s in f: process_command({"fan": f[s]})
            elif idx == IDX_VSWING:
                v = {"0":"0","10":"1","20":"2","30":"3"}
                if s in v: process_command({"vswing": v[s]})
            elif idx == IDX_VPOS:
                v = {"10":"1","20":"2","30":"3","40":"4","50":"5"}
                if s in v: process_command({"vpos": v[s]})
            elif idx == IDX_HSWING:
                v = {"0":"0","10":"1","20":"2","30":"3","40":"4"}
                if s in v: process_command({"hswing": v[s]})
            elif idx == IDX_HPOS:
                v = {"10":"1","20":"2","30":"3","40":"4","50":"5"}
                if s in v: process_command({"hpos": v[s]})
            elif idx == IDX_TEMP: process_command({"temp": int(float(s))})
            elif idx in [IDX_DISPLAY, IDX_ANTIMILDEW, IDX_HEALTH, IDX_ECO, IDX_BEEPER]:
                k = {IDX_DISPLAY:"display", IDX_ANTIMILDEW:"anti_mildew", IDX_HEALTH:"health", IDX_ECO:"eco", IDX_BEEPER:"beeper"}[idx]
                process_command({k: (n == 1)})
    except Exception as e: log(f"Błąd odbioru: {e}")

def update_domoticz(idx, n, s=""): client.publish("domoticz/in", json.dumps({"idx": idx, "nvalue": n, "svalue": str(s)}))

def sync_to_domoticz(dec):
    if "power" in dec: update_domoticz(IDX_POWER, 1 if dec["power"] == "on" else 0)
    if "sleep" in dec: update_domoticz(IDX_SLEEP, 1 if dec["sleep"] == "normal" else 0)
    if dec.get("mode"): update_domoticz(IDX_MODE, 0, {"auto":"10","cold":"20","wet":"30","wind":"40","hot":"50"}[dec["mode"]])
    if dec.get("fan"): update_domoticz(IDX_FAN, 0, {"auto":"10","mute":"20","low":"30","mid":"40","mid-high":"50","high":"60"}[dec["fan"]])
    if dec.get("vswing"): update_domoticz(IDX_VSWING, 0, {"0":"0","1":"10","2":"20","3":"30"}.get(dec["vswing"], "0"))
    if dec.get("vpos"): update_domoticz(IDX_VPOS, 0, {"1":"10","2":"20","3":"30","4":"40","5":"50"}.get(dec["vpos"], "10"))
    if dec.get("hswing"): update_domoticz(IDX_HSWING, 0, {"0":"0","1":"10","2":"20","3":"30","4":"40"}.get(dec["hswing"], "0"))
    if dec.get("hpos"): update_domoticz(IDX_HPOS, 0, {"1":"10","2":"20","3":"30","4":"40","5":"50"}.get(dec["hpos"], "10"))
    if "temp" in dec: update_domoticz(IDX_TEMP, 0, str(dec["temp"]))
    for k, i in [("display", IDX_DISPLAY), ("anti_mildew", IDX_ANTIMILDEW), ("health", IDX_HEALTH), ("eco", IDX_ECO), ("beeper", IDX_BEEPER)]:
        if k in dec: update_domoticz(i, 1 if dec[k] else 0)

client.on_message = on_message
client.connect("localhost", 1883, 60); client.subscribe([(TOPIC_SET, 0), ("domoticz/out", 0)]); client.loop_start()

while True:
    try:
        if pending_payload:
            cmd = pending_payload.copy()
            pending_payload = {}
            log(f"Wysyłam komendę: {cmd}")
            execute_command(cmd)
            
        current_dps = d.status().get("dps", {})
        if current_dps and current_dps != last_dps:
            log(f"Nowy stan DPS: {current_dps}")
            last_dps = current_dps
            dec = decode_dps(current_dps)
            client.publish(TOPIC_STATUS, json.dumps(dec), retain=True)
            sync_to_domoticz(dec)
            
        time.sleep(0.3)
    except Exception as e: 
        log(f"Błąd pętli: {e}")
        time.sleep(1.0)