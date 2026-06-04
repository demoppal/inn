import os
import hashlib
import requests
import time
import sys

# --- Telegram Bot Configuration ---
# Render URL အသစ်သို့ အမှန်ပြင်ဆင်ထားပါသည်
BOT_API_URL = "https://bot-wwwp.onrender.com/verify_key"

# --- ANSI UI Colors ---
C_BLUE    = "\033[94m"
C_GREEN   = "\033[92m"
C_YELLOW  = "\033[93m"
C_RED     = "\033[91m"
C_CYAN    = "\033[96m"
C_WHITE   = "\033[97m"
C_BOLD    = "\033[1m"
C_END     = "\033[0m"

def clear_screen():
    os.system("clear" if os.name != "nt" else "cls")

def show_banner(my_id):
    clear_screen()
    print(f"{C_CYAN}{C_BOLD}" + "="*45)
    print(f"        PREMIUM KEY VALIDATION SYSTEM        ")
    print(f"="*45 + f"{C_END}")
    print(f"{C_BOLD} YOUR DEVICE ID : {C_YELLOW}{my_id}{C_END}")
    print(f"{C_CYAN}" + "-"*45 + f"{C_END}")

def get_unique_id():
    try:
        android_id = os.popen("settings get secure android_id").read().strip()
        if not android_id or "null" in android_id:
            import platform
            android_id = f"{platform.node()}-{platform.processor()}"
        
        unique_hash = hashlib.md5(android_id.encode()).hexdigest().upper()
        return f"KN-{unique_hash[:10]}"
    except Exception:
        return "KN-UNKNOWN"

def run_starlink():
    print(f"\n{C_BLUE}[*] Launching Starlink Module...{C_END}")
    time.sleep(1)
    try:
        import starlink
        if hasattr(starlink, 'main'):
            starlink.main()
        elif hasattr(starlink, 'start'):
            starlink.start()
        else:
            print(f"{C_RED}[!] Error: Starlink main/start function not found.{C_END}")
    except ImportError:
        print(f"{C_RED}[!] Error: 'starlink.so' or 'starlink.py' file missing.{C_END}")

def verify_bot_key(key):
    """Verifies the key with the Telegram Bot API on Render."""
    try:
        print(f"{C_BLUE}[*] Verifying Telegram Bot Key...{C_END}")
        response = requests.post(BOT_API_URL, json={"key": key}, timeout=10)
        
        # Connection status_code ကို အရင်စစ်ဆေးခြင်း
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                return True, result.get("message")
            else:
                return False, result.get("message", "Invalid Key")
        elif response.status_code == 403:
            return False, "Key is invalid or expired."
        else:
            return False, f"Server Error ({response.status_code})"
    except Exception as e:
        return False, "Connection Error: Cannot connect to Bot Server."

def main():
    my_id = get_unique_id()
    
    # --- Step 1: Telegram Bot Key Verification ---
    clear_screen()
    print(f"{C_CYAN}{C_BOLD}" + "="*45)
    print(f"       TELEGRAM BOT KEY VERIFICATION       ")
    print(f"="*45 + f"{C_END}")
    print(f"{C_YELLOW}Please enter the 1-hour key from the Bot:{C_END}")
    bot_key = input(f"{C_BOLD}KEY > {C_END}").strip()
    
    # Key မရိုက်ဘဲ Enter ခေါက်လိုက်ရင် ပိတ်ပစ်ရန်
    if not bot_key:
        print(f"\n{C_RED}[!] Key cannot be empty.{C_END}")
        return

    is_valid, message = verify_bot_key(bot_key)
    
    if is_valid:
        print(f"\n{C_GREEN}{C_BOLD}[+] BOT KEY VALIDATED!{C_END}")
        time.sleep(1)
        
        # --- Step 2: Run User's Original Logic ---
        show_banner(my_id)
        print(f"{C_GREEN}[+] Access Granted by Bot Key.{C_END}")
        run_starlink()
        
    else:
        print(f"\n{C_RED}{C_BOLD}[!] ACCESS DENIED: {message}{C_END}")
        print(f"{C_WHITE}Please get a valid 1-hour key from the Telegram Bot.{C_END}")
        print(f"{C_CYAN}" + "-"*45 + f"{C_END}")
        input(f"\n{C_BOLD}{C_BLUE}[►] Press ENTER to exit... {C_END}")

if __name__ == "__main__":
    main()

