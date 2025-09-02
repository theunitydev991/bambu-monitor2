import cv2
import numpy as np
import requests

PRINTER_IP = "192.168.11.101"     # your printer IP
ACCESS_CODE = "32183365"          # your access code

def get_snapshot():
    url = f"http://{PRINTER_IP}/access/{ACCESS_CODE}/snapshot"
    try:
        resp = requests.get(url, stream=True, timeout=5)
        if resp.status_code == 200:
            arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
            frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            return frame
    except requests.RequestException as e:
        print(f"⚠️ Connection error: {e}")
    return None

while True:
    frame = get_snapshot()
    if frame is not None:
        # Resize for smoother display on Pi
        frame = cv2.resize(frame, (640, 360))
    else:
        print("❌ Failed to fetch snapshot")

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
