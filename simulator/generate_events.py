import requests, random, time
from datetime import datetime

BACKEND_URL = "http://localhost:8000"

def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

labels = ["motorbike", "motorcycle"]
W, H = 1280, 720
for i in range(100):
    x1 = random.randint(0, W//2)
    y1 = random.randint(0, H//2)
    x2 = x1 + random.randint(40, 160)
    y2 = y1 + random.randint(40, 160)
    cx, cy = (x1+x2)//2, (y1+y2)//2
    evento = "moto_esquerda" if cx < (W//2) else "moto_direita"
    payload = {
        "timestamp": now_str(),
        "label": random.choice(labels),
        "conf": round(random.uniform(0.5, 0.99), 2),
        "x1": x1, "y1": y1, "x2": x2, "y2": y2,
        "cx": cx, "cy": cy, "evento": evento
    }
    r = requests.post(f"{BACKEND_URL}/events", json=payload, timeout=5)
    print(i, r.status_code)
    time.sleep(0.05)
print("done")
