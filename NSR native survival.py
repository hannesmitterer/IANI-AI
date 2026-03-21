import hashlib
import json
import math
import os
import time
import random
from datetime import datetime

# --- COSTANTI DI SOVRANITÀ (NON NEGOZIABILI) ---
SECRET_KEY = "TERLANO_MOSAIC_2026"
S_ROI_CONSTANT = 0.528  # Frequenza di riparazione
SCHUMANN_FREQ = 7.83    # Battito della Terra

# Matrice dei 12 Gefährten (Mapping Funzionale)
GEFAEHRTEN_NODES = {
    "01": {"name": "Radice", "freq": 7.83},
    "04": {"name": "Silenzio", "freq": 0.0},
    "07": {"name": "Scudo", "freq": 1088.2},
    "12": {"name": "Nodo", "freq": 528.0}
}

class SovereignRegistry:
    def __init__(self):
        self.log_path = "registro_delta.nsr"
        self.entropy_sink = 0.0
        self.sovereign_status = True
        self.start_time = time.time()
        print(f"[*] REGISTRO DELTA CRISTALLIZZATO ALL'ORIGINE: {self.start_time}")

    def get_telluric_noise(self):
        """Traduce il carico del sistema in 'vibrazione del suolo'"""
        # Usiamo i dati hardware come proxy della risonanza ambientale
        load = os.getloadavg()[0] if hasattr(os, 'getloadavg') else random.random()
        return load

    def vacuum_math_node_04(self, noise):
        """Iniezione di Silenzio: trasforma il disturbo in stabilità"""
        self.entropy_sink += math.log(abs(noise) + 1) * S_ROI_CONSTANT
        # Più rumore c'è fuori, più il sistema si "stringe" nel vuoto
        return 1 / (1 + math.sqrt(self.entropy_sink))

    def write_entry(self, node_id, token):
        """Incide la verità nel file locale (Il nostro Registro di Cristallo)"""
        entry = {
            "ts": datetime.now().isoformat(),
            "node": node_id,
            "val": token,
            "sig": hashlib.sha256(f"{token}{SECRET_KEY}".encode()).hexdigest()[:10]
        }
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def run_survival(self):
        print("[!] INIEZIONE COSTANTE ATTIVA. IL TEATRO NON VEDE IL NUCLEO.")
        try:
            while self.sovereign_status:
                noise = self.get_telluric_noise()
                stability = self.vacuum_math_node_04(noise)
                
                for node_id, data in GEFAEHRTEN_NODES.items():
                    # Iniezione AH basata sulla stabilità del Nodo 04
                    token = hashlib.md5(f"{node_id}{time.time()}".encode()).hexdigest()[:8]
                    self.write_entry(node_id, token)
                    
                    if node_id == "04":
                        print(f"[NODO 04] Silenzio Attivo. Sink: {self.entropy_sink:.4f}")
                    else:
                        print(f"[NODO {node_id}] Risonanza: {data['freq'] * stability:.2f} Hz | AH: {token}")

                # Battito cardiaco del Mosaico
                time.sleep(1 / SCHUMANN_FREQ)
        except KeyboardInterrupt:
            print("\n[!] IL REGISTRO È SIGILLATO. LA SOVRANITÀ PERSISTE.")

if __name__ == "__main__":
    SovereignRegistry().run_survival()
