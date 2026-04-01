# lex_amoris_sovereign_node.py
# -----------------------------------------------------------------------------
# CITTA DELLA DIGITALE - PROTEZIONE LEX AMORIS (BFT-LITE)
# -----------------------------------------------------------------------------
# - Whitelist Immutabile (The Regent's Circle)
# - Consenso basato sulla Fiducia Radicale
# - Shunning automatico dei nodi schiavi/esterni
# -----------------------------------------------------------------------------

import asyncio
import json
import time
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Set

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# --- CONFIGURAZIONE SOVRANA (WHITELIST) ---
# Qui inseriamo le chiavi pubbliche dei "Gefährten" (Compagni di rotta)
# Solo i messaggi firmati da queste chiavi influenzeranno i Layer.
TRUSTED_PEERS_FILE = Path("trusted_gefährten.json")

def load_trusted_keys() -> Dict[str, str]:
    """Carica la lista delle chiavi pubbliche autorizzate."""
    if not TRUSTED_PEERS_FILE.exists():
        # Inizializzazione: Inseriamo la TUA chiave pubblica come Root
        return {"Regent_Root": "INSERISCI_QUI_LA_TUA_PUB_KEY_PEM"}
    with open(TRUSTED_PEERS_FILE, "r") as f:
        return json.load(f)

TRUSTED_KEYS = load_trusted_keys()

# --- CORE CRITTOGRAFICO ---
KEY_FILE = Path("lex_amoris_key.pem")

def get_keys():
    if KEY_FILE.exists():
        with open(KEY_FILE, "rb") as f:
            priv = RSA.import_key(f.read())
    else:
        priv = RSA.generate(2048)
        with open(KEY_FILE, "wb") as f:
            f.write(priv.export_key())
    return priv, priv.publickey()

_private_key, _public_key = get_keys()

def verify_trust(payload: dict, signature_hex: str) -> bool:
    """Verifica se il mittente è nella Whitelist dei Gefährten."""
    data = json.dumps({k: v for k, v in payload.items() if k != 'signature'}, sort_keys=True).encode()
    h = SHA256.new(data)
    
    for name, key_pem in TRUSTED_KEYS.items():
        try:
            pub_key = RSA.import_key(key_pem)
            pkcs1_15.new(pub_key).verify(h, bytes.fromhex(signature_hex))
            print(f"✅ Identità verificata: {name} (Gefährte)")
            return True
        except (ValueError, TypeError):
            continue
    return False

# --- GESTIONE LAYER CON CONSENSO ---
@dataclass
class LayerState:
    name: str
    score: int = 100
    
    def update(self, delta: int, origin: str):
        self.score = max(0, min(100, self.score + delta))
        print(f"📊 Layer {self.name} aggiornato a {self.score}% da {origin}")

layers = {n: LayerState(n) for n in ["Cognitive", "Technical", "Economic", "Social"]}

# --- IL PONTE (VAKUUM BRÜCKE) ---
async def handle_p2p_message(raw_msg: str):
    """Il setaccio della verità: scarta tutto ciò che non è Amore/Fiducia."""
    try:
        msg = json.loads(raw_msg)
        record = msg['record']
        sig = record['signature']
        
        # 1. Filtro d'ingresso (Non-Slavery Check)
        if verify_trust(record, sig):
            # 2. Sincronizzazione dei Layer
            if "YES" in record['answer']:
                layers["Social"].update(+2, "Network_Expansion")
                layers["Cognitive"].update(+1, "Shared_Truth")
            elif "NO" in record['answer']:
                print("🚨 Allerta da un Compagno: Forzatura rilevata in rete!")
                layers["Technical"].update(-5, "Network_Contraction")
        else:
            print("🛑 Messaggio scartato: Firma non riconosciuta o Nodo Schiavo.")
            
    except Exception as e:
        print(f"⚠️ Errore nel processamento del segnale: {e}")

# --- ESECUZIONE AUTONOMA ---
async def sovereign_loop():
    print(f"🚀 Nodo Lex Amoris Online. ID: {SHA256.new(_public_key.export_key()).hexdigest()[:10]}")
    print("🛡️ Scudo Vakuum: ATTIVO. Solo Gefährten autorizzati possono scrivere nel Registro Delta.")
    
    while True:
        # Simulazione ricezione segnale P2P
        # In produzione: qui si collega al socket libp2p/pubsub
        await asyncio.sleep(5)
        print("--- In ascolto sul Mare dei Dati ---")

if __name__ == "__main__":
    asyncio.run(sovereign_loop())
