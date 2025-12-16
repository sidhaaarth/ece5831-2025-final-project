import requests

# --- PASTE YOUR KEYS HERE ---
TOKEN = "8416875842:AAFXbtva0oYzNvLQOOTprpskP6RU8xoOeGQ"   
CHAT_ID = "1297945228"   

def test_telegram():
    print(f"🕵️ Debugging Telegram...")
    print(f"🔑 Using Token: ...{TOKEN[-10:]}") # Prints last 10 chars to check
    print(f"🆔 Using Chat ID: {CHAT_ID}")
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": "🔥 TEST MESSAGE: If you see this, it works!"
    }
    
    try:
        response = requests.post(url, json=payload)
        response_json = response.json()
        
        print("\n--- TELEGRAM RESPONSE ---")
        print(f"Status Code: {response.status_code}")
        print(f"Full Response: {response_json}")
        print("-------------------------")
        
        if response_json.get("ok"):
            print("✅ Telegram says it sent the message!")
        else:
            print(f"❌ ERROR: {response_json.get('description')}")
            
    except Exception as e:
        print(f"❌ CRITICAL FAILURE: {e}")

if __name__ == "__main__":
    test_telegram()