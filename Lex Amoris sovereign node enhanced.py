import os
import asyncio
import json
import logging
import time
from pathlib import Path
from dataclasses import dataclass, asdict
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# ===========================
# CONFIGURAZIONE & CRIPTO
# ===========================
CONFIG_FILE = "config.json"
KEY_FILE = "lex_amoris_key.pem"

def load_config(file_path=CONFIG_FILE):
    if not Path(file_path).exists():
        # Configurazione di default se non esiste
        return {"node_id": "Seedbringer_Node", "alert_threshold": 30}
    with open(file_path, 'r') as f:
        return json.load(f)

def get_node_keys():
    """Recupera o genera le chiavi RSA del nodo."""
    if Path(KEY_FILE).exists():
        with open(KEY_FILE, "rb") as f:
            priv = RSA.import_key(f.read())
    else:
        priv = RSA.generate(2048)
        with open(KEY_FILE, "wb") as f:
            f.write(priv.export_key())
    return priv, priv.publickey()

# ===========================
# LOGGING
# ===========================
def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%H:%M:%S'
    )

# ===========================
# CLASSE DEL NODO SOVRANO
# ===========================
class SovereignNode:
    def __init__(self, config):
        self.config = config
        self.running = False
        self.peers = {} # Dict: {peer_id: public_key_pem}
        self.layers = {"Cognitive": 100, "Technical": 100, "Economic": 100, "Social": 100}
        self.private_key, self.public_key = get_node_keys()
        self.node_id = SHA256.new(self.public_key.export_key()).hexdigest()[:12]
        self.logger = logging.getLogger(f"Node-{self.node_id}")

    def sign_decision(self, record):
        """Firma una decisione Lex Amoris."""
        data = json.dumps(record, sort_keys=True).encode()
        h = SHA256.new(data)
        return pkcs1_15.new(self.private_key).sign(h).hex()

    async def singularity_line(self, expand_check, force_check, context):
        """Implementazione della Singularity Line nel nodo."""
        await asyncio.sleep(0.1) # Pausa di riflessione
        
        is_forcing = force_check()
        is_expanding = expand_check()

        if is_forcing:
            answer = "NO (Contraction/Force detected)"
        elif is_expanding:
            answer = "YES (Expansion detected)"
        else:
            answer = "WAIT (Neutral)"

        record = {
            "ts": time.time(),
            "node": self.node_id,
            "context": context,
            "answer": answer
        }
        record["sig"] = self.sign_decision(record)
        return record

    async def start_node(self):
        self.running = True
        self.logger.info(f"🚀 Nodo Sovrano Online. PubKey: {self.node_id}")
        await self.main_loop()

    async def main_loop(self):
        try:
            while self.running:
                # Esempio di auto-monitoraggio dei Layer
                self.logger.debug(f"Layers Health: {self.layers}")
                
                # Simulazione di una decisione autonoma ogni 10 secondi
                decision = await self.singularity_line(
                    expand_check=lambda: True, 
                    force_check=lambda: False,
                    context="Heartbeat Sync"
                )
                self.logger.info(f"Decisione: {decision['answer']} | Sig: {decision['sig'][:10]}...")
                
                await asyncio.sleep(10)
        except asyncio.CancelledError:
            self.logger.info("Spegnimento asincrono...")
        except Exception as e:
            self.logger.error(f"Errore critico: {e}")

    def stop_node(self):
        self.running = False
        self.logger.info("🛑 Nodo sigillato in sicurezza.")

# ===========================
# ENTRY POINT
# ===========================
async def main():
    setup_logging(logging.INFO)
    config = load_config()
    node = SovereignNode(config)

    try:
        await node.start_node()
    except KeyboardInterrupt:
        node.stop_node()

if __name__ == "__main__":
    asyncio.run(main())
