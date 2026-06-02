import os
import json
import time
import hashlib
import hmac
from typing import Dict, Any
import requests

class OrangeMoneyAPI:
    """Intégration Orange Money"""
    
    def __init__(self):
        self.merchant_key = os.getenv("ORANGE_MERCHANT_KEY", "test_key")
        self.api_secret = os.getenv("ORANGE_API_SECRET", "test_secret")
        self.base_url = "https://api.orange.com/orange-money/webpayment/v1"
        
    def initiate_payment(self, amount: int, phone_number: str, order_id: str) -> Dict[str, Any]:
        """Initier un paiement Orange Money"""
        # Pour le test, simulation
        transaction_id = f"TRX_{int(time.time())}_{order_id}"
        
        return {
            "success": True,
            "transaction_id": transaction_id,
            "payment_url": f"{self.base_url}/redirect",
            "status": "pending",
            "message": f"✅ Demande de paiement de {amount} FCFA envoyée au {phone_number}",
            "code_verification": f"VERIF_{hashlib.md5(str(amount).encode()).hexdigest()[:6]}"
        }
    
    def check_payment_status(self, transaction_id: str) -> Dict[str, Any]:
        """Vérifier le statut d'un paiement"""
        return {
            "status": "completed",
            "transaction_id": transaction_id,
            "amount": 3500,
            "message": "Paiement confirmé"
        }

class WaveAPI:
    """Intégration Wave Money"""
    
    def __init__(self):
        self.api_key = os.getenv("WAVE_API_KEY", "test_key")
        
    def initiate_payment(self, amount: int, phone_number: str) -> Dict[str, Any]:
        transaction_id = f"WAVE_{int(time.time())}"
        return {
            "success": True,
            "transaction_id": transaction_id,
            "status": "pending",
            "message": f"✅ Lien de paiement Wave envoyé au {phone_number}"
        }

class MTNMoneyAPI:
    """Intégration MTN Mobile Money"""
    
    def __init__(self):
        self.api_key = os.getenv("MTN_API_KEY", "test_key")
        
    def initiate_payment(self, amount: int, phone_number: str) -> Dict[str, Any]:
        transaction_id = f"MTN_{int(time.time())}"
        return {
            "success": True,
            "transaction_id": transaction_id,
            "status": "pending",
            "message": f"✅ Demande de paiement MTN de {amount} FCFA envoyée"
        }

def process_payment(service: str, amount: int, phone: str, order_id: str = None):
    """Point d'entrée unique pour les paiements"""
    services = {
        "orange": OrangeMoneyAPI(),
        "wave": WaveAPI(),
        "mtn": MTNMoneyAPI()
    }
    
    if service not in services:
        return {"success": False, "message": "Service de paiement non reconnu"}
    
    api = services[service]
    return api.initiate_payment(amount, phone, order_id)
