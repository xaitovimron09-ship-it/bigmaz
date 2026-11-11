#!/usr/bin/env python3
"""
bigMAZ PRO Enterprise - Official Telegram Verification & Cabinet Bot
Bot: @bigmaz_bussines_bot
Direct Real-time Shared Database Sync
"""

import sys
import time
import json
import random
import re
import os
import urllib.request
import urllib.parse
from datetime import datetime

# ==================== SOZLAMALAR ====================
BOT_TOKEN = "9258482321:AAGJWbhuCiClZQ0zDJuf4VTgOTV0_GJm4vM"
API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(SCRIPT_DIR, "database.json")

def load_db():
    if not os.path.exists(DB_FILE):
        return {"config": {}, "users": [], "withdrawals": [], "deposits": [], "verification_codes": {}}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[BOT DB ERROR] load_db: {e}")
        return {"config": {}, "users": [], "withdrawals": [], "deposits": [], "verification_codes": {}}

def save_db(data):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[BOT DB ERROR] save_db: {e}")
        return False

# Mapping from chat_id to verified phone number
CHAT_PHONES = {}

def call_api(method, params=None):
    url = f"{API_BASE}/{method}"
    try:
        data = json.dumps(params).encode('utf-8') if params else None
        headers = {'Content-Type': 'application/json'}
        req = urllib.request.Request(url, data=data, headers=headers)
        with urllib.request.urlopen(req, timeout=35) as response:
            res = response.read().decode('utf-8')
            return json.loads(res)
    except Exception as e:
        if "timed out" in str(e).lower():
            return {'ok': True, 'result': []}
        print(f"[XATO] Telegram API ({method}): {e}")
        return None

def send_message(chat_id, text, reply_markup=None):
    params = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML' }
