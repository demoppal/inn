import run
import os
import sys

if __name__ == "__main__":
    try:
        # run.so ထဲက start_process function ကို လှမ်းခေါ်ခြင်း
        run.start_process()
    except KeyboardInterrupt:
        print("\n\n \033[1;31m[!] Stopped by user.\033[0m")
        sys.exit()
    except Exception as e:
        print(f"\n\n \033[1;31m[!] Error: {e}\033[0m")
        
