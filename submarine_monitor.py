"""
=============================================================================
  SUBMARINE CABIN - REAL-TIME AI MONITORING SYSTEM WITH AES-256 ENCRYPTION
=============================================================================
  Monitors: O2 Level, Temperature, Humidity, Pressure, CO2, CO, H2 Gas,
            Oxygen Cylinder Capacity
  Encryption: AES-256-GCM (Galois/Counter Mode) for authenticated encryption
  AI Layer:  Anomaly detection via threshold + rate-of-change analysis
=============================================================================
"""

import os
import json
import time
import random
import hashlib
import datetime
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# ─────────────────────────────────────────────
#  AES-256-GCM ENCRYPTION / DECRYPTION MODULE
# ─────────────────────────────────────────────

class AES256Encryptor:
    """
    AES-256-GCM provides:
      * 256-bit key  -> strong confidentiality
      * GCM mode     -> built-in authentication (detects tampering)
      * Unique nonce -> prevents replay attacks on sensor data
    """

    def __init__(self, key: bytes = None):
        # 256-bit key = 32 bytes
        self.key = key if key else os.urandom(32)
        self.aesgcm = AESGCM(self.key)

    def encrypt(self, plaintext: str) -> dict:
        """Encrypt a JSON string -> returns hex nonce + ciphertext."""
        nonce = os.urandom(12)          # 96-bit nonce (GCM standard)
        data  = plaintext.encode("utf-8")
        ct    = self.aesgcm.encrypt(nonce, data, None)
        return {
            "nonce":      nonce.hex(),
            "ciphertext": ct.hex(),
            "key_id":     hashlib.sha256(self.key).hexdigest()[:8],
        }

    def decrypt(self, package: dict) -> str:
        """Decrypt a package produced by encrypt()."""
        nonce = bytes.fromhex(package["nonce"])
        ct    = bytes.fromhex(package["ciphertext"])
        pt    = self.aesgcm.decrypt(nonce, ct, None)
        return pt.decode("utf-8")

    def key_hex(self) -> str:
        return self.key.hex()


# ─────────────────────────────────────────────
#  SENSOR SIMULATION ENGINE
# ─────────────────────────────────────────────

class SubmarineSensorSimulator:
    """
    Simulates all critical submarine cabin sensors.
    Supports:  NORMAL | ANOMALY_O2_DROP | ANOMALY_GAS_LEAK | ANOMALY_PRESSURE
    """

    SAFE_RANGES = {
        "o2_percent":        (19.5,  23.5),
        "temperature_c":     (18.0,  26.0),
        "humidity_percent":  (30.0,  70.0),
        "pressure_kpa":      (95.0, 105.0),
        "co2_ppm":           (0.0,  1000.0),
        "co_ppm":            (0.0,    35.0),
        "h2_ppm":            (0.0,   100.0),
        "o2_cylinder_bar":   (20.0,  300.0),
    }

    def __init__(self):
        self.state = {
            "o2_percent":       21.0,
            "temperature_c":    22.0,
            "humidity_percent": 50.0,
            "pressure_kpa":    101.3,
            "co2_ppm":         450.0,
            "co_ppm":            5.0,
            "h2_ppm":           10.0,
            "o2_cylinder_bar": 250.0,
        }
        self.tick = 0

    def _drift(self, current, low, high, noise=0.05, drift=0.0):
        val = current + random.gauss(drift, noise * (high - low))
        return round(max(low * 0.85, min(high * 1.15, val)), 3)

    def read(self, mode: str = "normal") -> dict:
        self.tick += 1

        if mode == "normal":
            self.state["o2_percent"]       = self._drift(self.state["o2_percent"],       19.5, 23.5, 0.01)
            self.state["temperature_c"]    = self._drift(self.state["temperature_c"],    18.0, 26.0, 0.02)
            self.state["humidity_percent"] = self._drift(self.state["humidity_percent"], 30.0, 70.0, 0.02)
            self.state["pressure_kpa"]     = self._drift(self.state["pressure_kpa"],     95.0, 105.0, 0.01)
            self.state["co2_ppm"]          = self._drift(self.state["co2_ppm"],           400,  600, 0.03)
            self.state["co_ppm"]           = self._drift(self.state["co_ppm"],              0,   15, 0.05)
            self.state["h2_ppm"]           = self._drift(self.state["h2_ppm"],              0,   40, 0.05)
            self.state["o2_cylinder_bar"] -= random.uniform(0.05, 0.15)

        elif mode == "anomaly_o2_drop":
            self.state["o2_percent"]      -= random.uniform(0.3, 0.8)
            self.state["o2_cylinder_bar"] -= random.uniform(0.5, 1.5)
            self.state["co2_ppm"]         += random.uniform(20, 60)

        elif mode == "anomaly_gas_leak":
            self.state["co_ppm"]          += random.uniform(5, 20)
            self.state["h2_ppm"]          += random.uniform(10, 40)
            self.state["temperature_c"]   += random.uniform(0.1, 0.5)

        elif mode == "anomaly_pressure":
            self.state["pressure_kpa"]    -= random.uniform(1.0, 3.0)
            self.state["temperature_c"]   -= random.uniform(0.5, 1.5)
            self.state["humidity_percent"]+= random.uniform(1.0, 3.0)

        return {
            "tick":      self.tick,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "mode":      mode,
            "readings":  {k: round(v, 3) for k, v in self.state.items()},
        }


# ─────────────────────────────────────────────
#  AI ANOMALY DETECTION ENGINE
# ─────────────────────────────────────────────

THRESHOLDS = {
    "o2_percent":        {"low": 19.5,  "high": 23.5,  "unit": "%"},
    "temperature_c":     {"low": 18.0,  "high": 26.0,  "unit": "C"},
    "humidity_percent":  {"low": 30.0,  "high": 70.0,  "unit": "%RH"},
    "pressure_kpa":      {"low": 95.0,  "high": 105.0, "unit": "kPa"},
    "co2_ppm":           {"low": 0,     "high": 1000,  "unit": "ppm"},
    "co_ppm":            {"low": 0,     "high": 35,    "unit": "ppm"},
    "h2_ppm":            {"low": 0,     "high": 100,   "unit": "ppm"},
    "o2_cylinder_bar":   {"low": 20.0,  "high": 300.0, "unit": "bar"},
}

SEVERITY_CRITICAL = {
    "o2_percent":      {"low": 18.0,  "high": 25.0},
    "co_ppm":          {"high": 70},
    "h2_ppm":          {"high": 400},
    "pressure_kpa":    {"low": 90.0,  "high": 110.0},
    "o2_cylinder_bar": {"low": 20.0},
}

def detect_anomalies(readings: dict, prev_readings: dict) -> list:
    alerts = []
    for param, val in readings.items():
        t = THRESHOLDS.get(param)
        if not t:
            continue
        status = "OK"
        if "low"  in t and val < t["low"]:  status = "WARNING_LOW"
        if "high" in t and val > t["high"]: status = "WARNING_HIGH"
        sc = SEVERITY_CRITICAL.get(param, {})
        if "low"  in sc and val < sc["low"]:  status = "CRITICAL_LOW"
        if "high" in sc and val > sc["high"]: status = "CRITICAL_HIGH"
        if prev_readings and param in prev_readings:
            delta = val - prev_readings[param]
            if abs(delta) > 0.05 * (t["high"] - t.get("low", 0)) and status == "OK":
                status = "RAPID_CHANGE"
        if status != "OK":
            alerts.append({
                "parameter": param,
                "value":     val,
                "unit":      t["unit"],
                "status":    status,
            })
    return alerts


# ─────────────────────────────────────────────
#  DISPLAY HELPERS
# ─────────────────────────────────────────────

R = "\033[91m"; Y = "\033[93m"; G = "\033[92m"
C = "\033[96m"; B = "\033[94m"; BOLD = "\033[1m"
RESET = "\033[0m"; DIM = "\033[2m"

def col(status):
    if "CRITICAL" in status: return R
    if "WARNING"  in status: return Y
    if "RAPID"    in status: return Y
    return G

PARAM_LABELS = {
    "o2_percent":       "O2 Level          ",
    "temperature_c":    "Temperature       ",
    "humidity_percent": "Humidity          ",
    "pressure_kpa":     "Cabin Pressure    ",
    "co2_ppm":          "CO2 Concentration ",
    "co_ppm":           "CO  Concentration ",
    "h2_ppm":           "H2  Concentration ",
    "o2_cylinder_bar":  "O2 Cylinder Press.",
}

def print_header():
    print(f"""
{BOLD}{C}+======================================================================+
|       SUBMARINE CABIN -- AI REAL-TIME MONITORING + AES-256          |
|       Encryption: AES-256-GCM  |  AI: Threshold + ROC Detection     |
+======================================================================+{RESET}
""")

def print_key_info(enc):
    print(f"{BOLD}{'─'*70}{RESET}")
    print(f"{BOLD}  AES-256-GCM SESSION KEY  (256-bit / 32 bytes){RESET}")
    print(f"{BOLD}{'─'*70}{RESET}")
    k = enc.key_hex()
    for i in range(0, len(k), 32):
        chunk = k[i:i+32]
        print(f"  {DIM}{' '.join(chunk[j:j+4] for j in range(0,len(chunk),4))}{RESET}")
    print(f"\n  {DIM}Key fingerprint (SHA-256 prefix): {k[:16]}...{RESET}")
    print(f"{BOLD}{'─'*70}{RESET}\n")

def print_tick(td, enc_pkg, alerts):
    tick, ts, mode, readings = td["tick"], td["timestamp"], td["mode"], td["readings"]
    alert_map = {a["parameter"]: a["status"] for a in alerts}

    print(f"\n{BOLD}{'='*70}{RESET}")
    print(f"{BOLD}  TICK #{tick:03d}  |  {ts}  |  Mode: {mode.upper()}{RESET}")
    print(f"{BOLD}{'='*70}{RESET}")

    print(f"\n  {BOLD}[ SENSOR READINGS ]{RESET}")
    for param, label in PARAM_LABELS.items():
        val    = readings[param]
        unit   = THRESHOLDS[param]["unit"]
        status = alert_map.get(param, "OK")
        c      = col(status)
        tag    = f"  [{status}]" if status != "OK" else ""
        print(f"    {label}: {c}{val:>10.3f} {unit}{RESET}{c}{tag}{RESET}")

    print(f"\n  {BOLD}[ AES-256-GCM ENCRYPTED PACKET ]{RESET}")
    print(f"    {DIM}Key ID   : {enc_pkg['key_id']}{RESET}")
    print(f"    {DIM}Nonce    : {enc_pkg['nonce'][:24]}...{RESET}")
    ct = enc_pkg['ciphertext']
    print(f"    {DIM}CipherTxt: {ct[:64]}...{ct[-16:]}{RESET}")
    print(f"    {DIM}Enc size : {len(ct)//2} bytes  |  Nonce: 12 B  |  Auth-tag: 16 B{RESET}")

    if alerts:
        print(f"\n  {BOLD}[ !! AI ANOMALY ALERTS ]{RESET}")
        for a in alerts:
            c = col(a["status"])
            print(f"    {c}>>  {a['parameter']:25s}  {a['value']:>10.3f} {a['unit']:5s}  ->  {a['status']}{RESET}")
    else:
        print(f"\n  {G}[ OK  All parameters within safe operating limits ]{RESET}")

def print_decrypt_check(enc, pkg, tick):
    raw  = enc.decrypt(pkg)
    data = json.loads(raw)
    o2   = data["readings"]["o2_percent"]
    cyl  = data["readings"]["o2_cylinder_bar"]
    print(f"\n  {BOLD}[ DECRYPTION VERIFIED -- TICK #{tick} ]{RESET}")
    print(f"    {G}OK  Auth tag valid -- data integrity confirmed{RESET}")
    print(f"    {DIM}Decrypted O2 Level    : {o2} %{RESET}")
    print(f"    {DIM}Decrypted O2 Cylinder : {cyl} bar{RESET}")

def print_summary(log):
    total  = len(log)
    normal = sum(1 for e in log if not e["alerts"])
    anomal = total - normal

    print(f"\n\n{BOLD}{C}{'='*70}")
    print(f"  SIMULATION COMPLETE -- SUMMARY REPORT")
    print(f"{'='*70}{RESET}")
    print(f"  Total ticks simulated   : {total}")
    print(f"  {G}Normal ticks            : {normal}{RESET}")
    print(f"  {Y}Anomaly ticks           : {anomal}{RESET}")

    all_a = [a for e in log for a in e["alerts"]]
    if all_a:
        from collections import Counter
        counts = Counter(a["parameter"] for a in all_a)
        print(f"\n  Most triggered parameters:")
        for p, cnt in counts.most_common(5):
            print(f"    {Y}>>  {p:30s}  {cnt} alert(s){RESET}")

    last = log[-1]["readings"]
    print(f"\n  {BOLD}Final Sensor State:{RESET}")
    for k, label in PARAM_LABELS.items():
        print(f"    {label}: {last[k]} {THRESHOLDS[k]['unit']}")

    print(f"\n  {BOLD}Encryption Summary:{RESET}")
    print(f"    Algorithm    : AES-256-GCM")
    print(f"    Key size     : 256 bits (32 bytes)")
    print(f"    Mode         : Galois/Counter Mode (authenticated encryption)")
    print(f"    Nonce size   : 96 bits per packet (fresh per transmission)")
    print(f"    Auth tag     : 128 bits (tamper detection)")
    print(f"    Packets enc. : {total}")
    print(f"{BOLD}{C}{'='*70}{RESET}\n")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def run_simulation():
    print_header()
    enc    = AES256Encryptor()
    print_key_info(enc)

    sensor = SubmarineSensorSimulator()
    log    = []
    prev   = None

    scenario = (
        ["normal"]             * 5 +
        ["anomaly_o2_drop"]    * 4 +
        ["anomaly_gas_leak"]   * 4 +
        ["anomaly_pressure"]   * 4 +
        ["normal"]             * 3
    )

    for idx, mode in enumerate(scenario):
        td      = sensor.read(mode)
        alerts  = detect_anomalies(td["readings"], prev)
        enc_pkg = enc.encrypt(json.dumps(td))

        print_tick(td, enc_pkg, alerts)

        if (idx + 1) % 5 == 0:
            print_decrypt_check(enc, enc_pkg, td["tick"])

        log.append({"tick": td["tick"], "readings": td["readings"],
                    "alerts": alerts, "mode": mode})
        prev = dict(td["readings"])
        time.sleep(0.35)

    print_summary(log)


if __name__ == "__main__":
    run_simulation()
