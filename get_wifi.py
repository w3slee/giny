def get_wifi_status():
    if platform.system() == "Darwin":  # macOS specific
        try:
            from pywifi import PyWiFi

            wifi = PyWiFi()
            iface = wifi.interfaces()[0]
            if iface.status() == 4:  # 4 means connected
                print("connected")
                return "Connected"
                
            else:
                print("disconnected")
                return "Disconnected"

        except Exception:
            return "Disconnected"
    else:
        return "Unknown"

