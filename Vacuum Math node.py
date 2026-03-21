import hashlib
import json
from datetime import datetime

# --- ESTENSIONE CRITTOGRAFICA ---
SECRET_KEY = "TERLANO_MOSAIC_2026" # Chiave di derivazione per il Registro

class SovereignRegistry(TerlanoHardwareInterface):
    def __init__(self):
        super().__init__()
        self.log_path = "registro_delta.nsr"
        self.entropy_sink = 0.0 # Accumulatore per il Nodo 04
        print("[*] REGISTRO DELTA INIZIALIZZATO: SCRITTURA SINTROPICA ATTIVA.")

    def vacuum_math_node_04(self, external_noise):
        """Nodo 04: Il Silenzio che assorbe l'entropia (Matematica del Vuoto)"""
        # Il silenzio non è assenza, è opposizione di fase 180°
        # Trasforma il rumore esterno in '0' assoluto per il sistema
        self.entropy_sink += math.log(abs(external_noise) + 1) * S_ROI_CONSTANT
        reduction_factor = 1 / (1 + self.entropy_sink)
        return reduction_factor # Moltiplicatore di stabilità

    def write_delta_entry(self, node_id, token):
        """Scrive l'iniezione AH nel registro criptato locale"""
        timestamp = datetime.now().isoformat()
        # Firma Digitale del Mosaico (HMAC-like)
        signature = hashlib.sha256(f"{token}{timestamp}{SECRET_KEY}".encode()).hexdigest()[:16]
        
        entry = {
            "ts": timestamp,
            "node": node_id,
            "token": token,
            "sig": signature,
            "v": "1.0-NSR"
        }

        with open(self.log_path, "a") as f:
            # Scrittura in formato pseudo-JSON per persistenza
            f.write(json.dumps(entry) + "\n")

    def run_survival_loop(self):
        self.activate_vakuum_shield()
        print("[!] IL REGISTRO DELTA STA ORA TESTIMONIANDO LA REALTÀ.")
        
        try:
            while self.sovereign_status:
                # 1. Calcolo del Silenzio (Nodo 04)
                # Assorbiamo una variabile casuale di 'rumore' di sistema
                noise_sample = os.getloadavg()[0] if hasattr(os, 'getloadavg') else 0.5
                stability = self.vacuum_math_node_04(noise_sample)
                
                # 2. Scansione Nodi con Stabilità Applicata
                for node_id, data in GEFAEHRTEN_NODES.items():
                    # Applichiamo il fattore di stabilità del Silenzio a tutte le frequenze
                    adjusted_freq = data['freq'] * stability
                    
                    if node_id == "04":
                        # Il Nodo 04 resta muto ma processa i log
                        print(f"[.] NODO 04 (SILENZIO) ASSORBE ENTROPIA: {self.entropy_sink:.2f}")
                        continue
                    
                    # Emissione Audio (se non è il nodo 04)
                    self.play_frequency(adjusted_freq, 0.03)
                    
                    # Generazione e Registrazione AH
                    ah_token = self.inject_ah_value(node_id)
                    self.write_delta_entry(node_id, ah_token)
                
                # Sincronizzazione finale col battito terrestre
                time.sleep(1 / SCHUMANN_FREQ)
                
        except KeyboardInterrupt:
            print(f"\n[!] SESSIONE CHIUSA. REGISTRO SALVATO IN {self.log_path}")
            print("[*] L'ORDINE SINTROPICO È STATO PRESERVATO.")

# --- ESECUZIONE INTEGRALE ---
if __name__ == "__main__":
    mosaico_finale = SovereignRegistry()
    mosaico_finale.run_survival_loop()
